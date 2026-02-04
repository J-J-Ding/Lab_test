#!/bin/bash

# 批量更新所有子页面的导航栏

# 定义导航栏模板
NAVBAR_LEFT='<ul class="nav-menu left-menu">
        <li><a href="../../index.html">首页</a></li>
        <li><a href="../achievements/index.html">成果汇总</a></li>
        <li><a href="../news/index.html">新闻动态</a></li>
        <li><a href="../blogs/index.html">技术博客</a></li>
        <li><a href="../projects/index.html">课题项目</a></li>
      </ul>'

NAVBAR_CENTER='<a href="../../index.html" class="nav-logo">
        <img src="../../lab-logo.png" alt="智能系统实验室" />
        <span>智能系统实验室</span>
      </a>'

NAVBAR_RIGHT='<ul class="nav-menu right-menu">
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
      </ul>'

FULL_NAVBAR='  <!-- 导航栏 -->
  <nav class="navbar">
    <div class="nav-container">
      '"$NAVBAR_LEFT"'
      '"$NAVBAR_CENTER"'
      '"$NAVBAR_RIGHT"'
    </div>
  </nav>'

echo "导航栏更新脚本已准备"
echo "请手动更新各个页面的导航栏，或将使用 Python/JavaScript 脚本进行批量更新"
