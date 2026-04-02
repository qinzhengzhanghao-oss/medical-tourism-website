#!/usr/bin/env python3
"""
完整功能优化脚本 - 基于智能体修复原则
为所有页面添加完整功能和设计优化
"""

import os
import re
from pathlib import Path
from datetime import datetime

def log_message(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def ensure_design_system(html_content):
    """确保引入设计系统"""
    if 'design-system.css' not in html_content:
        # 在head中添加设计系统链接
        design_system_link = '<link rel="stylesheet" href="design-system.css">'
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'    {design_system_link}\n</head>')
        elif '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n    {design_system_link}')
    return html_content

def enhance_navigation(html_content, page_type):
    """增强导航功能"""
    enhancements = []
    
    # 检查是否有导航结构
    if 'nav' not in html_content.lower() and 'navbar' not in html_content.lower():
        # 添加基础导航
        nav_template = '''
    <nav class="navbar">
        <div class="container nav-container">
            <a href="index.html" class="nav-logo">医疗旅游</a>
            <button class="nav-toggle">
                <span class="nav-toggle-icon"></span>
            </button>
            <ul class="nav-menu">
                <li><a href="index.html" class="nav-link">首页</a></li>
                <li><a href="about.html" class="nav-link">关于我们</a></li>
                <li><a href="services.html" class="nav-link">服务</a></li>
                <li><a href="contact.html" class="nav-link">联系</a></li>
            </ul>
        </div>
    </nav>'''
        
        # 插入到body开始处
        if '<body>' in html_content:
            html_content = html_content.replace('<body>', f'<body>\n{nav_template}')
            enhancements.append("添加标准导航")
    
    return html_content, enhancements

def enhance_forms(html_content):
    """增强表单功能"""
    enhancements = []
    
    # 检查是否有表单
    if '<form' in html_content:
        # 确保表单使用设计系统类
        form_patterns = [
            (r'<input[^>]*>', self_closing=True),
            (r'<textarea[^>]*>.*?</textarea>', self_closing=False),
            (r'<select[^>]*>.*?</select>', self_closing=False),
            (r'<button[^>]*>.*?</button>', self_closing=False),
        ]
        
        # 简化：添加表单容器
        if 'form-group' not in html_content:
            # 在form标签后添加类提示
            html_content = html_content.replace('<form', '<form class="form-container"')
            enhancements.append("优化表单结构")
    
    return html_content, enhancements

def enhance_mobile_experience(html_content):
    """增强移动端体验"""
    enhancements = []
    
    # 添加触摸优化
    if 'touch-action' not in html_content:
        touch_css = '''
    <style>
    /* 触摸优化 */
    button, a, input, textarea, select {
        touch-action: manipulation;
    }
    
    /* 最小触摸目标大小 */
    @media (max-width: 768px) {
        button, .btn, a.nav-link {
            min-height: 44px;
            min-width: 44px;
            padding: 12px 16px;
        }
    }
    </style>'''
        
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{touch_css}\n</head>')
            enhancements.append("添加触摸优化")
    
    return html_content, enhancements

def enhance_content_structure(html_content):
    """增强内容结构"""
    enhancements = []
    
    # 确保使用容器类
    if 'container' not in html_content and 'main' in html_content.lower():
        # 在main内容外添加容器
        main_pattern = r'<main[^>]*>(.*?)</main>'
        match = re.search(main_pattern, html_content, re.DOTALL | re.IGNORECASE)
        if match:
            main_content = match.group(1)
            new_main = f'<main>\n    <div class="container">\n{main_content}\n    </div>\n</main>'
            html_content = html_content.replace(match.group(0), new_main)
            enhancements.append("优化内容容器")
    
    return html_content, enhancements

def add_interactivity(html_content):
    """添加交互功能"""
    enhancements = []
    
    # 添加导航切换JavaScript
    if 'nav-toggle' in html_content and 'nav-menu' in html_content:
        js_code = '''
    <script>
    // 导航菜单切换
    document.addEventListener('DOMContentLoaded', function() {
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', function() {
                navMenu.classList.toggle('active');
            });
            
            // 点击菜单外关闭菜单
            document.addEventListener('click', function(event) {
                if (!navToggle.contains(event.target) && !navMenu.contains(event.target)) {
                    navMenu.classList.remove('active');
                }
            });
        }
    });
    </script>'''
        
        if '</body>' in html_content:
            html_content = html_content.replace('</body>', f'{js_code}\n</body>')
            enhancements.append("添加导航交互")
    
    return html_content, enhancements

def main():
    print("=" * 60)
    print("🚀 完整功能优化脚本")
    print("基于智能体修复原则，为所有页面添加完整功能")
    print("=" * 60)
    
    # 获取所有HTML文件
    html_files = list(Path('.').glob('*.html'))
    log_message(f"找到 {len(html_files)} 个HTML文件")
    
    # 排除备份文件
    core_files = [f for f in html_files if 'backup' not in str(f) and 'test' not in str(f).lower()]
    log_message(f"核心文件: {len(core_files)} 个")
    
    optimized_count = 0
    total_enhancements = []
    
    for html_file in core_files[:50]:  # 先处理前50个，避免时间过长
        log_message(f"优化: {html_file.name}")
        
        try:
            # 读取文件
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_enhancements = []
            
            # 1. 确保设计系统
            content = ensure_design_system(content)
            
            # 2. 增强导航
            content, nav_enhance = enhance_navigation(content, html_file.name)
            file_enhancements.extend(nav_enhance)
            
            # 3. 增强表单
            content, form_enhance = enhance_forms(content)
            file_enhancements.extend(form_enhance)
            
            # 4. 增强移动端体验
            content, mobile_enhance = enhance_mobile_experience(content)
            file_enhancements.extend(mobile_enhance)
            
            # 5. 增强内容结构
            content, content_enhance = enhance_content_structure(content)
            file_enhancements.extend(content_enhance)
            
            # 6. 添加交互功能
            content, interact_enhance = add_interactivity(content)
            file_enhancements.extend(interact_enhance)
            
            # 如果有优化，保存文件
            if file_enhancements:
                # 创建备份
                backup_file = f"{html_file}.backup.enhance_{datetime.now().strftime('%H%M%S')}"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 保存优化后的文件
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                optimized_count += 1
                total_enhancements.append((html_file.name, file_enhancements))
                log_message(f"  ✅ 优化: {', '.join(file_enhancements)}")
            else:
                log_message(f"  ⏭️ 无需优化")
                
        except Exception as e:
            log_message(f"  ❌ 错误: {str(e)[:50]}...")
    
    print("\n" + "=" * 60)
    print("🎯 优化完成!")
    print(f"✅ 优化了 {optimized_count}/{len(core_files)} 个核心文件")
    
    # 输出优化摘要
    if total_enhancements:
        print("\n📋 优化摘要:")
        categories = {}
        for file_name, enhancements in total_enhancements:
            for enhancement in enhancements:
                categories[enhancement] = categories.get(enhancement, 0) + 1
        
        for enhancement, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {enhancement}: {count} 个文件")
    
    # 生成报告
    report_file = "enhancement-report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"""# 完整功能优化报告

## 执行时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 优化统计
- 总HTML文件: {len(html_files)} 个
- 核心文件: {len(core_files)} 个
- 优化文件: {optimized_count} 个
- 优化率: {optimized_count/len(core_files)*100:.1f}%

## 优化内容
""")
        
        for enhancement, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {enhancement}: {count} 个文件\n")
        
        f.write("""
## 下一步建议
1. **测试功能**: 验证导航、表单、移动端功能
2. **设计检查**: 确保设计系统正确应用
3. **性能测试**: 检查页面加载性能
4. **用户测试**: 收集真实用户反馈
""")
    
    log_message(f"报告已保存: {report_file}")
    print(f"\n📄 详细报告: {report_file}")

if __name__ == '__main__':
    main()