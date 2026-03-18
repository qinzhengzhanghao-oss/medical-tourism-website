#!/usr/bin/env python3
"""
全网站US-trained表述终极清查脚本
检查每个文件的每个角落，确保零遗漏
"""

import os
import re
import glob
import html
from html.parser import HTMLParser

class UltimateUSTrainedScanner:
    """终极US-trained扫描器"""
    
    def __init__(self):
        self.total_files = 0
        self.files_with_us_trained = []
        self.total_us_trained_count = 0
        self.detailed_report = []
    
    def scan_file(self, file_path):
        """彻底扫描单个文件的所有US-trained表述"""
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查文件名本身
            file_name_matches = []
            if 'us-trained' in filename.lower() or 'us trained' in filename.lower():
                file_name_matches.append({
                    'type': 'filename',
                    'location': '文件名',
                    'content': filename,
                    'line': 0
                })
            
            # 检查文件内容
            content_matches = self._scan_content(content, filename)
            
            all_matches = file_name_matches + content_matches
            
            if all_matches:
                self.files_with_us_trained.append((filename, all_matches))
                self.total_us_trained_count += len(all_matches)
                
                # 添加到详细报告
                self.detailed_report.append({
                    'filename': filename,
                    'matches': all_matches,
                    'total': len(all_matches)
                })
                
                return True, len(all_matches)
            else:
                return False, 0
                
        except Exception as e:
            print(f"⚠️ {filename}: 扫描失败 - {e}")
            return False, 0
    
    def _scan_content(self, content, filename):
        """扫描文件内容中的所有US-trained表述"""
        matches = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            # 检查各种US-trained变体
            patterns = [
                (r'us-trained', 'US-trained'),
                (r'us trained', 'US trained'),
                (r'us\-trained', 'US-trained'),
                (r'u\.s\.-trained', 'U.S.-trained'),
                (r'u\.s\. trained', 'U.S. trained'),
                (r'american-trained', 'American-trained'),
                (r'american trained', 'American trained'),
                (r'usa-trained', 'USA-trained'),
                (r'usa trained', 'USA trained'),
            ]
            
            for pattern, display in patterns:
                pattern_regex = re.compile(pattern, re.IGNORECASE)
                pattern_matches = list(pattern_regex.finditer(line))
                
                for match in pattern_matches:
                    # 确定位置类型
                    location_type = self._determine_location_type(line, line_num, filename)
                    
                    # 获取上下文
                    start = max(0, match.start() - 30)
                    end = min(len(line), match.end() + 30)
                    context = line[start:end].strip()
                    
                    matches.append({
                        'type': 'content',
                        'location': location_type,
                        'pattern': display,
                        'content': context,
                        'full_line': line.strip()[:100],
                        'line': line_num
                    })
        
        return matches
    
    def _determine_location_type(self, line, line_num, filename):
        """确定US-trained所在的位置类型"""
        line_lower = line.lower()
        
        if line_lower.startswith('<title'):
            return 'title标签'
        elif '<meta' in line_lower and 'content=' in line_lower:
            return 'meta标签'
        elif '<script' in line_lower:
            return 'JavaScript代码'
        elif '<style' in line_lower:
            return 'CSS样式'
        elif '<!--' in line_lower and '-->' in line_lower:
            return 'HTML注释'
        elif 'href=' in line_lower or 'src=' in line_lower:
            return '链接/资源'
        elif 'class=' in line_lower or 'id=' in line_lower:
            return 'CSS类名/ID'
        elif 'data-' in line_lower:
            return '数据属性'
        elif line_lower.startswith('<h'):
            return '标题标签'
        elif line_lower.startswith('<p'):
            return '段落标签'
        elif line_lower.startswith('<div'):
            return 'div标签'
        elif line_lower.startswith('<span'):
            return 'span标签'
        elif line_lower.startswith('<a'):
            return '链接标签'
        elif line_lower.startswith('<li'):
            return '列表项'
        elif line_lower.startswith('<td') or line_lower.startswith('<th'):
            return '表格单元格'
        else:
            return '正文文本'
    
    def generate_report(self):
        """生成详细报告"""
        report = []
        
        report.append("=" * 100)
        report.append("全网站US-trained表述终极清查报告")
        report.append("=" * 100)
        report.append("")
        
        report.append(f"📊 统计信息：")
        report.append(f"  扫描文件总数: {self.total_files}")
        report.append(f"  发现US-trained的文件数: {len(self.files_with_us_trained)}")
        report.append(f"  US-trained表述总数: {self.total_us_trained_count}")
        report.append("")
        
        if self.files_with_us_trained:
            report.append("📋 发现US-trained的文件列表（按数量排序）：")
            self.files_with_us_trained.sort(key=lambda x: len(x[1]), reverse=True)
            
            for filename, matches in self.files_with_us_trained:
                report.append(f"  {filename}: {len(matches)} 处")
            
            report.append("")
            report.append("🔍 US-trained位置类型分布：")
            location_count = {}
            for filename, matches in self.files_with_us_trained:
                for match in matches:
                    loc_type = match.get('location', '未知')
                    location_count[loc_type] = location_count.get(loc_type, 0) + 1
            
            for loc_type, count in sorted(location_count.items(), key=lambda x: x[1], reverse=True):
                report.append(f"  {loc_type}: {count} 处")
            
            report.append("")
            report.append("🚨 最严重的10个文件详情：")
            for i, (filename, matches) in enumerate(self.files_with_us_trained[:10]):
                report.append(f"\n{i+1}. {filename} ({len(matches)} 处):")
                for j, match in enumerate(matches[:5]):  # 每个文件显示前5个
                    line_info = f"行{match['line']}" if match['line'] > 0 else ""
                    report.append(f"   [{match['location']}] {line_info}: {match['content'][:80]}...")
                if len(matches) > 5:
                    report.append(f"   ... 还有 {len(matches)-5} 处")
        
        else:
            report.append("🎉 恭喜！全网站没有发现任何US-trained表述！")
        
        report.append("")
        report.append("=" * 100)
        
        return "\n".join(report)
    
    def save_detailed_report(self, output_file):
        """保存详细报告到文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
        
        # 同时保存JSON格式的详细数据
        import json
        json_file = output_file.replace('.txt', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.detailed_report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 详细报告已保存: {output_file}")
        print(f"📄 JSON数据已保存: {json_file}")

def main():
    print("=" * 100)
    print("全网站US-trained表述终极清查行动")
    print("检查每个文件的每个角落，确保零遗漏")
    print("=" * 100)
    print()
    
    # 创建扫描器
    scanner = UltimateUSTrainedScanner()
    
    # 获取所有HTML文件
    html_files = glob.glob("*.html")
    scanner.total_files = len(html_files)
    
    print(f"扫描 {scanner.total_files} 个HTML文件...")
    print()
    
    # 扫描所有文件
    for file_path in html_files:
        filename = os.path.basename(file_path)
        print(f"扫描 {filename}...", end=' ')
        
        has_us_trained, count = scanner.scan_file(file_path)
        
        if has_us_trained:
            print(f"❌ 发现 {count} 处US-trained表述")
        else:
            print(f"✅ 干净")
    
    print()
    print("=" * 100)
    
    # 生成报告
    report = scanner.generate_report()
    print(report)
    
    # 保存详细报告
    scanner.save_detailed_report("ultimate_us_trained_scan_report.txt")
    
    # 如果有US-trained，提供修复建议
    if scanner.files_with_us_trained:
        print("\n🛠️ 修复建议：")
        print("1. 运行最终清理脚本: python3 final_us_trained_elimination.py")
        print("2. 手动检查特殊位置（JavaScript、CSS、注释等）")
        print("3. 检查文件名是否需要重命名")
        print("4. 重新扫描验证")
    
    return scanner.total_us_trained_count

if __name__ == "__main__":
    remaining_count = main()
    
    if remaining_count == 0:
        print("\n🎉 终极清查完成：全网站US-trained表述已彻底清除！")
    else:
        print(f"\n⚠️  警告：还有 {remaining_count} 处US-trained表述需要处理")
        print("请立即运行修复脚本或手动处理！")