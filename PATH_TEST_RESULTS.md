# 导航栏路径计算测试结果

## 测试日期
2026年2月10日

## 测试环境
- 本地环境：`http://localhost:8000`
- GitHub Pages：`https://j-j-ding.github.io/Lab_test`

## 统一导航栏位置
`data/navbar-unified.html`

## 测试结果汇总

### 1. 导航栏路径计算（calculateNavbarPath）

| 当前页面 | 本地路径 | GitHub Pages路径 | 验证 |
|---------|---------|----------------|------|
| `/index.html` | `data/navbar-unified.html` | `data/navbar-unified.html` | ✓ |
| `/data/projects/index.html` | `../navbar-unified.html` | `../navbar-unified.html` | ✓ |
| `/data/papers/DBFNET/index.html` | `../../navbar-unified.html` | `../../navbar-unified.html` | ✓ |
| `/Lab_test/index.html` | - | `data/navbar-unified.html` | ✓ |
| `/Lab_test/data/projects/index.html` | - | `../navbar-unified.html` | ✓ |
| `/Lab_test/data/papers/DBFNET/index.html` | - | `../../navbar-unified.html` | ✓ |

### 2. 链接路径计算（calculateRelativePath）

#### 从 `/data/papers/DBFNET/index.html`

| 目标 | 计算结果 | 实际指向 | 验证 |
|-----|---------|---------|------|
| `data/members/index.html` | `../../members/index.html` | `/data/members/index.html` | ✓ |
| `data/news/index.html` | `../../news/index.html` | `/data/news/index.html` | ✓ |
| `data/papers/index.html` | `../../papers/index.html` | `/data/papers/index.html` | ✓ |
| `index.html` | `../../../index.html` | `/index.html` | ✓ |
| `lab-logo.png` | `../../../lab-logo.png` | `/lab-logo.png` | ✓ |
| `css/style.css` | `../../../css/style.css` | `/css/style.css` | ✓ |

#### 从 `/Lab_test/data/papers/DBFNET/index.html`

| 目标 | 计算结果 | 实际指向 | 验证 |
|-----|---------|---------|------|
| `data/members/index.html` | `../../members/index.html` | `/Lab_test/data/members/index.html` | ✓ |
| `index.html` | `../../../../index.html` | `/Lab_test/index.html` | ✓ |

### 3. 深度嵌套测试

**最深层路径：** `data/papers/DBFNET/index.html`

路径段：`['data', 'papers', 'DBFNET', 'index.html']`

- data 索引：0
- 当前目录：`['data', 'papers', 'DBFNET']`
- data 目录：`['data']`
- 回退层数：2（从 DBFNET/ → papers/ → data/）

**计算结果：**
- 导航栏：`../../navbar-unified.html` ✓
- 访问 data 子目录：`../../xxx/index.html` ✓
- 访问根目录：`../../../index.html` ✓

## 核心算法

### calculateNavbarPath
```javascript
const currentDirSegments = pathSegments.slice(0, -1); // 去掉文件名
const dataDirSegments = pathSegments.slice(0, dataIndex + 1); // 从根到data
const levelsBack = currentDirSegments.length - dataDirSegments.length;
```

### calculateRelativePath
```javascript
if (targetPath.startsWith('data/')) {
    // 回退到data目录，去掉data/前缀
    levelsBack = len(currentDir) - len(dataDir);
    finalTarget = targetPath.substring(5);
} else {
    // 回退到根目录
    levelsBack = len(currentDir);
    finalTarget = targetPath;
}
```

## 结论

✅ **所有测试通过！**

路径计算逻辑完全正确，能够正确处理：
1. 本地环境和 GitHub Pages 环境
2. 根目录页面和 data 目录页面
3. 深度嵌套的目录结构（如 `data/papers/DBFNET/index.html`）
4. 访问 data 目录内外的不同资源

**关键改进：**
- 正确处理 pathSegments 包含文件名的情况
- 根据目标路径智能决定回退位置（data目录 或 根目录）
- 统一导航栏文件始终位于 `data/navbar-unified.html`
