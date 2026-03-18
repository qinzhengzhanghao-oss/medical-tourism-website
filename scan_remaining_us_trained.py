#!/usr/bin/env python3
"""
扫描剩余'美国培训'相关表述
"""

import os
import re
import glob

def scan_remaining():
    html_files = glob.glob("*.html")
    
    total_remaining = 0
    files_with_remaining = []
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找所有剩余的相关表述
            patterns = [
                r'us-trained',
                r'美国培训',
                r'US trained',
                r'US-trained',
                r'US培训',
                r'美国训练'
            ]
            
            positions = []
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # 获取上下文
                        start = max(0, line.lower().find('us-trained') - 20)
                        end = min(len(line), line.lower().find('us-trained') + 50)
                        if start < end:
                            context = line[start:end]
                            
                            positions.append({
                                'line': line_num,
                                'pattern': pattern,
                                'context': context.strip(),
                                'full_line': line.strip()[:80]
                            })
                        break
            
            if positions:
                files_with_remaining.append((filename, positions))
                total_remaining += len(positions)
                print(f"❌ {filename}: {len(positions)} 处剩余表述")
                
                # 显示前3个位置
                for i, pos in enumerate(positions[:3]):
                    print(f"   行{pos['line']}: {pos['context']}")
                if len(positions) > 3:
                    print(f"   ... 还有 {len(positions)-3} 处")
                
        except Exception as e:
            print(f"⚠️ {filename}: 扫描失败 - {e}")
    
    print(f"\n总计剩余: {total_remaining} 处'美国培训'相关表述")
    print(f"涉及文件: {len(files_with_remaining)} 个")
    
    if files_with_remaining:
        print("\n📋 剩余表述最多的文件：")
        files_with_remaining.sort(key=lambda x: len(x[1]), reverse=True)
        
        for filename, positions in files_with_remaining[:10]:
            print(f"  {filename}: {len(positions)} 处")
    
    return total_remaining, files_with_remaining

if __name__ == "__main__":
    scan_remaining()
