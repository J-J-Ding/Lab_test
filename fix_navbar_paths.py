#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复子页面的导航栏路径问题"""

import os
import re
from pathlib import Path

# 子页面的正确导航栏
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

# 定义每个页面的active链接
PAGES_CONFIG = {
    'data/achievements/index.html': 'href="../achievements/index.html" class="active"',
    'data/news/index.html': 'href="../news/index.html" class="active"',
    'data/blogs/index.html': 'href="../blogs/index.html" class="active"',
    'data/projects/index.html': 'href="../projects/index.html" class="active"',
    'data/papers/index.html': 'href="../papers/index.html" class="active"',
    'data/competitions/index.html': 'href="../competitions/index.html" class="active"',
    'data/publications/index.html': 'href="../publications/index.html" class="active"',
    'data/activities/index.html': 'href="../activities/index.html" class="active"',
    'data/members/index.html': 'href="../members/index.html" class="active"',
    'data/members/member.html': 'href="../members/index.html" class="active"',
}

def fix_page(file_path, active_link=None):
    """修复单个页面"""
    print(f"正在修复: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换导航栏
        nav_pattern = r'\s*<nav class="navbar">.*?</nav>\s*'
        content = re.sub(nav_pattern, SUBPAGE_NAVBAR, content, flags=re.DOTALL)

        # 设置active类
        if active_link:
            # 移除旧的active类
            content = re.sub(r'class="active"', '', content)
            # 添加新的active类
            content = content.replace(active_link.replace('class="active"', ''), active_link)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ 成功修复: {file_path}")
        return True

    except Exception as e:
        print(f"✗ 修复失败: {file_path}")
        print(f"  错误: {str(e)}")
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent

    print("=" * 60)
    print("开始修复所有子页面的导航栏")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for page_file, active_link in PAGES_CONFIG.items():
        file_path = base_dir / page_file

        if file_path.exists():
            if fix_page(file_path, active_link):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"⚠ 文件不存在: {page_file}")
            fail_count += 1

    print("=" * 60)
    print(f"修复完成! 成功: {success_count}, 失败: {fail_count}")
    print("=" * 60)
    print("\n✓ 所有子页面现在使用正确的统一导航栏")
    print("✓ Active类已正确设置")

if __name__ == '__main__':
    main()
