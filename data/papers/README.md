# 发表论文栏目说明

## 文件结构

```
data/papers/
├── index.html              # 论文列表页面（主页）
├── css/
│   └── paper_detail.css  # 论文详情页样式
└── [论文ID]/              # 每篇论文独立文件夹
    ├── index.html          # 论文详情页
    ├── [论文ID].pdf       # 论文原文PDF
    ├── [论文ID]_paper.png # 论文封面图
    └── [论文ID]_Framework.png # 技术路线图
```

## 添加新论文步骤

### 1. 创建论文文件夹
```bash
cd data/papers
mkdir 论文ID
```

### 2. 准备文件
- 论文原文PDF：重命名为 `[论文ID].pdf`
- 论文封面图：重命名为 `[论文ID]_paper.png`（建议A4比例）
- 技术路线图：重命名为 `[论文ID]_Framework.png`

### 3. 创建详情页 index.html
参考 `DBFNET/index.html` 的格式，包含以下内容：
- 论文标题
- 作者列表（使用锚点链接到团队成员页面，格式：`../members/index.html#成员ID`）
- 发表期刊
- 发表时间
- 论文摘要（过长用...表示）
- 论文链接
- 论文原文下载
- 论文封面展示
- 技术路线预览
- 论文详细信息（类型、等级、影响因子、研究领域等）

### 4. 在 index.html 中添加论文卡片
在 `data/papers/index.html` 的 `#contentList` 中添加论文卡片：

```html
<div class="item-card" data-date="YYYY-MM">
  <div class="item-title">论文标题</div>
  <div class="item-meta">
    <span>📄 期刊名</span>
    <span>📅 发表时间(YYYY-MM)</span>
  </div>
  <div class="item-content">
    摘要内容（过长用...表示）
  </div>
  <div class="item-footer">
    <div class="item-author">
      <span>👤</span>
      <a href="../members/index.html#成员ID1" class="item-link">作者1</a>
      <span>, </span>
      <a href="../members/index.html#成员ID2" class="item-link">作者2</a>
    </div>
    <a href="论文ID/index.html" class="btn btn-sm">查看详情</a>
  </div>
</div>
```

## 作者链接规范

### 成员ID格式
- 使用下划线连接姓和名：`FirstName_LastName` 或 `中文名`
- 示例：`Junjie_Ding`, `Jiangwen_Xiao`, `张三`

### 团队成员页面锚点
在团队成员页面中，每位成员的卡片需要添加对应ID的锚点：
```html
<div class="member-card" id="成员ID">
  <!-- 成员信息 -->
</div>
```

这样论文中的作者链接会自动跳转到对应成员的位置。

## 排序规则
论文列表按 `data-date` 属性（发表时间）倒序排列，最新的论文显示在最前面。

## 图片规范
- 论文封面：A4比例（210mm × 297mm 或 1:1.414），推荐宽度800px
- 技术路线图：横向或纵向布局，保持清晰度，推荐宽度1200px
- 暂无图片时使用 `lab-logo.png` 作为占位符

## 搜索集成
论文标题、作者、摘要会自动被搜索功能索引，无需额外配置。
