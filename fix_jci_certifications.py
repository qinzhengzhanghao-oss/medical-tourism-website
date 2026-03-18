#!/usr/bin/env python3
"""
批量修复JCI认证表述脚本
将"JCI认证"替换为"ISO9001质量体系认证"和"国家评定的三级甲等医院"
"""

import os
import re
import glob
from pathlib import Path

def fix_jci_certifications(file_path):
    """修复单个文件中的JCI认证表述"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 记录原始内容长度
        original_length = len(content)
        
        # 定义替换规则
        replacements = [
            # 1. JCI认证的医院 → ISO9001认证的医院
            (r'JCI-accredited hospitals', 'ISO9001-certified hospitals'),
            (r'JCI-accredited hospital', 'ISO9001-certified hospital'),
            (r'JCI accredited hospitals', 'ISO9001 certified hospitals'),
            (r'JCI accredited hospital', 'ISO9001 certified hospital'),
            (r'JCI-certified hospitals', 'ISO9001-certified hospitals'),
            (r'JCI-certified hospital', 'ISO9001-certified hospital'),
            (r'JCI certified hospitals', 'ISO9001 certified hospitals'),
            (r'JCI certified hospital', 'ISO9001 certified hospital'),
            
            # 2. JCI认证 → ISO9001质量体系认证
            (r'JCI accreditation', 'ISO9001 quality system certification'),
            (r'JCI Accreditation', 'ISO9001 Quality System Certification'),
            (r'JCI认证', 'ISO9001质量体系认证'),
            
            # 3. 国际JCI标准 → 国际ISO9001标准
            (r'international JCI standards', 'international ISO9001 standards'),
            (r'JCI standards', 'ISO9001 standards'),
            (r'JCI Standards', 'ISO9001 Standards'),
            
            # 4. JCI检查 → ISO9001审核
            (r'JCI inspection', 'ISO9001 audit'),
            (r'JCI Inspection', 'ISO9001 Audit'),
            
            # 5. 添加三级甲等医院表述
            (r'ISO9001-certified hospitals', 'ISO9001-certified Grade 3A hospitals'),
            (r'ISO9001 certified hospitals', 'ISO9001 certified Grade 3A hospitals'),
            (r'ISO9001-certified hospital', 'ISO9001-certified Grade 3A hospital'),
            (r'ISO9001 certified hospital', 'ISO9001 certified Grade 3A hospital'),
            
            # 6. 特定短语替换
            (r'with JCI accreditation', 'with ISO9001 certification and Grade 3A hospital status'),
            (r'JCI-accredited,', 'ISO9001-certified Grade 3A,'),
            (r'JCI accredited,', 'ISO9001 certified Grade 3A,'),
            
            # 7. 描述性替换
            (r'JCI \(Joint Commission International\)', 'ISO9001 Quality Management System'),
            (r'the Joint Commission International', 'the ISO9001 Quality Management System'),
        ]
        
        # 应用所有替换规则
        modified_content = content
        for pattern, replacement in replacements:
            modified_content = re.sub(pattern, replacement, modified_content, flags=re.IGNORECASE)
        
        # 添加额外的三级甲等医院说明（在相关段落后）
        hospital_patterns = [
            r'(ISO9001[^<]*hospital[^<]*</p>)',
            r'(ISO9001[^<]*hospitals[^<]*</p>)',
            r'(Grade 3A[^<]*</p>)'
        ]
        
        for pattern in hospital_patterns:
            matches = re.findall(pattern, modified_content, re.IGNORECASE)
            for match in matches:
                if 'Grade 3A' not in match and '三级甲等' not in match:
                    # 在段落后添加说明
                    additional_info = ' (Grade 3A is the highest hospital classification in China)'
                    modified_content = modified_content.replace(match, match + additional_info)
        
        # 检查是否有修改
        if modified_content != content:
            # 备份原文件
            backup_path = f"{file_path}.backup.jci_fix"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 写入修改后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            changes = len(re.findall(r'JCI', content, re.IGNORECASE)) - len(re.findall(r'JCI', modified_content, re.IGNORECASE))
            return True, changes, original_length, len(modified_content)
        else:
            return False, 0, original_length, len(modified_content)
            
    except Exception as e:
        print(f"错误处理文件 {file_path}: {e}")
        return False, 0, 0, 0

def main():
    print("=== 开始批量修复JCI认证表述 ===")
    print("将'JCI认证'替换为'ISO9001质量体系认证'和'国家评定的三级甲等医院'")
    print()
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    
    total_files = 0
    total_changes = 0
    total_original_jci = 0
    
    print("扫描文件中的JCI表述...")
    
    # 先统计
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                jci_count = len(re.findall(r'JCI', content, re.IGNORECASE))
                if jci_count > 0:
                    total_original_jci += jci_count
                    print(f"  {file_path}: {jci_count} 处JCI表述")
        except:
            continue
    
    print(f"\n总计: {len(html_files)} 个HTML文件，{total_original_jci} 处JCI表述需要修改")
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
                if 'JCI' in content.upper():
                    success, changes, orig_len, new_len = fix_jci_certifications(file_path)
                    if success:
                        total_files += 1
                        total_changes += changes
                        print(f"  ✅ {file_path}: 修改了 {changes} 处表述")
        except Exception as e:
            print(f"  ❌ {file_path}: 处理失败 - {e}")
    
    print(f"\n=== 批量修改完成 ===")
    print(f"修改了 {total_files} 个文件")
    print(f"替换了 {total_changes} 处JCI表述")
    print(f"剩余JCI表述: {total_original_jci - total_changes}")
    print("\n重要提醒:")
    print("1. 所有修改的文件都有备份，扩展名为 .backup.jci_fix")
    print("2. 请仔细检查修改结果，确保表述准确")
    print("3. 主要替换为: 'ISO9001质量体系认证' 和 '国家评定的三级甲等医院'")
    print("4. Grade 3A 是中国最高级别的医院评定")

if __name__ == "__main__":
    main()