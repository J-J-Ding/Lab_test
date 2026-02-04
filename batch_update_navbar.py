#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新导航栏脚本
用于将所有子页面的导航栏更新为新的三栏布局
"""

import os
import re
from pathlib import Path

# 定义页面及其对应的active导航项
PAGES_CONFIG = {
    'blogs/index.html': {
        'active': '<li><a href="../blogs/index.html" class="active">技术博客</a></li>',
        'section': '技术博客'
    },
    'projects/index.html': {
        'active': '<li><a href="../projects/index.html" class="active">课题项目</a></li>',
        'section': '课题项目'
    },
    'papers/index.html': {
        'active': '<li><a href="../papers/index.html" class="active">发表论文</a></li>',
        'section': '发表论文'
    },
    'competitions/index.html': {
        'active': '<li><a href="../competitions/index.html" class="active">学科竞赛</a></li>',
        'section': '学科竞赛'
    },
    'publications/index.html': {
        'active': '<li><a href="../publications/index.html" class="active">出版刊物</a></li>',
        'section': '出版刊物'
    },
    'teachers/index.html': {
        'active': '<a href="../teachers/index.html">师资队伍</a>',  # 在下拉菜单中
        'section': '师资队伍'
    },
    'students/index.html': {
        'active': '<a href="../students/index.html">学生培养</a>',  # 在下拉菜单中
        'section': '学生培养'
    },
    'activities/index.html': {
        'active': '<li><a href="../activities/index.html" class="active">团建活动</a></li>',
        'section': '团建活动'
    }
}

# 新的导航栏HTML模板
NEW_NAVBAR = '''  <!-- 导航栏 -->
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
  </nav>'''

# 搜索脚本
SEARCH_SCRIPT = '''  <script src="../../js/search.js"></script>
</body>
</html>'''

def update_page(file_path, config):
    """更新单个页面的导航栏"""
    print(f"正在更新: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. 替换导航栏
        # 查找旧的 <nav> 标签并替换
        nav_pattern = r'\s*<!-- 导航栏 -->.*?</nav>\s*'
        content = re.sub(nav_pattern, NEW_NAVBAR, content, flags=re.DOTALL)

        # 2. 设置active类
        active_link = config['active']
        if 'class="active"' not in active_link:
            # 对于下拉菜单中的项，需要特殊处理
            content = content.replace(active_link, active_link.replace('>', ' class="active">'))

        # 3. 添加搜索脚本
        if SEARCH_SCRIPT.strip() not in content:
            content = re.sub(r'\s*</body>\s*</html>\s*$', SEARCH_SCRIPT, content, flags=re.MULTILINE)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ 成功更新: {file_path}")
        return True

    except Exception as e:
        print(f"✗ 更新失败: {file_path}")
        print(f"  错误: {str(e)}")
        return False

def main():
    """主函数"""
    data_dir = Path(__file__).parent / 'data'

    if not data_dir.exists():
        print(f"错误: data 目录不存在 - {data_dir}")
        return

    print("=" * 60)
    print("开始批量更新导航栏")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for page_file, config in PAGES_CONFIG.items():
        file_path = data_dir / page_file

        if file_path.exists():
            if update_page(file_path, config):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"⚠ 文件不存在: {page_file}")
            fail_count += 1

    print("=" * 60)
    print(f"更新完成!")
    print(f"成功: {success_count}, 失败: {fail_count}")
    print("=" * 60)

if __name__ == '__main__':
    main()
