#!/usr/bin/env python3
"""
批量修复'美国培训的牙医'表述脚本
将"美国培训的牙医"替换为"行业资深牙科专家"
"""

import os
import re
import glob

def fix_us_trained_dentists(file_path):
    """修复单个文件中的'美国培训的牙医'表述"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 定义替换规则
        replacements = [
            # 1. US-trained dentists → Industry-experienced dental specialists
            (r'US-trained dentists', 'Industry-experienced dental specialists'),
            (r'US trained dentists', 'Industry experienced dental specialists'),
            (r'US-trained dentist', 'Industry-experienced dental specialist'),
            (r'US trained dentist', 'Industry experienced dental specialist'),
            
            # 2. US-trained dental specialists → Experienced dental specialists
            (r'US-trained dental specialists', 'Experienced dental specialists'),
            (r'US trained dental specialists', 'Experienced dental specialists'),
            
            # 3. US-trained doctors → Seasoned dental experts
            (r'US-trained doctors', 'Seasoned dental experts'),
            (r'US trained doctors', 'Seasoned dental experts'),
            
            # 4. US-trained medical team → Professional dental team
            (r'US-trained medical team', 'Professional dental team'),
            (r'US trained medical team', 'Professional dental team'),
            
            # 5. 美国培训的牙医 → 行业资深牙科专家
            (r'美国培训的牙医', '行业资深牙科专家'),
            (r'美国培训牙医', '行业资深牙科专家'),
            (r'美国培训医生', '行业资深牙科专家'),
            
            # 6. 美国训练 → 专业训练
            (r'美国训练', '专业训练'),
            (r'美国培训', '专业培训'),
            
            # 7. US education/training → Professional education/training
            (r'US education', 'Professional education'),
            (r'US training', 'Professional training'),
            (r'US-educated', 'Professionally-educated'),
            
            # 8. 特定短语替换
            (r'with US training', 'with extensive professional training'),
            (r'US-trained,', 'Professionally-trained,'),
            (r'US trained,', 'Professionally trained,'),
            
            # 9. 描述性替换
            (r'US-trained and certified', 'Professionally-trained and certified'),
            (r'US trained and certified', 'Professionally trained and certified'),
            (r'US-trained professionals', 'Professional dental experts'),
            (r'US trained professionals', 'Professional dental experts'),
            
            # 10. 文件特定替换
            (r'us-trained-dentists-china\.html', 'experienced-dental-specialists-china.html'),
            (r'US-Trained Dentists', 'Experienced Dental Specialists'),
            (r'US Trained Dentists', 'Experienced Dental Specialists'),
        ]
        
        # 应用所有替换规则
        modified_content = content
        for pattern, replacement in replacements:
            modified_content = re.sub(pattern, replacement, modified_content, flags=re.IGNORECASE)
        
        # 添加额外的专业资质说明（在相关段落后）
        expertise_patterns = [
            r'(Industry-experienced[^<]*specialists[^<]*</p>)',
            r'(Experienced dental[^<]*</p>)',
            r'(Seasoned dental[^<]*</p>)',
            r'(行业资深牙科专家[^<]*</p>)'
        ]
        
        for pattern in expertise_patterns:
            matches = re.findall(pattern, modified_content, re.IGNORECASE)
            for match in matches:
                if 'extensive experience' not in match and 'professional certification' not in match:
                    # 在段落后添加说明
                    additional_info = ' with extensive clinical experience and professional certification'
                    modified_content = modified_content.replace(match, match + additional_info)
        
        # 检查是否有修改
        if modified_content != content:
            # 备份原文件
            backup_path = f"{file_path}.backup.us_trained_fix"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 写入修改后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            # 计算修改数量
            original_count = len(re.findall(r'us-trained|美国培训|US trained', content, re.IGNORECASE))
            modified_count = len(re.findall(r'us-trained|美国培训|US trained', modified_content, re.IGNORECASE))
            changes = original_count - modified_count
            
            return True, changes, len(content), len(modified_content)
        else:
            return False, 0, len(content), len(modified_content)
            
    except Exception as e:
        print(f"错误处理文件 {file_path}: {e}")
        return False, 0, 0, 0

def main():
    print("=== 开始批量修复'美国培训的牙医'表述 ===")
    print("将'美国培训的牙医'替换为'行业资深牙科专家'")
    print()
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    
    total_files = 0
    total_changes = 0
    total_original = 0
    
    print("扫描文件中的'美国培训'相关表述...")
    
    # 先统计
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                count = len(re.findall(r'us-trained|美国培训|US trained', content, re.IGNORECASE))
                if count > 0:
                    total_original += count
                    print(f"  {os.path.basename(file_path)}: {count} 处相关表述")
        except:
            continue
    
    print(f"\n总计: {len(html_files)} 个HTML文件，{total_original} 处'美国培训'相关表述需要修改")
    print()
    
    # 确认是否继续
    response = input("是否开始批量修改？(yes/no): ")
    if response.lower() != 'yes':
        print("操作已取消")
        return
    
    print("\n开始批量修改...")
    
    # 批量修改
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(r'us-trained|美国培训|US trained', content, re.IGNORECASE):
                    success, changes, orig_len, new_len = fix_us_trained_dentists(file_path)
                    if success:
                        total_files += 1
                        total_changes += changes
                        print(f"  ✅ {os.path.basename(file_path)}: 修改了 {changes} 处表述")
        except Exception as e:
            print(f"  ❌ {os.path.basename(file_path)}: 处理失败 - {e}")
    
    print(f"\n=== 批量修改完成 ===")
    print(f"修改了 {total_files} 个文件")
    print(f"替换了 {total_changes} 处'美国培训'相关表述")
    print(f"剩余相关表述: {total_original - total_changes}")
    print("\n重要提醒:")
    print("1. 所有修改的文件都有备份，扩展名为 .backup.us_trained_fix")
    print("2. 请仔细检查修改结果，确保表述准确")
    print("3. 主要替换为: '行业资深牙科专家' 和 'Industry-experienced dental specialists'")
    print("4. 需要重命名的文件: us-trained-dentists-china.html → experienced-dental-specialists-china.html")

if __name__ == "__main__":
    main()