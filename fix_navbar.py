#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复导航栏 - 去除下拉菜单中的多余项"""

import os
from pathlib import Path

# 需要更新的页面
PAGES = [
    'data/achievements/index.html',
    'data/news/index.html',
    'data/blogs/index.html',
    'data/projects/index.html',
    'data/papers/index.html',
    'data/competitions/index.html',
    'data/publications/index.html',
    'data/teachers/index.html',
    'data/students/index.html',
    'data/activities/index.html',
    'data/members/index.html',
    'data/members/member.html',
]

# 新的团队成员下拉菜单HTML
NEW_DROPDOWN = '''<li class="nav-dropdown">
          <a href="../members/index.html">团队成员 ▾</a>
          <div class="nav-dropdown-content">
            <a href="../members/index.html">团队成员</a>
          </div>
        </li>'''

# 旧的下拉菜单HTML（需要替换的）
OLD_DROPDOWN_PATTERNS = [
    '''<li class="nav-dropdown">
          <a href="../members/index.html">团队成员 ▾</a>
          <div class="nav-dropdown-content">
            <a href="../members/index.html">全部成员</a>
            <a href="../teachers/index.html">师资队伍</a>
            <a href="../students/index.html">学生培养</a>
          </div>
        </li>''',
    '''<li class="nav-dropdown">
          <a href="../../index.html">团队成员 ▾</a>
          <div class="nav-dropdown-content">
            <a href="../members/index.html">全部成员</a>
            <a href="../teachers/index.html">师资队伍</a>
            <a href="../students/index.html">学生培养</a>
          </div>
        </li>''',
]

def fix_page(file_path):
    """修复单个页面"""
    print(f"正在修复: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查并替换下拉菜单
        for old_dropdown in OLD_DROPDOWN_PATTERNS:
            if old_dropdown in content:
                content = content.replace(old_dropdown, NEW_DROPDOWN)
                print(f"  ✓ 已替换下拉菜单")
                break

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"  ✗ 修复失败: {e}")
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent

    print("=" * 60)
    print("开始修复导航栏下拉菜单")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for page in PAGES:
        file_path = base_dir / page

        if file_path.exists():
            if fix_page(file_path):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"⚠ 文件不存在: {page}")
            fail_count += 1

    print("=" * 60)
    print(f"修复完成! 成功: {success_count}, 失败: {fail_count}")
    print("=" * 60)

if __name__ == '__main__':
    main()
