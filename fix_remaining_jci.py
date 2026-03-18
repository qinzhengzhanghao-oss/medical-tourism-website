#!/usr/bin/env python3
"""
修复剩余JCI表述脚本
处理meta标签、标题、表格等复杂情况
"""

import os
import re
import glob

def fix_remaining_jci(file_path):
    """修复单个文件中的剩余JCI表述"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 修复meta描述中的JCI
        content = re.sub(
            r'(<meta[^>]*description[^>]*content="[^"]*)JCI[^"]*"',
            r'\1ISO9001-certified Grade 3A hospitals"',
            content,
            flags=re.IGNORECASE
        )
        
        # 2. 修复标题中的JCI
        content = re.sub(
            r'<h[1-6][^>]*>([^<]*)JCI([^<]*)</h[1-6]>',
            r'<h\1>ISO9001-Certified Grade 3A Hospitals</h\1>',
            content,
            flags=re.IGNORECASE
        )
        
        # 3. 修复表格中的JCI
        content = re.sub(
            r'<td[^>]*>([^<]*)JCI([^<]*)</td>',
            r'<td>ISO9001 Standards</td>',
            content,
            flags=re.IGNORECASE
        )
        
        # 4. 修复列表中的JCI
        content = re.sub(
            r'<li[^>]*>([^<]*)JCI([^<]*)</li>',
            r'<li>ISO9001 Quality System Certification</li>',
            content,
            flags=re.IGNORECASE
        )
        
        # 5. 修复div中的JCI
        content = re.sub(
            r'<div[^>]*>([^<]*)JCI([^<]*)</div>',
            r'<div>ISO9001 Certification</div>',
            content,
            flags=re.IGNORECASE
        )
        
        # 6. 修复段落中的JCI
        content = re.sub(
            r'<p[^>]*>([^<]*)JCI([^<]*)</p>',
            r'<p>ISO9001 Quality Management System</p>',
            content,
            flags=re.IGNORECASE
        )
        
        # 7. 修复span中的JCI
        content = re.sub(
            r'<span[^>]*>([^<]*)JCI([^<]*)</span>',
            r'<span>ISO9001</span>',
            content,
            flags=re.IGNORECASE
        )
        
        # 8. 修复属性中的JCI
        content = re.sub(
            r'([a-z-]+)="[^"]*JCI[^"]*"',
            r'\1="ISO9001 Grade 3A"',
            content,
            flags=re.IGNORECASE
        )
        
        # 9. 修复纯文本中的JCI（不在标签内）
        # 先标记所有HTML标签
        import html
        from html.parser import HTMLParser
        
        class JCIReplacer(HTMLParser):
            def __init__(self):
                super().__init__()
                self.result = []
                self.in_tag = False
                
            def handle_starttag(self, tag, attrs):
                self.in_tag = True
                attrs_str = ' '.join(f'{k}="{v}"' for k, v in attrs)
                if attrs_str:
                    self.result.append(f'<{tag} {attrs_str}>')
                else:
                    self.result.append(f'<{tag}>')
                    
            def handle_endtag(self, tag):
                self.in_tag = False
                self.result.append(f'</{tag}>')
                
            def handle_data(self, data):
                if not self.in_tag:
                    # 在文本中替换JCI
                    data = re.sub(r'\bJCI\b', 'ISO9001 Grade 3A', data, flags=re.IGNORECASE)
                    data = re.sub(r'\bJCI-accredited\b', 'ISO9001-certified Grade 3A', data, flags=re.IGNORECASE)
                    data = re.sub(r'\bJCI accreditation\b', 'ISO9001 quality system certification', data, flags=re.IGNORECASE)
                self.result.append(data)
                
            def get_result(self):
                return ''.join(self.result)
        
        # 使用HTML解析器处理
        parser = JCIReplacer()
        parser.feed(content)
        content = parser.get_result()
        parser.close()
        
        # 检查是否有修改
        if content != original_content:
            # 备份
            backup_path = f"{file_path}.backup.jci_phase2"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # 写入修改
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            changes = len(re.findall(r'JCI', original_content, re.IGNORECASE)) - len(re.findall(r'JCI', content, re.IGNORECASE))
            return True, changes
        else:
            return False, 0
            
    except Exception as e:
        print(f"错误处理文件 {file_path}: {e}")
        return False, 0

def main():
    print("=== 开始修复剩余JCI表述 ===")
    print("处理meta标签、标题、表格等复杂情况")
    print()
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    
    total_files = 0
    total_changes = 0
    files_with_jci = []
    
    print("扫描文件中的剩余JCI表述...")
    
    # 先扫描
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                jci_count = len(re.findall(r'JCI', content, re.IGNORECASE))
                if jci_count > 0:
                    files_with_jci.append((file_path, jci_count))
                    print(f"  {file_path}: {jci_count} 处JCI表述")
        except:
            continue
    
    print(f"\n总计: {len(files_with_jci)} 个文件还有JCI表述")
    print()
    
    # 批量修复
    print("开始批量修复...")
    for file_path, jci_count in files_with_jci:
        success, changes = fix_remaining_jci(file_path)
        if success:
            total_files += 1
            total_changes += changes
            print(f"  ✅ {file_path}: 修复了 {changes} 处表述")
        else:
            print(f"  ⚠️ {file_path}: 无修改或处理失败")
    
    print(f"\n=== 修复完成 ===")
    print(f"处理了 {total_files} 个文件")
    print(f"修复了 {total_changes} 处JCI表述")
    
    # 最终检查
    print("\n最终检查剩余JCI...")
    remaining_count = 0
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                jci_count = len(re.findall(r'JCI', content, re.IGNORECASE))
                if jci_count > 0:
                    remaining_count += jci_count
                    print(f"  ⚠️ {file_path}: 还有 {jci_count} 处JCI")
        except:
            continue
    
    print(f"\n剩余JCI表述总数: {remaining_count}")
    
    if remaining_count > 0:
        print("\n⚠️ 警告: 还有JCI表述未处理")
        print("可能需要手动检查以下类型:")
        print("1. JavaScript代码中的JCI")
        print("2. 注释中的JCI")
        print("3. 特殊格式的JCI")
    else:
        print("\n🎉 恭喜! 所有JCI表述已处理完成!")

if __name__ == "__main__":
    main()