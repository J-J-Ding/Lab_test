#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为每个页面设置正确的active类"""

import os
from pathlib import Path

PAGES_ACTIVE = {
    'data/achievements/index.html': '成果汇总',
    'data/news/index.html': '新闻动态',
    'data/blogs/index.html': '技术博客',
    'data/projects/index.html': '课题项目',
    'data/papers/index.html': '发表论文',
    'data/competitions/index.html': '学科竞赛',
    'data/publications/index.html': '出版刊物',
    'data/activities/index.html': '团建活动',
    'data/members/index.html': '团队成员',
}

def set_active_class(file_path, title):
    """设置active类"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 移除所有active类
        content = content.replace('class="active"', '')

        # 添加新的active类到对应的标题
        pattern = f'href="[^"]*">{title}</a>'
        replacement = f'href="../{file_path.parent.name}/index.html" class="active">{title}</a>'
        content = content.replace(pattern, replacement)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ {file_path}: 已设置 active='{title}'")
        return True
    except Exception as e:
        print(f"✗ {file_path}: {str(e)}")
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent

    print("=" * 60)
    print("开始设置导航栏active类")
    print("=" * 60)

    success = 0
    for page_file, title in PAGES_ACTIVE.items():
        file_path = base_dir / page_file
        if file_path.exists():
            if set_active_class(file_path, title):
                success += 1

    print("=" * 60)
    print(f"完成! 成功设置 {success} 个页面")

if __name__ == '__main__':
    main()
