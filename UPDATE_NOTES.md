# 项目更新说明

## 已完成的优化

### 1. ✅ 导航栏优化
- **新布局**：采用三栏布局，LOGO居中，导航菜单分布在两侧
- **导航项精简**：
  - 左侧（5项）：成果汇总、新闻动态、技术博客、课题项目、发表论文
  - 右侧（5项）：团队成员（下拉菜单）、学科竞赛、出版刊物、团建活动、搜索框
- **下拉菜单**：团队成员包含子菜单（全部成员、师资队伍、学生培养）
- **响应式设计**：导航栏按钮使用相对单位（%、vw）而非固定像素
- **LOGO位置**：LOGO显示在导航栏中间，"智能系统实验室"文字在LOGO下方

### 2. ✅ 全屏轮播图
- **全屏显示**：轮播图高度为 `100vh - 90px`，占满整个页面
- **图片占位**：所有轮播图使用 `lab-logo.png` 作为占位符
- **容器适配**：图片使用 `object-fit: contain` 确保完整显示

### 3. ✅ 搜索功能
- **全局搜索框**：在导航栏右侧添加搜索框
- **搜索脚本**：创建了 `js/search.js` 提供搜索功能
- **搜索逻辑**：支持实时搜索和回车搜索
- **搜索结果**：以模态框形式展示搜索结果

### 4. ✅ CSS优化
- **导航栏CSS**：更新为支持三栏布局
- **下拉菜单**：添加下拉菜单样式和动画
- **搜索框样式**：添加搜索框和输入框样式
- **响应式优化**：改进移动端导航栏显示

### 5. ✅ 内容分离示例
- **示例文件**：
  - `data/content-example/news-001.html` - 单个新闻内容文件
  - `data/content-example/news-index.html` - 新闻列表页面示例
- **文件结构**：每个内容项有单独的HTML文件，index.html仅链接列表

## 待手动更新的页面

以下页面需要手动更新导航栏，使其与新的三栏布局一致：

### 需要更新的页面列表：

1. **data/blogs/index.html**
2. **data/projects/index.html**
3. **data/papers/index.html**
4. **data/competitions/index.html**
5. **data/publications/index.html**
6. **data/teachers/index.html**
7. **data/students/index.html**
8. **data/activities/index.html**
9. **data/members/member.html**

### 更新导航栏的步骤：

#### 1. 替换旧的导航栏为新的三栏布局

**旧导航栏结构：**
```html
<nav class="navbar">
  <div class="nav-container">
    <div class="nav-logo">
      <img src="..." />
      <span>...</span>
    </div>
    <ul class="nav-menu">
      <li><a href="...">...</a></li>
      <!-- 更多导航项 -->
    </ul>
  </div>
</nav>
```

**新导航栏结构：**
```html
<nav class="navbar">
  <div class="nav-container">
    <ul class="nav-menu left-menu">
      <li><a href="../../index.html">首页</a></li>
      <li><a href="../achievements/index.html">成果汇总</a></li>
      <li><a href="../news/index.html">新闻动态</a></li>
      <li><a href="../blogs/index.html">技术博客</a></li>
      <li><a href="../projects/index.html">课题项目</a></li>
    </ul>
    <a href="../../index.html" class="nav-logo">
      <img src="../../lab-logo.png" alt="智能系统实验室" />
      <span>智能系统实验室</span>
    </a>
    <ul class="nav-menu right-menu">
      <li class="nav-dropdown">
        <a href="../members/index.html">团队成员 ▾</a>
        <div class="nav-dropdown-content">
          <a href="../members/index.html">全部成员</a>
          <a href="../teachers/index.html">师资队伍</a></li>
          <a href="../students/index.html">学生培养</a>
        </div>
      </li>
      <li><a href="../papers/index.html">发表论文</a></li>
      <li><a href="../competitions/index.html">学科竞赛</a></li>
      <li><a href="../publications/index.html">出版刊物</a></li>
      <li><a href="../activities/index.html">团建活动</a></li>
      <li class="search-container">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" class="search-input" id="globalSearch" placeholder="搜索..." />
        </div>
      </li>
    </ul>
  </div>
</nav>
```

#### 2. 更新active类
- 根据当前页面，将对应的 `<a>` 标签添加 `class="active"` 属性

#### 3. 添加搜索脚本
在页面底部 `</body>` 标签之前添加：
```html
<script src="../../js/search.js"></script>
```

### 各页面active类位置：

- **blogs/index.html**：`<li><a href="../blogs/index.html" class="active">技术博客</a></li>`
- **projects/index.html**：`<li><a href="../projects/index.html" class="active">课题项目</a></li>`
- **papers/index.html**：`<li><a href="../papers/index.html" class="active">发表论文</a></li>`
- **competitions/index.html**：`<li><a href="../competitions/index.html" class="active">学科竞赛</a></li>`
- **publications/index.html**：`<li><a href="../publications/index.html" class="active">出版刊物</a></li>`
- **teachers/index.html**：下拉菜单中的 `<a href="../teachers/index.html">师资队伍</a>`
- **students/index.html**：下拉菜单中的 `<a href="../students/index.html">学生培养</a>`
- **activities/index.html**：`<li><a href="../activities/index.html" class="active">团建活动</a></li>`
- **members/member.html**：团队成员页面保持不变

## 项目文件结构

```
Lab_test/
├── index.html                    # 主页（已更新）
├── css/
│   ├── style.css               # 主样式（已更新）
│   └── slider.css             # 轮播图样式（已更新）
├── js/
│   ├── slider.js              # 轮播图脚本
│   └── search.js             # 搜索脚本（新增）
├── lab-logo.png              # LOGO文件
├── data/
│   ├── achievements/         # 成果汇总（已更新）
│   │   └── index.html
│   ├── news/               # 新闻动态（已更新）
│   │   └── index.html
│   ├── members/            # 团队成员（已更新）
│   │   ├── index.html
│   │   └── member.html
│   ├── blogs/              # 技术博客（待更新）
│   ├── projects/           # 课题项目（待更新）
│   ├── papers/             # 发表论文（待更新）
│   ├── competitions/       # 学科竞赛（待更新）
│   ├── publications/       # 出版刊物（待更新）
│   ├── teachers/           # 师资队伍（待更新）
│   ├── students/           # 学生培养（待更新）
│   ├── activities/         # 团建活动（待更新）
│   └── content-example/    # 内容分离示例
│       ├── news-001.html
│       └── news-index.html
└── README.md
```

## CSS文件按模块分离（可选）

如果需要为每个栏目创建专属CSS文件：

1. 在 `data/栏目名/css/` 目录下创建 `style.css`
2. 在页面 `<head>` 中引入：
   ```html
   <link rel="stylesheet" href="../../css/style.css" />
   <link rel="stylesheet" href="css/style.css" />
   ```

示例：
```html
<!-- data/news/index.html -->
<head>
  <link rel="stylesheet" href="../../css/style.css" />
  <link rel="stylesheet" href="css/style.css" />  <!-- 新闻专属样式 -->
</head>
```

## 内容分离建议

### 当前结构（推荐更新为）
```
data/news/
├── index.html              # 新闻列表页面
├── news-001.html          # 单个新闻详情
├── news-002.html          # 单个新闻详情
└── ...
```

### index.html 中如何链接
```html
<div class="item-card">
  <h3>新闻标题</h3>
  <div class="item-meta">
    <span>📅 2025-01-01</span>
  </div>
  <p>新闻摘要...</p>
  <a href="news-001.html" class="item-link">阅读更多 →</a>
</div>
```

### 内容文件结构
每个 `news-XXX.html` 文件包含完整的页面结构（导航栏、文章内容等），参考 `data/content-example/news-001.html`

## 注意事项

1. **图片占位符**：所有临时使用在线占位图片的地方，都改为使用 `lab-logo.png`
2. **全屏轮播**：轮播图高度为 `calc(100vh - 90px)`，确保在不同屏幕上都全屏
3. **响应式**：导航栏在移动端会自动折叠为垂直布局
4. **搜索功能**：搜索功能目前是前端实现，如需完整搜索功能需要后端支持或配置静态数据文件
