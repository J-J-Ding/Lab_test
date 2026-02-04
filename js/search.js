// 全局搜索功能 - 扫描data目录中的内容
(function() {
  'use strict';

  // 搜索结果数据（从各页面标题和描述中提取）
  let searchData = [];

  // 页面配置：页面路径、标题、描述、分类
  const PAGE_CONFIG = [
    { url: 'data/achievements/index.html', title: '成果汇总', desc: '展示实验室所有成果，包括项目、论文、竞赛、刊物等', category: '成果汇总' },
    { url: 'data/news/index.html', title: '新闻动态', desc: '实验室最新新闻和活动', category: '新闻动态' },
    { url: 'data/blogs/index.html', title: '技术博客', desc: '实验室成员的技术博客和心得', category: '技术博客' },
    { url: 'data/projects/index.html', title: '课题项目', desc: '实验室承担的科研项目', category: '课题项目' },
    { url: 'data/papers/index.html', title: '发表论文', desc: '发表的学术论文', category: '发表论文' },
    { url: 'data/competitions/index.html', title: '学科竞赛', desc: '参与的各类学科竞赛', category: '学科竞赛' },
    { url: 'data/publications/index.html', title: '出版刊物', desc: '出版的书籍和刊物', category: '出版刊物' },
    { url: 'data/activities/index.html', title: '团建活动', desc: '实验室团队建设活动', category: '团建活动' },
    { url: 'data/members/index.html', title: '团队成员', desc: '实验室全体成员信息', category: '团队成员' },
    { url: 'data/graduates/index.html', title: '成员去向', desc: '毕业学生去向统计', category: '成员去向' }
  ];

  // 内容关键词映射
  const CONTENT_KEYWORDS = [
    { keywords: ['项目', '科研', '课题', '基金', '研发', '创新'], url: 'data/projects/index.html', title: '课题项目', category: '课题项目' },
    { keywords: ['论文', '期刊', '发表', 'CVPR', 'ICCV', 'NeurIPS', '会议'], url: 'data/papers/index.html', title: '发表论文', category: '发表论文' },
    { keywords: ['竞赛', '获奖', '一等奖', '二等奖', '挑战', '比赛'], url: 'data/competitions/index.html', title: '学科竞赛', category: '学科竞赛' },
    { keywords: ['书', '教材', '出版', '刊物', '专著'], url: 'data/publications/index.html', title: '出版刊物', category: '出版刊物' },
    { keywords: ['新闻', '动态', '活动', '会议', '庆典', '事件'], url: 'data/news/index.html', title: '新闻动态', category: '新闻动态' },
    { keywords: ['博客', '技术', '心得', '分享', '文章', '教程'], url: 'data/blogs/index.html', title: '技术博客', category: '技术博客' },
    { keywords: ['活动', '团建', '聚餐', '旅游', '户外'], url: 'data/activities/index.html', title: '团建活动', category: '团建活动' },
    { keywords: ['成员', '团队', '老师', '学生', '博士', '硕士', '本科'], url: 'data/members/index.html', title: '团队成员', category: '团队成员' },
    { keywords: ['成果', '项目', '论文', '竞赛', '刊物', '奖项'], url: 'data/achievements/index.html', title: '成果汇总', category: '成果汇总' },
    { keywords: ['毕业', '就业', '去向', '工作', '深造', '企业', '高校'], url: 'data/graduates/index.html', title: '成员去向', category: '成员去向' }
  ];

  class GlobalSearch {
    constructor() {
      this.searchInput = document.getElementById('globalSearch');
      if (!this.searchInput) return;

      this.searchResultsBox = null;
      this.init();
    }

    init() {
      // 输入事件
      this.searchInput.addEventListener('input', this.debounce((e) => {
        const query = this.searchInput.value.trim();
        if (query.length > 0) {
          this.performSearch(query);
        } else {
          this.hideResults();
        }
      }, 300));

      // 回车键搜索
      this.searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          const query = this.searchInput.value.trim();
          if (query.length > 0) {
            this.performSearch(query);
          }
        }
      });

      // 点击搜索图标
      this.searchInput.parentElement.addEventListener('click', (e) => {
        if (e.target.classList.contains('search-icon')) {
          this.searchInput.focus();
        }
      });

      // 点击页面其他地方隐藏结果
      document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-container')) {
          this.hideResults();
        }
      });
    }

    // 防抖函数
    debounce(func, wait) {
      let timeout;
      return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
      };
    }

    // 执行搜索
    performSearch(query) {
      const results = this.searchPages(query);
      this.displayResults(results, query);
    }

    // 搜索页面
    searchPages(query) {
      const queryLower = query.toLowerCase();
      const results = [];

      // 搜索页面标题和描述
      PAGE_CONFIG.forEach(page => {
        const titleMatch = page.title.toLowerCase().includes(queryLower);
        const descMatch = page.desc.toLowerCase().includes(queryLower);
        const categoryMatch = page.category.toLowerCase().includes(queryLower);

        if (titleMatch || descMatch || categoryMatch) {
          results.push({
            title: page.title,
            desc: page.desc,
            url: page.url,
            category: page.category,
            matchType: titleMatch ? '标题' : (descMatch ? '描述' : '分类')
          });
        }
      });

      // 根据关键词搜索
      CONTENT_KEYWORDS.forEach(item => {
        const keywordMatch = item.keywords.some(kw => kw.includes(queryLower));
        if (keywordMatch) {
          // 检查是否已存在
          const exists = results.some(r => r.url === item.url);
          if (!exists) {
            results.push({
              title: item.title,
              desc: `包含相关内容: ${query}`,
              url: item.url,
              category: item.category,
              matchType: '关键词'
            });
          }
        }
      });

      return results;
    }

    // 显示搜索结果
    displayResults(results, query) {
      if (!this.searchResultsBox) {
        this.createResultsBox();
      }

      if (results.length === 0) {
        this.searchResultsBox.innerHTML = `
          <div class="search-no-results">
            <div class="no-results-icon">🔍</div>
            <p>未找到相关内容</p>
            <p class="no-results-tip">试试搜索：项目、论文、竞赛、新闻、成员...</p>
          </div>
        `;
        this.showResults();
        return;
      }

      const resultsHtml = results.map(item => `
        <div class="search-result-item" data-url="${item.url}">
          <div class="search-result-main">
            <div class="search-result-title">${this.highlightMatch(item.title, query)}</div>
            <div class="search-result-desc">${item.desc}</div>
          </div>
          <div class="search-result-meta">
            <span class="search-result-category">${item.category}</span>
            <span class="search-result-match">匹配: ${item.matchType}</span>
          </div>
        </div>
      `).join('');

      this.searchResultsBox.innerHTML = `
        <div class="search-results-header">
          <span>找到 ${results.length} 个结果</span>
          <span class="close-search" onclick="document.querySelector('.search-results').classList.remove('show')">×</span>
        </div>
        <div class="search-results-list">${resultsHtml}</div>
      `;

      this.showResults();
      this.attachResultClickHandlers();
    }

    // 高亮匹配文本
    highlightMatch(text, query) {
      if (!query) return text;
      const regex = new RegExp(`(${query})`, 'gi');
      return text.replace(regex, '<mark class="search-highlight">$1</mark>');
    }

    // 创建结果框
    createResultsBox() {
      this.searchResultsBox = document.createElement('div');
      this.searchResultsBox.id = 'searchResults';
      this.searchResultsBox.className = 'search-results';

      // 添加样式
      if (!document.getElementById('searchResultsStyles')) {
        const style = document.createElement('style');
        style.id = 'searchResultsStyles';
        style.textContent = `
          #searchResults {
            position: fixed;
            top: 110px;
            right: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
            max-width: 450px;
            width: 90%;
            max-height: 500px;
            overflow-y: auto;
            z-index: 1002;
            display: none;
            border: 1px solid var(--border-color);
          }
          #searchResults.show {
            display: block;
            animation: fadeIn 0.3s ease;
          }
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
          }
          .search-results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid var(--border-color);
            background: var(--bg-secondary);
            border-radius: 12px 12px 0 0;
          }
          .search-results-header span:first-child {
            font-weight: 600;
            color: var(--text-primary);
            font-size: 14px;
          }
          .close-search {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: rgba(0,0,0,0.05);
            border: none;
            cursor: pointer;
            font-size: 20px;
            color: var(--text-light);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            line-height: 1;
          }
          .close-search:hover {
            background: rgba(0,0,0,0.1);
            color: var(--text-primary);
          }
          .search-results-list {
            padding: 10px;
          }
          .search-result-item {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px solid transparent;
          }
          .search-result-item:hover {
            background: var(--bg-secondary);
            border-color: var(--primary-color);
          }
          .search-result-main {
            margin-bottom: 12px;
          }
          .search-result-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
          }
          .search-result-desc {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
          }
          .search-result-meta {
            display: flex;
            gap: 12px;
            align-items: center;
          }
          .search-result-category {
            background: var(--primary-color);
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
          }
          .search-result-match {
            font-size: 12px;
            color: var(--text-light);
          }
          .search-highlight {
            background: #fef08a;
            padding: 2px 6px;
            border-radius: 3px;
          }
          .search-no-results {
            padding: 40px 20px;
            text-align: center;
          }
          .no-results-icon {
            font-size: 48px;
            margin-bottom: 15px;
            opacity: 0.5;
          }
          .search-no-results p {
            margin: 10px 0;
            color: var(--text-secondary);
          }
          .no-results-tip {
            font-size: 13px;
            color: var(--text-light);
          }
          @media (max-width: 768px) {
            #searchResults {
              top: auto;
              bottom: 10px;
              right: 10px;
              left: 10px;
              max-height: 60vh;
            }
          }
        `;
        document.head.appendChild(style);
      }

      document.body.appendChild(this.searchResultsBox);
    }

    // 显示结果
    showResults() {
      this.searchResultsBox.classList.add('show');
    }

    // 隐藏结果
    hideResults() {
      if (this.searchResultsBox) {
        this.searchResultsBox.classList.remove('show');
      }
    }

    // 附加结果点击事件
    attachResultClickHandlers() {
      const items = this.searchResultsBox.querySelectorAll('.search-result-item');
      items.forEach(item => {
        item.addEventListener('click', (e) => {
          e.preventDefault();
          const url = item.dataset.url;
          if (url) {
            window.location.href = url;
          }
        });
      });
    }
  }

  // 页面加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new GlobalSearch());
  } else {
    new GlobalSearch();
  }
})();
