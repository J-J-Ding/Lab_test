#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一所有页面的导航栏 - 去除首页按钮，只保留统一导航"""

import os
import re
from pathlib import Path

# 统一的导航栏HTML（所有页面完全相同）
UNIFIED_NAVBAR = '''  <nav class="navbar">
    <div class="nav-container">
      <ul class="nav-menu left-menu">
        <li><a href="../../index.html">成果汇总</a></li>
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

# 主页的导航栏（没有相对路径）
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

# 定义每个页面的active位置
PAGES_CONFIG = {
    'index.html': {'active': None, 'navbar': INDEX_NAVBAR},
    'data/achievements/index.html': {'active': '<li><a href="data/achievements/index.html" class="active">成果汇总</a></li>', 'navbar': INDEX_NAVBAR},
    'data/news/index.html': {'active': '<li><a href="data/news/index.html" class="active">新闻动态</a></li>', 'navbar': INDEX_NAVBAR},
    'data/blogs/index.html': {'active': '<li><a href="data/blogs/index.html" class="active">技术博客</a></li>', 'navbar': INDEX_NAVBAR},
    'data/projects/index.html': {'active': '<li><a href="data/projects/index.html" class="active">课题项目</a></li>', 'navbar': INDEX_NAVBAR},
    'data/papers/index.html': {'active': '<li><a href="data/papers/index.html" class="active">发表论文</a></li>', 'navbar': INDEX_NAVBAR},
    'data/competitions/index.html': {'active': '<li><a href="data/competitions/index.html" class="active">学科竞赛</a></li>', 'navbar': INDEX_NAVBAR},
    'data/publications/index.html': {'active': '<li><a href="data/publications/index.html" class="active">出版刊物</a></li>', 'navbar': INDEX_NAVBAR},
    'data/activities/index.html': {'active': '<li><a href="data/activities/index.html" class="active">团建活动</a></li>', 'navbar': INDEX_NAVBAR},
    'data/members/index.html': {'active': '<li><a href="data/members/index.html" class="active">团队成员</a></li>', 'navbar': INDEX_NAVBAR},
    'data/members/member.html': {'active': '<li><a href="data/members/index.html" class="active">团队成员</a></li>', 'navbar': INDEX_NAVBAR},
}

def update_page(file_path, config):
    """更新单个页面的导航栏"""
    print(f"正在更新: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用配置的导航栏
        navbar = config['navbar']

        # 替换旧的导航栏
        nav_pattern = r'\s*<nav class="navbar">.*?</nav>\s*'
        content = re.sub(nav_pattern, navbar, content, flags=re.DOTALL)

        # 设置active类
        if config['active']:
            content = content.replace(config['active'].replace(' class="active"', ''), config['active'])

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
    base_dir = Path(__file__).parent

    print("=" * 60)
    print("开始统一所有页面的导航栏")
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
            fail_count += 1

    print("=" * 60)
    print(f"更新完成! 成功: {success_count}, 失败: {fail_count}")
    print("=" * 60)
    print("\n✓ 所有页面现在使用完全相同的导航栏")
    print("✓ LOGO可点击跳转到首页")
    print("✓ 无'首页'导航按钮")
    print("✓ 只有当前栏目用蓝框标注")

if __name__ == '__main__':
    main()
