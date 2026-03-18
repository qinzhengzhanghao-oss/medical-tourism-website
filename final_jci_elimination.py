#!/usr/bin/env python3
"""
全网站JCI表述最终清除脚本
基于彻底清查结果，确保零遗漏
"""

import os
import re
import glob
import json

def eliminate_all_jci():
    """彻底清除所有JCI表述"""
    
    print("=" * 80)
    print("全网站JCI表述最终清除行动")
    print("目标：零遗漏，全位置，绝对干净")
    print("=" * 80)
    print()
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    print(f"处理 {len(html_files)} 个HTML文件...")
    print()
    
    # 定义全面的修复规则
    fix_rules = [
        # 1. 中文内容中的JCI
        (r'JCI官网验证', 'ISO9001官网验证'),
        (r'JCI国际认证', 'ISO9001国际认证'),
        (r'JCI官网', 'ISO9001官网'),
        (r'JCI审核', 'ISO9001审核'),
        (r'JCI认证', 'ISO9001认证'),
        
        # 2. 英文内容中的JCI
        (r'\bJCI\b', 'ISO9001 Grade 3A'),
        (r'\bJCI-', 'ISO9001-'),
        (r'\bjci-', 'iso9001-'),
        (r'JCI\s+', 'ISO9001 '),
        (r'\s+JCI\s+', ' ISO9001 '),
        (r'JCI\.', 'ISO9001.'),
        (r'JCI,', 'ISO9001,'),
        (r'JCI\)', 'ISO9001)'),
        (r'\(JCI', '(ISO9001'),
        (r'JCI/', 'ISO9001/'),
        (r'/JCI', '/ISO9001'),
        (r'JCI:', 'ISO9001:'),
        (r':JCI', ':ISO9001'),
        
        # 3. JCI-accredited相关
        (r'JCI-accredited', 'ISO9001-certified Grade 3A'),
        (r'JCI accredited', 'ISO9001 certified Grade 3A'),
        (r'JCI-Accredited', 'ISO9001-Certified Grade 3A'),
        (r'JCI Accredited', 'ISO9001 Certified Grade 3A'),
        
        # 4. JCI hospitals相关
        (r'JCI hospitals', 'ISO9001-certified Grade 3A hospitals'),
        (r'JCI hospital', 'ISO9001-certified Grade 3A hospital'),
        (r'JCI Hospitals', 'ISO9001-Certified Grade 3A Hospitals'),
        (r'JCI Hospital', 'ISO9001-Certified Grade 3A Hospital'),
        
        # 5. 标题和meta标签
        (r'<title>[^<]*JCI[^<]*</title>', '<title>ISO9001-Certified Grade 3A Hospitals</title>'),
        (r'<meta[^>]*content="[^"]*JCI[^"]*"[^>]*>', '<meta content="ISO9001-certified Grade 3A hospitals">'),
        (r'description="[^"]*JCI[^"]*"', 'description="ISO9001-certified Grade 3A hospitals"'),
        
        # 6. JSON和JavaScript中的JCI
        (r'"JCI[^"]*"', '"ISO9001"'),
        (r"'JCI[^']*'", "'ISO9001'"),
        (r'JCI[^"]*"', 'ISO9001"'),
        (r'data-jci="[^"]*"', 'data-iso9001="true"'),
        
        # 7. 链接文本中的JCI
        (r'>JCI Hospitals<', '>ISO9001 Hospitals<'),
        (r'>JCI医院<', '>ISO9001医院<'),
        
        # 8. 属性中的JCI
        (r'[a-zA-Z-]*="[^"]*JCI[^"]*"', 'certification="ISO9001 Grade 3A"'),
        
        # 9. 注释中的JCI
        (r'<!--[^>]*JCI[^>]*-->', '<!-- ISO9001 Grade 3A Hospitals -->'),
        
        # 10. 最终清理：任何剩余的JCI（大小写不敏感）
        (r'[Jj][Cc][Ii]', 'ISO9001 Grade 3A'),
    ]
    
    total_fixed = 0
    total_files = 0
    files_fixed = []
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            original_jci_count = len(re.findall(r'[Jj][Cc][Ii]', content))
            
            if original_jci_count == 0:
                # print(f"✅ {filename}: 已经干净")
                continue
            
            # 应用所有修复规则
            for pattern, replacement in fix_rules:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # 额外处理：逐行清理
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                # 如果还有JCI，使用更激进的清理
                if 'jci' in line.lower():
                    # 替换所有变体
                    cleaned_line = re.sub(r'[Jj][Cc][Ii][^\s]*', 'ISO9001 Grade 3A', line)
                    cleaned_line = re.sub(r'[Jj][Cc][Ii]', 'ISO9001 Grade 3A', cleaned_line)
                    cleaned_lines.append(cleaned_line)
                else:
                    cleaned_lines.append(line)
            
            content = '\n'.join(cleaned_lines)
            
            # 最终检查
            final_jci_count = len(re.findall(r'[Jj][Cc][Ii]', content))
            fixed_count = original_jci_count - final_jci_count
            
            if fixed_count > 0:
                # 备份原文件
                backup_path = f"{file_path}.backup.final_elimination"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 保存修复后的文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                total_fixed += fixed_count
                total_files += 1
                files_fixed.append((filename, fixed_count, final_jci_count))
                
                print(f"✅ {filename}: 修复了 {fixed_count} 处JCI表述，剩余 {final_jci_count} 处")
                
        except Exception as e:
            print(f"❌ {filename}: 处理失败 - {e}")
    
    print()
    print("=" * 80)
    print("清除行动完成")
    print("=" * 80)
    print()
    
    print(f"📊 处理统计：")
    print(f"  处理文件数: {total_files}")
    print(f"  修复JCI表述数: {total_fixed}")
    print()
    
    if files_fixed:
        print("📋 已修复的文件列表：")
        files_fixed.sort(key=lambda x: x[1], reverse=True)
        
        for filename, fixed_count, remaining in files_fixed:
            status = "✅ 完全清除" if remaining == 0 else f"⚠️  剩余 {remaining} 处"
            print(f"  {filename}: 修复了 {fixed_count} 处，{status}")
    
    # 最终验证
    print()
    print("=" * 80)
    print("最终验证扫描")
    print("=" * 80)
    print()
    
    remaining_total = 0
    remaining_files = []
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            remaining = len(re.findall(r'[Jj][Cc][Ii]', content))
            if remaining > 0:
                remaining_total += remaining
                remaining_files.append((filename, remaining))
                
        except:
            continue
    
    if remaining_total == 0:
        print("🎉 恭喜！全网站JCI表述已彻底清除！")
        print("所有146个HTML文件都已完全干净。")
    else:
        print(f"⚠️  警告：还有 {remaining_total} 处JCI表述需要手动处理")
        print()
        print("📋 还有JCI的文件列表：")
        remaining_files.sort(key=lambda x: x[1], reverse=True)
        
        for filename, count in remaining_files:
            print(f"  {filename}: {count} 处")
        
        print()
        print("🛠️ 需要手动处理的文件建议：")
        print("1. 检查这些文件中的JCI是否在特殊位置（如二进制数据、加密内容）")
        print("2. 可能需要直接编辑文件，查找并替换")
        print("3. 考虑删除或重写这些文件")
    
    print()
    print("=" * 80)
    
    # 生成报告
    report = {
        'total_files': len(html_files),
        'files_fixed': total_files,
        'jci_fixed': total_fixed,
        'remaining_total': remaining_total,
        'remaining_files': [{'filename': f, 'count': c} for f, c in remaining_files],
        'timestamp': '2026-03-18 22:47'
    }
    
    with open('jci_elimination_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📄 详细报告已保存: jci_elimination_report.json")

if __name__ == "__main__":
    eliminate_all_jci()