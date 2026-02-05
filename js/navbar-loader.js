// 智能导航栏加载器 - 兼容本地和HTTP环境
function loadNavbar() {
    const navbarContainer = document.getElementById('navbar-container');
    if (!navbarContainer) {
        console.warn('导航栏容器未找到');
        return;
    }

    // 计算当前页面相对于根目录的层级
    const currentPath = window.location.pathname;
    const pathSegments = currentPath.split('/').filter(Boolean);
    const pathDepth = pathSegments.length;

    // 计算导航栏文件的相对路径
    let navbarPath = calculateNavbarPath(pathDepth, pathSegments);

    console.log('当前路径:', currentPath, '层级:', pathDepth, '导航栏路径:', navbarPath);

    // 使用绝对URL路径避免CORS问题
    const baseUrl = window.location.origin + window.location.pathname.replace(/\/[^\/]*$/, '/');
    const navbarUrl = baseUrl + navbarPath;

    fetch(navbarUrl, { cache: 'no-store' })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            navbarContainer.innerHTML = html;

            // 修正导航栏中的所有链接路径
            fixAllNavbarLinks(pathDepth);

            // 设置当前页面的激活状态
            setActiveNavItem();

            // 初始化搜索功能
            initializeSearch();
        })
        .catch(error => {
            console.error('加载导航栏失败:', error);
            console.error('尝试的URL:', navbarUrl);
            // 显示更详细的错误信息
            navbarContainer.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #666; background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; margin: 10px;">
                    <strong>导航栏加载失败</strong><br>
                    <small>路径: ${navbarPath}</small><br>
                    <small>错误: ${error.message}</small>
                </div>`;
        });
}

// 计算导航栏文件的相对路径
function calculateNavbarPath(pathDepth, pathSegments) {
    // 查找data目录的位置
    let dataIndex = -1;
    for (let i = 0; i < pathSegments.length; i++) {
        if (pathSegments[i] === 'data') {
            dataIndex = i;
            break;
        }
    }

    // 根据不同的环境计算路径
    if (dataIndex === -1) {
        // 根目录页面 (index.html)
        return 'data/navbar-unified.html';
    } else {
        // data目录或其子目录下的页面
        // 计算从当前页面回退到data目录的层数
        // 例如: /Lab_test/data/papers/index.html
        // pathSegments = ['Lab_test', 'data', 'papers', 'index.html']
        // pathDepth = 4, dataIndex = 1
        // data目录深度 = dataIndex + 1 = 2
        // 需要回退: 4 - 2 = 2层
        const dataDepth = dataIndex + 1;
        const levelsToData = pathDepth - dataDepth;

        let relativePath = '';
        for (let i = 0; i < levelsToData; i++) {
            relativePath += '../';
        }
        return relativePath + 'navbar-unified.html';
    }
}

// 修正导航栏中的所有链接路径
// function fixAllNavbarLinks(pathDepth) {
//     // 修正logo链接
//     const logoLink = document.querySelector('.nav-logo');
//     if (logoLink) {
//         logoLink.href = calculateRelativePath('index.html', pathDepth);
//     }
    
//     // 修正logo图片
//     const logoImg = document.querySelector('.nav-logo img');
//     if (logoImg) {
//         logoImg.src = calculateRelativePath('lab-logo.png', pathDepth);
//     }
    
//     // 修正所有导航链接
//     const navLinks = document.querySelectorAll('.nav-menu a:not(.nav-logo)');
//     navLinks.forEach(link => {
//         const originalHref = link.getAttribute('href');
//         if (originalHref && !originalHref.startsWith('http')) {
//             link.href = calculateRelativePath('data/' + originalHref, pathDepth);
//         }
//     });
// }

function fixAllNavbarLinks(pathDepth) {
    // 获取当前页面信息
    const currentPath = window.location.pathname;
    const pathSegments = currentPath.split('/').filter(Boolean);

    // 查找data目录的位置
    let dataIndex = -1;
    for (let i = 0; i < pathSegments.length; i++) {
        if (pathSegments[i] === 'data') {
            dataIndex = i;
            break;
        }
    }

    // 更严格的"不要改写"的判断：外链/协议链接/锚点都跳过
    function shouldRewrite(href) {
        if (!href) return false;
        if (href.startsWith('#')) return false;                 // #anchor
        if (/^(https?:)?\/\//i.test(href)) return false;        // http:// https:// //cdn...
        if (/^[a-z][a-z0-9+.-]*:/i.test(href)) return false;    // mailto: tel: javascript: data: ...
        return true;
    }

    // 统一把 href 变成"站内相对路径"再交给 calculateRelativePath
    function toInternalTarget(href) {
        // 去掉开头的 /，避免 GitHub Pages 项目页下被解析到域名根
        let p = href.replace(/^\/+/, "");

        // 避免重复拼 data/
        if (!p.startsWith("data/")) p = "data/" + p;

        // 清理可能出现的 data/data/（防御性）
        p = p.replace(/^data\/data\//, "data/");

        return p;
    }

    // 修正logo链接
    const logoLink = document.querySelector('.nav-logo');
    if (logoLink) {
        logoLink.setAttribute('href', calculateRelativePath('index.html', pathDepth));
    }

    // 修正logo图片
    const logoImg = document.querySelector('.nav-logo img');
    if (logoImg) {
        logoImg.setAttribute('src', calculateRelativePath('lab-logo.png', pathDepth));
    }

    // 修正所有导航链接
    const navLinks = document.querySelectorAll('.nav-menu a:not(.nav-logo)');
    navLinks.forEach(link => {
        const originalHref = link.getAttribute('href');

        // ✅ 不要只判断 startsWith('http')，要判断"所有协议/外链/锚点"
        if (!shouldRewrite(originalHref)) return;

        // 只改写站内页面：统一转成 data/xxx 再算相对路径
        const target = toInternalTarget(originalHref);

        // ✅ 用 setAttribute 保留相对路径形式（更好排查）
        link.setAttribute('href', calculateRelativePath(target, pathDepth));
    });
}


// 计算相对路径 - 优化为基于data目录的准确计算
function calculateRelativePath(targetPath, currentDepth) {
    const currentPath = window.location.pathname;
    const pathSegments = currentPath.split('/').filter(Boolean);

    // 查找data目录的位置
    let dataIndex = -1;
    for (let i = 0; i < pathSegments.length; i++) {
        if (pathSegments[i] === 'data') {
            dataIndex = i;
            break;
        }
    }

    if (dataIndex === -1) {
        // 根目录页面，直接使用目标路径
        return targetPath;
    } else {
        // data目录或其子目录下的页面
        // 计算从当前页面回退到data目录的层数
        // 例如: /Lab_test/data/papers/index.html
        // pathSegments = ['Lab_test', 'data', 'papers', 'index.html']
        // currentDepth = 4, dataIndex = 1
        // data目录深度 = 2
        // 需要回退: 4 - 2 = 2层

        const dataDepth = dataIndex + 1;
        const levelsToData = currentDepth - dataDepth;

        // 如果目标路径以data/开头，去掉它因为我们已经在data目录下
        if (targetPath.startsWith('data/')) {
            targetPath = targetPath.substring(5);
        }

        let relativePath = '';
        for (let i = 0; i < levelsToData; i++) {
            relativePath += '../';
        }
        return relativePath + targetPath;
    }
}

// 设置当前页面的导航项为激活状态
// function setActiveNavItem() {
//     const currentPath = window.location.pathname;
//     const navLinks = document.querySelectorAll('.nav-menu a');
    
//     // 提取当前页面的关键标识
//     const pathParts = currentPath.split('/').filter(Boolean);
//     const currentPageIdentifier = pathParts.length > 1 ? pathParts[pathParts.length - 2] : '';
    
//     navLinks.forEach(link => {
//         link.classList.remove('active');
//         const href = link.getAttribute('href');
        
//         if (href && !href.startsWith('http')) {
//             // 检查链接是否指向当前页面或相关页面
//             if (href.includes(currentPageIdentifier) && currentPageIdentifier !== '') {link.classList.add('active');}
//             // if (href.includes(currentPageIdentifier) || 
//             //     (currentPageIdentifier === '' && href.includes('index.html'))) {
//             //     link.classList.add('active');
//             // }
//         }
//     });
// }

function setActiveNavItem() {
  const navLinks = document.querySelectorAll('.nav-menu a');
  if (!navLinks.length) return;

  // 规范化 pathname：统一 index.html、尾斜杠、解码
  function normalizePath(p) {
    p = decodeURIComponent(p || '/');
    p = p.replace(/\/index\.html?$/i, '/'); // /index.html => /
    p = p.replace(/\/+$/, '/');             // 去掉多余尾斜杠
    return p;
  }

  const currentPath = normalizePath(window.location.pathname);

  let bestLink = null;
  let bestScore = -1;

  navLinks.forEach(link => {
    link.classList.remove('active');

    const href = link.getAttribute('href');
    if (!href) return;

    // 跳过外链/协议链接/#锚点（不要误改）
    if (href.startsWith('#')) return;
    if (/^(https?:)?\/\//i.test(href)) return;
    if (/^[a-z][a-z0-9+.-]*:/i.test(href)) return; // mailto: tel: javascript: ...

    // 用 URL 解析相对路径，避免层级深时匹配失真
    const linkPath = normalizePath(new URL(href, window.location.origin).pathname);

    // 评分：优先"完全相等"，其次"前缀命中（栏目/目录）"，且选最长命中
    let score = -1;

    if (currentPath === linkPath) {
      score = 1_000_000 + linkPath.length; // 完全命中最大
    } else {
      // 前缀命中要做"边界判断"，避免 /data 匹配到 /database
      const isPrefix =
        linkPath !== '/' &&
        currentPath.startsWith(linkPath) &&
        (linkPath.endsWith('/') || currentPath.charAt(linkPath.length) === '/');

      if (isPrefix) score = linkPath.length;
      // 首页兜底：/ 或 /index.html
      if (linkPath === '/' && currentPath === '/') score = Math.max(score, 1);
    }

    if (score > bestScore) {
      bestScore = score;
      bestLink = link;
    }
  });

  if (bestLink) bestLink.classList.add('active');
}


// 初始化搜索功能
function initializeSearch() {
    const searchInput = document.getElementById('globalSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.trim();
            if (searchTerm.length > 2) {
                console.log('搜索关键词:', searchTerm);
                // 这里可以添加实际的搜索逻辑
            }
        });
    }
}

// 页面加载完成后加载导航栏
document.addEventListener('DOMContentLoaded', loadNavbar);