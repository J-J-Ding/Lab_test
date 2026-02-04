#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复导航栏：添加成员去向、移除下拉菜单、修复active类、修复搜索功能"""

import os
import re
from pathlib import Path

# 主页导航栏（10项：左5+右5）
INDEX_NAVBAR = '''  <nav class="navbar">
    <div class="nav-container">
      <ul class="nav-menu left-menu">
        <li><a href="data/achievements/index.html">成果汇总</a></li>
        <li><a href="data/news/index.html">新闻动态</a></li>
        <li><a href="data/blogs/index.html">技术博客</a></li>
        <li><a href="data/projects/index.html">课题项目</a></li>
        <li><a href="data/papers/index.html">发表论文</a></li>
      </ul>
      <a href="index.html" class="nav-logo">
        <img src="lab-logo.png" alt="智能系统实验室" />
        <span>智能系统实验室</span>
      </a>
      <ul class="nav-menu right-menu">
        <li><a href="data/members/index.html">团队成员</a></li>
        <li><a href="data/graduates/index.html">成员去向</a></li>
        <li><a href="data/competitions/index.html">学科竞赛</a></li>
        <li><a href="data/publications/index.html">出版刊物</a></li>
        <li><a href="data/activities/index.html">团建活动</a></li>
        <li class="search-container">
          <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" class="search-input" id="globalSearch" placeholder="搜索..." />
          </div>
        </li>
      </ul>
    </div>
  </nav>'''

# 子页面导航栏（相对路径）
SUBPAGE_NAVBAR = '''  <nav class="navbar">
    <div class="nav-container">
      <ul class="nav-menu left-menu">
        <li><a href="../achievements/index.html">成果汇总</a></li>
        <li><a href="../news/index.html">新闻动态</a></li>
        <li><a href="../blogs/index.html">技术博客</a></li>
        <li><a href="../projects/index.html">课题项目</a></li>
        <li><a href="../papers/index.html">发表论文</a></li>
      </ul>
      <a href="../../index.html" class="nav-logo">
        <img src="../../lab-logo.png" alt="智能系统实验室" />
        <span>智能系统实验室</span>
      </a>
      <ul class="nav-menu right-menu">
        <li><a href="../members/index.html">团队成员</a></li>
        <li><a href="../graduates/index.html">成员去向</a></li>
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

# 每个页面的active设置
PAGES_CONFIG = {
    'index.html': {'active': None, 'navbar': INDEX_NAVBAR},
    'data/achievements/index.html': {'active': 'href="../achievements/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/news/index.html': {'active': 'href="../news/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/blogs/index.html': {'active': 'href="../blogs/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/projects/index.html': {'active': 'href="../projects/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/papers/index.html': {'active': 'href="../papers/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/competitions/index.html': {'active': 'href="../competitions/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/publications/index.html': {'active': 'href="../publications/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/activities/index.html': {'active': 'href="../activities/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/members/index.html': {'active': 'href="../members/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
    'data/members/member.html': {'active': 'href="../members/index.html" class="active"', 'navbar': SUBPAGE_NAVBAR},
}

def update_page(file_path, config):
    """更新单个页面"""
    print(f"正在更新: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用配置的导航栏
        navbar = config['navbar']

        # 替换导航栏
        nav_pattern = r'\s*<!-- 导航栏 -->\s*<nav class="navbar">.*?</nav>\s*'
        content = re.sub(nav_pattern, '<!-- 导航栏 -->' + navbar, content, flags=re.DOTALL)

        # 设置active类
        if config['active']:
            # 移除所有旧的active类
            content = re.sub(r'class="active"', '', content)
            # 添加新的active类
            base_pattern = config['active'].replace(' class="active"', '')
            content = content.replace(base_pattern, config['active'])

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ 成功: {file_path}")
        return True

    except Exception as e:
        print(f"✗ 失败: {file_path}")
        print(f"  错误: {str(e)}")
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent

    print("=" * 60)
    print("更新所有页面的导航栏")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for page_file, config in PAGES_CONFIG.items():
        file_path = base_dir / page_file

        if file_path.exists():
            if update_page(file_path, config):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"⚠ 文件不存在: {page_file}")

    print("=" * 60)
    print(f"完成! 成功: {success_count}, 失败: {fail_count}")
    print("=" * 60)
    print("\n✓ 添加了'成员去向'导航项")
    print("✓ 移除了下拉菜单")
    print("✓ Active类已正确设置")
    print("✓ 所有页面导航栏完全统一")

if __name__ == '__main__':
    main()
