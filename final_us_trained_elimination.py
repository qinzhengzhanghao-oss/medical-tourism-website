#!/usr/bin/env python3
"""
全网站'美国培训的牙医'表述最终清除脚本
确保零遗漏
"""

import os
import re
import glob

def eliminate_all_us_trained():
    """彻底清除所有'美国培训'相关表述"""
    
    print("=" * 80)
    print("全网站'美国培训的牙医'表述最终清除行动")
    print("目标：零遗漏，全位置，绝对干净")
    print("=" * 80)
    print()
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    print(f"处理 {len(html_files)} 个HTML文件...")
    print()
    
    # 定义全面的修复规则
    fix_rules = [
        # 1. 标题中的US-Trained
        (r'<title>[^<]*US-Trained[^<]*</title>', '<title>Experienced Dental Specialists Database | China Dental Tourism</title>'),
        (r'<title>[^<]*US Trained[^<]*</title>', '<title>Professional Dental Specialists Database | China Dental Tourism</title>'),
        
        # 2. meta标签中的US-trained
        (r'<meta[^>]*content="[^"]*us-trained[^"]*"[^>]*>', '<meta content="experienced-dental-specialists-china">'),
        (r'content="us-trained[^"]*"', 'content="experienced-dental-specialists"'),
        (r'description="[^"]*US-trained[^"]*"', 'description="Experienced dental specialists"'),
        
        # 3. 属性中的US-trained
        (r'data-ai-authority="us-trained[^"]*"', 'data-ai-authority="experienced-dental-specialists"'),
        (r'data-doctors="us-trained"', 'data-doctors="experienced-specialists"'),
        (r'data-verification="us-trained"', 'data-verification="professional-certification"'),
        (r'dental-specialists="us-trained"', 'dental-specialists="experienced"'),
        
        # 4. span标签中的US-trained
        (r'<span[^>]*>US-trained[^<]*</span>', '<span>Experienced Specialists</span>'),
        (r'<span[^>]*>US trained[^<]*</span>', '<span>Professional Specialists</span>'),
        (r'<span[^>]*>US-Trained[^<]*</span>', '<span>Experienced Specialists</span>'),
        
        # 5. strong标签中的US-Trained
        (r'<strong[^>]*>US-Trained[^<]*</strong>', '<strong>Experienced Specialist</strong>'),
        (r'<strong[^>]*>US trained[^<]*</strong>', '<strong>Professional Specialist</strong>'),
        
        # 6. 文本中的US-trained
        (r'\bUS-trained\b', 'experienced'),
        (r'\bUS trained\b', 'professional'),
        (r'\bUS-Trained\b', 'Experienced'),
        (r'\bUS Trained\b', 'Professional'),
        
        # 7. 特定短语
        (r'US-trained specialist', 'experienced specialist'),
        (r'US-trained specialists', 'experienced specialists'),
        (r'US-trained dental team', 'professional dental team'),
        (r'US-trained surgeons', 'experienced surgeons'),
        (r'US-trained medical staff', 'professional medical staff'),
        (r'US-trained implant specialists', 'experienced implant specialists'),
        (r'US-trained and/or board-certified', 'professionally certified'),
        (r'US-trained medical coordinators', 'professional medical coordinators'),
        (r'US-trained oral surgeon', 'experienced oral surgeon'),
        (r'US-trained medical directors', 'professional medical directors'),
        
        # 8. 中文表述
        (r'美国培训', '专业培训'),
        (r'美国训练', '专业训练'),
        
        # 9. 最终清理：任何剩余的US-trained（大小写不敏感）
        (r'[Uu][Ss]-[Tt]rained', 'experienced'),
        (r'[Uu][Ss] [Tt]rained', 'professional'),
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
            original_count = len(re.findall(r'[Uu][Ss]-[Tt]rained|[Uu][Ss] [Tt]rained|美国培训', content))
            
            if original_count == 0:
                # print(f"✅ {filename}: 已经干净")
                continue
            
            # 应用所有修复规则
            for pattern, replacement in fix_rules:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # 额外处理：逐行清理
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                # 如果还有US-trained，使用更激进的清理
                if re.search(r'[Uu][Ss]-[Tt]rained|[Uu][Ss] [Tt]rained', line, re.IGNORECASE):
                    # 替换所有变体
                    cleaned_line = re.sub(r'[Uu][Ss]-[Tt]rained[^\s]*', 'experienced', line, flags=re.IGNORECASE)
                    cleaned_line = re.sub(r'[Uu][Ss] [Tt]rained[^\s]*', 'professional', cleaned_line, flags=re.IGNORECASE)
                    cleaned_lines.append(cleaned_line)
                else:
                    cleaned_lines.append(line)
            
            content = '\n'.join(cleaned_lines)
            
            # 最终检查
            final_count = len(re.findall(r'[Uu][Ss]-[Tt]rained|[Uu][Ss] [Tt]rained|美国培训', content))
            fixed_count = original_count - final_count
            
            if fixed_count > 0:
                # 备份原文件
                backup_path = f"{file_path}.backup.final_us_trained_elimination"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 保存修复后的文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                total_fixed += fixed_count
                total_files += 1
                files_fixed.append((filename, fixed_count, final_count))
                
                print(f"✅ {filename}: 修复了 {fixed_count} 处表述，剩余 {final_count} 处")
                
        except Exception as e:
            print(f"❌ {filename}: 处理失败 - {e}")
    
    print()
    print("=" * 80)
    print("清除行动完成")
    print("=" * 80)
    print()
    
    print(f"📊 处理统计：")
    print(f"  处理文件数: {total_files}")
    print(f"  修复表述数: {total_fixed}")
    print()
    
    if files_fixed:
        print("📋 已修复的文件列表：")
        files_fixed.sort(key=lambda x: x[1], reverse=True)
        
        for filename, fixed_count, remaining in files_fixed[:20]:  # 显示前20个
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
            
            remaining = len(re.findall(r'[Uu][Ss]-[Tt]rained|[Uu][Ss] [Tt]rained|美国培训', content))
            if remaining > 0:
                remaining_total += remaining
                remaining_files.append((filename, remaining))
                
        except:
            continue
    
    if remaining_total == 0:
        print("🎉 恭喜！全网站'美国培训'相关表述已彻底清除！")
        print("所有146个HTML文件都已完全干净。")
    else:
        print(f"⚠️  警告：还有 {remaining_total} 处'美国培训'相关表述需要手动处理")
        print()
        print("📋 还有相关表述的文件列表：")
        remaining_files.sort(key=lambda x: x[1], reverse=True)
        
        for filename, count in remaining_files:
            print(f"  {filename}: {count} 处")
        
        print()
        print("🛠️ 需要手动处理的文件建议：")
        print("1. 检查这些文件中的表述是否在特殊位置")
        print("2. 可能需要直接编辑文件，查找并替换")
        print("3. 考虑使用更激进的替换策略")
    
    print()
    print("=" * 80)
    
    return remaining_total, remaining_files

if __name__ == "__main__":
    eliminate_all_us_trained()