#!/usr/bin/env python3
"""
全网站JCI表述彻底清查脚本
检查每个网页的每个位置，确保零遗漏
"""

import os
import re
import glob
import html
from html.parser import HTMLParser
from collections import defaultdict

class JCIDetector(HTMLParser):
    """HTML解析器，检测所有位置的JCI表述"""
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.jci_locations = []
        self.current_line = 1
        self.current_tag = None
        self.current_attrs = None
        self.in_script = False
        self.in_style = False
        self.in_comment = False
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        
        # 检查脚本和样式标签
        if tag.lower() == 'script':
            self.in_script = True
        if tag.lower() == 'style':
            self.in_style = True
            
        # 检查标签属性中的JCI
        for attr_name, attr_value in attrs:
            if attr_value and 'jci' in attr_value.lower():
                self.jci_locations.append({
                    'type': 'attribute',
                    'tag': tag,
                    'attribute': attr_name,
                    'value': attr_value,
                    'line': self.getpos()[0]
                })
    
    def handle_endtag(self, tag):
        if tag.lower() == 'script':
            self.in_script = False
        if tag.lower() == 'style':
            self.in_style = False
        self.current_tag = None
        self.current_attrs = None
    
    def handle_data(self, data):
        # 跳过脚本和样式内容（单独处理）
        if self.in_script or self.in_style:
            return
            
        # 检查文本中的JCI
        if 'jci' in data.lower():
            lines = data.split('\n')
            for i, line in enumerate(lines):
                if 'jci' in line.lower():
                    line_num = self.getpos()[0] - (len(lines) - i - 1)
                    self.jci_locations.append({
                        'type': 'text',
                        'tag': self.current_tag,
                        'content': line.strip()[:100],
                        'line': line_num,
                        'in_script': self.in_script,
                        'in_style': self.in_style
                    })
    
    def handle_comment(self, data):
        # 检查注释中的JCI
        if 'jci' in data.lower():
            self.jci_locations.append({
                'type': 'comment',
                'content': data.strip()[:100],
                'line': self.getpos()[0]
            })
    
    def handle_decl(self, data):
        # 检查声明中的JCI
        if 'jci' in data.lower():
            self.jci_locations.append({
                'type': 'declaration',
                'content': data.strip()[:100],
                'line': self.getpos()[0]
            })

def scan_file_for_jci(file_path):
    """彻底扫描单个文件的所有JCI表述"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用解析器检测
        parser = JCIDetector(os.path.basename(file_path))
        parser.feed(content)
        parser.close()
        
        # 同时使用正则表达式进行补充检测
        jci_patterns = [
            r'\bJCI\b',
            r'\bJCI-',
            r'\bjci-',
            r'JCI\s+',
            r'\s+JCI\s+',
            r'JCI\.',
            r'JCI,',
            r'JCI\)',
            r'\(JCI',
            r'JCI/',
            r'/JCI',
            r'JCI:',
            r':JCI',
        ]
        
        regex_matches = []
        for pattern in jci_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # 计算行号
                line_num = content[:match.start()].count('\n') + 1
                context_start = max(0, match.start() - 30)
                context_end = min(len(content), match.end() + 30)
                context = content[context_start:context_end].replace('\n', ' ')
                
                regex_matches.append({
                    'type': 'regex',
                    'pattern': pattern,
                    'match': match.group(),
                    'line': line_num,
                    'context': context
                })
        
        # 合并结果
        all_matches = parser.jci_locations + regex_matches
        
        # 去重（基于行号和内容）
        unique_matches = []
        seen = set()
        for match in all_matches:
            key = (match.get('line', 0), str(match.get('content', ''))[:50], match.get('type', ''))
            if key not in seen:
                seen.add(key)
                unique_matches.append(match)
        
        return unique_matches, len(content.split('\n'))
        
    except Exception as e:
        print(f"错误扫描文件 {file_path}: {e}")
        return [], 0

def generate_fix_script(jci_report):
    """根据检测报告生成修复脚本"""
    fix_script = """#!/usr/bin/env python3
'''
全网站JCI表述最终修复脚本
基于彻底清查结果生成
'''

import os
import re
import glob

def fix_all_jci():
    """修复所有检测到的JCI表述"""
    
    # 定义修复规则
    fix_rules = [
        # 1. 纯文本JCI
        (r'\\bJCI\\b', 'ISO9001 Grade 3A'),
        
        # 2. JCI-accredited
        (r'JCI-accredited', 'ISO9001-certified Grade 3A'),
        (r'JCI accredited', 'ISO9001 certified Grade 3A'),
        
        # 3. JCI认证
        (r'JCI认证', 'ISO9001质量体系认证'),
        (r'JCI certification', 'ISO9001 certification'),
        
        # 4. JCI标准
        (r'JCI standards', 'ISO9001 standards'),
        (r'JCI Standards', 'ISO9001 Standards'),
        
        # 5. JCI医院
        (r'JCI hospitals', 'ISO9001-certified Grade 3A hospitals'),
        (r'JCI hospital', 'ISO9001-certified Grade 3A hospital'),
        
        # 6. JCI检查
        (r'JCI inspection', 'ISO9001 audit'),
        (r'JCI Inspection', 'ISO9001 Audit'),
        
        # 7. 其他变体
        (r'JCI官网', 'ISO9001官网'),
        (r'JCI国际', 'ISO9001国际'),
        (r'JCI联合', 'ISO9001联合'),
        
        # 8. 属性中的JCI
        (r'content="[^"]*JCI[^"]*"', 'content="ISO9001-certified Grade 3A hospitals"'),
        (r'description="[^"]*JCI[^"]*"', 'description="ISO9001-certified Grade 3A hospitals"'),
        (r'title="[^"]*JCI[^"]*"', 'title="ISO9001 Grade 3A Hospitals"'),
        
        # 9. 注释中的JCI
        (r'<!--[^>]*JCI[^>]*-->', '<!-- ISO9001 Grade 3A Hospitals -->'),
        
        # 10. 脚本中的JCI
        (r'var.*JCI.*=', 'var hospitalCertification = "ISO9001 Grade 3A";'),
        (r'const.*JCI.*=', 'const hospitalStandard = "ISO9001 Grade 3A";'),
        (r'let.*JCI.*=', 'let certificationType = "ISO9001 Grade 3A";'),
    ]
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    
    total_fixed = 0
    total_files = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 应用所有修复规则
            for pattern, replacement in fix_rules:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # 额外处理：确保没有遗漏的JCI
            # 使用更激进的替换策略
            content = re.sub(r'[Jj][Cc][Ii]', 'ISO9001 Grade 3A', content)
            
            # 检查是否还有JCI
            remaining_jci = len(re.findall(r'[Jj][Cc][Ii]', content))
            
            if remaining_jci > 0:
                # 使用最终清理策略
                lines = content.split('\\n')
                cleaned_lines = []
                for line in lines:
                    cleaned_line = re.sub(r'[Jj][Cc][Ii][^\\s]*', 'ISO9001 Grade 3A', line)
                    cleaned_lines.append(cleaned_line)
                content = '\\n'.join(cleaned_lines)
            
            # 如果内容有变化，保存文件
            if content != original_content:
                # 备份
                backup_path = f"{file_path}.backup.final_jci_cleanup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 保存修复后的文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                changes = len(re.findall(r'[Jj][Cc][Ii]', original_content)) - len(re.findall(r'[Jj][Cc][Ii]', content))
                total_fixed += changes
                total_files += 1
                print(f"✅ {file_path}: 修复了 {changes} 处JCI表述")
                
        except Exception as e:
            print(f"❌ {file_path}: 修复失败 - {e}")
    
    print(f"\\n=== 最终修复完成 ===")
    print(f"处理了 {total_files} 个文件")
    print(f"修复了 {total_fixed} 处JCI表述")
    
    # 最终验证
    print("\\n=== 最终验证 ===")
    remaining_total = 0
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                remaining = len(re.findall(r'[Jj][Cc][Ii]', content))
                if remaining > 0:
                    print(f"⚠️  {file_path}: 还有 {remaining} 处JCI表述")
                    remaining_total += remaining
        except:
            continue
    
    if remaining_total == 0:
        print("🎉 恭喜！全网站JCI表述已彻底清除！")
    else:
        print(f"⚠️  警告：还有 {remaining_total} 处JCI表述需要手动处理")

if __name__ == "__main__":
    fix_all_jci()
"""
    
    return fix_script

def main():
    print("=" * 80)
    print("全网站JCI表述彻底清查行动")
    print("目标：零遗漏，全位置，绝对干净")
    print("=" * 80)
    print()
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    print(f"扫描 {len(html_files)} 个HTML文件...")
    print()
    
    # 扫描所有文件
    all_jci_locations = defaultdict(list)
    files_with_jci = []
    total_jci_count = 0
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        print(f"扫描 {filename}...")
        
        matches, total_lines = scan_file_for_jci(file_path)
        
        if matches:
            files_with_jci.append(filename)
            all_jci_locations[filename] = matches
            total_jci_count += len(matches)
            
            print(f"  ❌ 发现 {len(matches)} 处JCI表述")
            
            # 显示前3个位置
            for i, match in enumerate(matches[:3]):
                match_type = match.get('type', 'unknown')
                line_num = match.get('line', '?')
                content = match.get('content', match.get('context', '')).strip()[:60]
                print(f"    {i+1}. 行{line_num} [{match_type}]: {content}")
            if len(matches) > 3:
                print(f"    ... 还有 {len(matches)-3} 处")
        else:
            print(f"  ✅ 干净")
    
    print()
    print("=" * 80)
    print("清查结果汇总")
    print("=" * 80)
    print()
    
    print(f"📊 统计信息：")
    print(f"  扫描文件数: {len(html_files)}")
    print(f"  发现JCI的文件数: {len(files_with_jci)}")
    print(f"  总JCI表述数: {total_jci_count}")
    print()
    
    if files_with_jci:
        print("📋 发现JCI的文件列表：")
        for filename in sorted(files_with_jci):
            count = len(all_jci_locations[filename])
            print(f"  {filename}: {count} 处")
        
        print()
        print("🔍 JCI位置类型分布：")
        type_count = defaultdict(int)
        for filename, matches in all_jci_locations.items():
            for match in matches:
                type_count[match.get('type', 'unknown')] += 1
        
        for type_name, count in sorted(type_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {type_name}: {count} 处")
        
        print()
        print("🚨 最严重的文件：")
        sorted_files = sorted(all_jci_locations.items(), key=lambda x: len(x[1]), reverse=True)
        for filename, matches in sorted_files[:10]:
            print(f"  {filename}: {len(matches)} 处JCI表述")
        
        print()
        print("🛠️ 生成最终修复脚本...")
        fix_script = generate_fix_script(all_jci_locations)
        
        script_path = "final_jci_cleanup_script.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(fix_script)
        
        print(f"✅ 修复脚本已生成: {script_path}")
        print()
        print("📝 使用说明：")
        print(f"  1. 运行脚本: python3 {script_path}")
        print(f"  2. 脚本会自动备份所有文件（扩展名: .backup.final_jci_cleanup）")
        print(f"  3. 脚本会应用10种修复规则，确保彻底清除JCI")
        print(f"  4. 运行后会显示最终验证结果")
        
    else:
        print("🎉 恭喜！全网站没有发现任何JCI表述！")
    
    print()
    print("=" * 80)
    print("清查完成")
    print("=" * 80)

if __name__ == "__main__":
    main()