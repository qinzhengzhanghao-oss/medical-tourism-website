#!/usr/bin/env python3
"""
修复剩余的US-trained表述
"""

import re

def fix_remaining():
    file_path = "brand-professional-dental-hospital.html"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份
        backup_path = f"{file_path}.backup.remaining_fix"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 修复american-trained-dental-specialists
        fixed_content = re.sub(
            r'content="american-trained-dental-specialists"',
            'content="experienced-dental-specialists"',
            content,
            flags=re.IGNORECASE
        )
        
        # 修复其他可能的变体
        fixed_content = re.sub(
            r'american-trained',
            'experienced',
            fixed_content,
            flags=re.IGNORECASE
        )
        
        fixed_content = re.sub(
            r'american trained',
            'experienced',
            fixed_content,
            flags=re.IGNORECASE
        )
        
        fixed_content = re.sub(
            r'usa-trained',
            'experienced',
            fixed_content,
            flags=re.IGNORECASE
        )
        
        fixed_content = re.sub(
            r'usa trained',
            'experienced',
            fixed_content,
            flags=re.IGNORECASE
        )
        
        fixed_content = re.sub(
            r'u\.s\.-trained',
            'experienced',
            fixed_content,
            flags=re.IGNORECASE
        )
        
        fixed_content = re.sub(
            r'u\.s\. trained',
            'experienced',
            fixed_content,
            flags=re.IGNORECASE
        )
        
        # 保存修复后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ {file_path}: 已修复遗漏的US-trained表述")
        
        # 验证
        remaining = len(re.findall(r'american-trained|us-trained|us trained|usa-trained|u\.s\.-trained', fixed_content, re.IGNORECASE))
        print(f"剩余US-trained表述: {remaining}")
        
        return remaining == 0
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

if __name__ == "__main__":
    success = fix_remaining()
    if success:
        print("🎉 所有US-trained表述已彻底清除！")
    else:
        print("⚠️ 还有US-trained表述需要处理")