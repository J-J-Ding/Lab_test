#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加新论文并更新搜索配置的脚本
"""

import os
import sys
import shutil
from pathlib import Path

def add_new_paper():
    """添加新论文到系统"""
    print("=" * 50)
    print("添加新论文到智能系统实验室")
    print("=" * 50)
    
    # 获取论文信息
    paper_id = input("\n请输入论文ID（目录名，如 DBFNET）: ").strip()
    if not paper_id:
        print("❌ 论文ID不能为空")
        return
    
    paper_title = input("请输入论文标题: ").strip()
    journal = input("请输入发表期刊: ").strip()
    publish_date = input("请输入发表时间（格式：YYYY-MM）: ").strip()
    abstract = input("请输入论文摘要: ").strip()
    paper_link = input("请输入论文链接（留空则无）: ").strip()
    
    # 获取作者列表
    authors_input = input("请输入作者列表（用逗号分隔，格式：姓名_ID，如：Junjie_Ding, Jiangwen_Xiao）: ").strip()
    authors = [a.strip() for a in authors_input.split(',') if a.strip()]
    
    print("\n" + "=" * 50)
    print("论文信息:")
    print(f"  论文ID: {paper_id}")
    print(f"  论文标题: {paper_title}")
    print(f"  期刊: {journal}")
    print(f"  发表时间: {publish_date}")
    print(f"  作者: {', '.join(authors)}")
    print("=" * 50)
    
    confirm = input("\n确认信息是否正确？(y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消")
        return
    
    # 创建论文目录
    base_dir = Path(__file__).parent.parent / 'data' / 'papers'
    paper_dir = base_dir / paper_id
    
    if paper_dir.exists():
        print(f"⚠️  目录 {paper_id} 已存在")
        overwrite = input("是否覆盖？(y/n): ").strip().lower()
        if overwrite != 'y':
            print("❌ 已取消")
            return
        shutil.rmtree(paper_dir)
    
    paper_dir.mkdir(exist_ok=True)
    print(f"✅ 创建目录: {paper_dir}")
    
    # 复制文件
    logo_path = Path(__file__).parent.parent / 'lab-logo.png'
    example_pdf = Path(__file__).parent.parent / 'example_pdf.pdf'
    
    # 复制论文原文
    pdf_dest = paper_dir / f"{paper_id}.pdf"
    if example_pdf.exists():
        shutil.copy2(example_pdf, pdf_dest)
        print(f"✅ 复制论文原文: {pdf_dest}")
    
    # 复制论文封面
    paper_cover_dest = paper_dir / f"{paper_id}_paper.png"
    shutil.copy2(logo_path, paper_cover_dest)
    print(f"✅ 复制论文封面: {paper_cover_dest}")
    
    # 复制技术路线图
    framework_dest = paper_dir / f"{paper_id}_Framework.png"
    shutil.copy2(logo_path, framework_dest)
    print(f"✅ 复制技术路线图: {framework_dest}")
    
    # 生成论文详情页
    detail_html = generate_detail_html(paper_id, paper_title, journal, publish_date, abstract, paper_link, authors)
    detail_path = paper_dir / 'index.html'
    with open(detail_path, 'w', encoding='utf-8') as f:
        f.write(detail_html)
    print(f"✅ 生成详情页: {detail_path}")
    
    # 更新论文列表页
    update_papers_list(paper_id, paper_title, journal, publish_date, abstract, authors, base_dir)
    
    # 更新搜索配置
    update_search_config(paper_id)
    
    print("\n" + "=" * 50)
    print("✅ 论文添加完成！")
    print("=" * 50)
    print(f"\n📝 下一步:")
    print(f"  1. 替换 {paper_dir / f'{paper_id}.pdf'} 为真实论文PDF")
    print(f"  2. 替换 {paper_dir / f'{paper_id}_paper.png'} 为真实论文封面（A4比例）")
    print(f"  3. 替换 {paper_dir / f'{paper_id}_Framework.png'} 为真实技术路线图")
    print(f"  4. 如有其他插图，添加到 {paper_dir} 目录中")

def generate_detail_html(paper_id, paper_title, journal, publish_date, abstract, paper_link, authors):
    """生成论文详情页HTML"""
    authors_html = '\n              '.join([
        f'<a href="../../members/index.html#{author}" class="paper-author-link">👤 {author}</a>'
        for author in authors
    ])
    
    paper_links_html = ''
    if paper_link:
        paper_links_html = f'''
              <a href="{paper_link}" target="_blank" class="paper-link-card">
                <div class="paper-link-icon">🔗</div>
                <div class="paper-link-info">
                  <div class="paper-link-title">论文链接</div>
                  <div class="paper-link-desc">访问官方论文页面</div>
                </div>
              </a>'''
    
    return f'''<!doctype html>
<html lang="zh">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{paper_title} - 智能系统实验室</title>
  <link rel="stylesheet" href="../../../css/style.css" />
  <link rel="stylesheet" href="css/paper_detail.css" />
</head>
<body>
  <nav class="navbar">
    <div class="nav-container">
      <ul class="nav-menu left-menu">
        <li><a href="../../achievements/index.html">成果汇总</a></li>
        <li><a href="../../news/index.html">新闻动态</a></li>
        <li><a href="../../blogs/index.html">技术博客</a></li>
        <li><a href="../../projects/index.html">课题项目</a></li>
        <li><a href="../index.html" class="active">发表论文</a></li>
      </ul>
      <a href="../../../index.html" class="nav-logo">
        <img src="../../../lab-logo.png" alt="智能系统实验室" />
        <span>智能系统实验室</span>
      </a>
      <ul class="nav-menu right-menu">
        <li><a href="../../competitions/index.html">学科竞赛</a></li>
        <li><a href="../../publications/index.html">出版刊物</a></li>
        <li><a href="../../members/index.html">团队成员</a></li>
        <li><a href="../../graduates/index.html">成员去向</a></li>
        <li><a href="../../activities/index.html">团建活动</a></li>
        <li class="search-container">
          <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" class="search-input" id="globalSearch" placeholder="搜索..." />
          </div>
        </li>
      </ul>
    </div>
  </nav>

  <main class="main-content" style="padding-top: 70px;">
    <section class="section">
      <div class="section-container">
        <div class="back-button">
          <a href="../index.html" class="btn btn-outline">← 返回论文列表</a>
        </div>

        <div class="paper-detail-container">
          <!-- 论文头部 -->
          <div class="paper-header">
            <h1 class="paper-title">{paper_title}</h1>
            
            <div class="paper-authors">
              {authors_html}
            </div>
            
            <div class="paper-meta">
              <div class="paper-meta-item">
                <span class="paper-meta-label">📄 发表期刊:</span>
                <span class="paper-meta-value">{journal}</span>
              </div>
              <div class="paper-meta-item">
                <span class="paper-meta-label">📅 发表时间:</span>
                <span class="paper-meta-value">{publish_date}</span>
              </div>
            </div>
          </div>

          <!-- 论文摘要 -->
          <div class="paper-section" data-search="abstract">
            <h2 class="paper-section-title">论文摘要</h2>
            <p class="paper-abstract">
              {abstract}
            </p>
          </div>

          <!-- 技术路线 -->
          <div class="paper-section" data-search="framework">
            <h2 class="paper-section-title">技术路线</h2>
            <div class="paper-framework">
              <img src="{paper_id}_Framework.png" alt="{paper_title} Framework" class="paper-framework-image" onerror="this.src='../../../lab-logo.png'" />
              <p class="paper-framework-caption">{paper_title} 技术框架图</p>
            </div>
          </div>

          <!-- 下载链接 -->
          <div class="paper-section">
            <h2 class="paper-section-title">资源下载</h2>
            <div class="paper-links">
{paper_links_html}
              <a href="{paper_id}.pdf" target="_blank" class="paper-link-card">
                <div class="paper-link-icon">📄</div>
                <div class="paper-link-info">
                  <div class="paper-link-title">论文原文</div>
                  <div class="paper-link-desc">下载PDF文档</div>
                </div>
              </a>
              <a href="{paper_id}_paper.png" target="_blank" class="paper-link-card">
                <div class="paper-link-icon">🖼️</div>
                <div class="paper-link-info">
                  <div class="paper-link-title">论文封面</div>
                  <div class="paper-link-desc">查看封面图片</div>
                </div>
              </a>
            </div>
          </div>

          <!-- 论文详细信息 -->
          <div class="paper-section">
            <h2 class="paper-section-title">论文信息</h2>
            <div class="paper-info-grid">
              <div class="paper-info-item">
                <div class="paper-info-label">论文类型</div>
                <div class="paper-info-value">期刊论文</div>
              </div>
              <div class="paper-info-item">
                <div class="paper-info-label">期刊等级</div>
                <div class="paper-info-value">CCF-A类</div>
              </div>
              <div class="paper-info-item">
                <div class="paper-info-label">影响因子</div>
                <div class="paper-info-value">--</div>
              </div>
              <div class="paper-info-item">
                <div class="paper-info-label">研究领域</div>
                <div class="paper-info-value">人工智能</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <script src="../../../js/search.js"></script>
</body>
</html>'''

def update_papers_list(paper_id, paper_title, journal, publish_date, abstract, authors, base_dir):
    """更新论文列表页面"""
    list_path = base_dir / 'index.html'
    
    # 读取现有内容
    with open(list_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 摘要截断（如果太长）
    abstract_display = abstract[:150] + '...' if len(abstract) > 150 else abstract
    
    # 生成作者链接
    authors_html = '<span>, </span>\n                '.join([
        f'<a href="../members/index.html#{author}" class="item-link">{author}</a>'
        for author in authors
    ])
    
    # 生成论文卡片HTML
    card_html = f'''
          <div class="item-card" data-date="{publish_date}">
            <div class="item-title">{paper_title}</div>
            <div class="item-meta">
              <span>📄 {journal}</span>
              <span>📅 {publish_date}</span>
            </div>
            <div class="item-content">
              {abstract_display}
            </div>
            <div class="item-footer">
              <div class="item-author">
                <span>👤</span>
                {authors_html}
              </div>
              <a href="{paper_id}/index.html" class="btn btn-sm">查看详情</a>
            </div>
          </div>'''
    
    # 在contentList后插入新卡片
    content_list_marker = '<div id="contentList">'
    if content_list_marker in content:
        content = content.replace(content_list_marker, content_list_marker + '\n          ' + card_html.strip())
        with open(list_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 更新论文列表: {list_path}")
    else:
        print(f"⚠️  未找到contentList标记，请手动添加到论文列表")

def update_search_config(paper_id):
    """更新搜索配置"""
    search_js_path = Path(__file__).parent.parent / 'js' / 'search.js'
    
    with open(search_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在getKnownPaperDirs函数中添加新论文ID
    old_pattern = "return ['DBFNET'];"
    new_pattern = f"return ['DBFNET', '{paper_id}'];"
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        with open(search_js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 更新搜索配置: {search_js_path}")
    else:
        print(f"⚠️  请手动在 search.js 的 getKnownPaperDirs() 中添加 '{paper_id}'")

def main():
    """主函数"""
    try:
        add_new_paper()
    except KeyboardInterrupt:
        print("\n\n❌ 操作已中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
