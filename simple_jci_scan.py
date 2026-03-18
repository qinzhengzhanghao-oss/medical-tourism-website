#!/usr/bin/env python3
"""
全网站JCI表述彻底清查脚本（简化版）
"""

import os
import re
import glob

def scan_all_files():
    """扫描所有HTML文件中的JCI表述"""
    
    html_files = glob.glob("*.html")
    print(f"扫描 {len(html_files)} 个HTML文件...")
    print()
    
    total_jci = 0
    files_with_jci = []
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找所有JCI出现的位置
            jci_positions = []
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # 查找JCI（不区分大小写）
                matches = re.finditer(r'[Jj][Cc][Ii]', line)
                for match in matches:
                    # 获取上下文
                    start = max(0, match.start() - 20)
                    end = min(len(line), match.end() + 20)
                    context = line[start:end]
                    
                    # 确定位置类型
                    line_lower = line.lower()
                    pos = match.start()
                    
                    location_type = "正文"
                    if line_lower.startswith('<title'):
                        location_type = "标题"
                    elif '<meta' in line_lower and 'content=' in line_lower:
                        location_type = "meta标签"
                    elif 'footer' in line_lower or '底部' in line_lower:
                        location_type = "底部信息栏"
                    elif '<!--' in line_lower and '-->' in line_lower:
                        location_type = "注释"
                    elif '<script' in line_lower or '</script>' in line_lower:
                        location_type = "脚本"
                    elif '<style' in line_lower or '</style>' in line_lower:
                        location_type = "样式"
                    elif line_lower.startswith('<h'):
                        location_type = "标题标签"
                    
                    jci_positions.append({
                        'line': line_num,
                        'type': location_type,
                        'context': context.strip(),
                        'full_line': line.strip()[:80]
                    })
            
            if jci_positions:
                files_with_jci.append((filename, jci_positions))
                total_jci += len(jci_positions)
                print(f"❌ {filename}: {len(jci_positions)} 处JCI表述")
                
                # 显示前3个位置
                for i, pos in enumerate(jci_positions[:3]):
                    print(f"   行{pos['line']} [{pos['type']}]: {pos['context']}")
                if len(jci_positions) > 3:
                    print(f"   ... 还有 {len(jci_positions)-3} 处")
            else:
                print(f"✅ {filename}: 干净")
                
        except Exception as e:
            print(f"⚠️ {filename}: 扫描失败 - {e}")
    
    print()
    print("=" * 60)
    print("清查结果汇总")
    print("=" * 60)
    print()
    
    print(f"📊 统计信息：")
    print(f"  扫描文件数: {len(html_files)}")
    print(f"  发现JCI的文件数: {len(files_with_jci)}")
    print(f"  总JCI表述数: {total_jci}")
    print()
    
    if files_with_jci:
        print("📋 发现JCI的文件列表（按数量排序）：")
        files_with_jci.sort(key=lambda x: len(x[1]), reverse=True)
        
        for filename, positions in files_with_jci[:20]:  # 显示前20个
            print(f"  {filename}: {len(positions)} 处")
        
        print()
        print("🔍 JCI位置类型分布：")
        type_count = {}
        for filename, positions in files_with_jci:
            for pos in positions:
                type_count[pos['type']] = type_count.get(pos['type'], 0) + 1
        
        for type_name, count in sorted(type_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {type_name}: {count} 处")
        
        print()
        print("🚨 最严重的5个文件详情：")
        for i, (filename, positions) in enumerate(files_with_jci[:5]):
            print(f"\n{i+1}. {filename} ({len(positions)} 处):")
            for pos in positions[:5]:  # 每个文件显示前5个位置
                print(f"   行{pos['line']} [{pos['type']}]: {pos['context']}")
            if len(positions) > 5:
                print(f"   ... 还有 {len(positions)-5} 处")
    
    print()
    print("=" * 60)
    
    # 生成修复建议
    if files_with_jci:
        print("\n🛠️ 修复建议：")
        print("1. 创建最终清理脚本，处理所有位置的JCI")
        print("2. 特别注意以下位置类型：")
        for type_name in sorted(type_count.keys()):
            print(f"   - {type_name}")
        print("3. 运行清理后需要重新扫描验证")
    
    return files_with_jci, total_jci

if __name__ == "__main__":
    scan_all_files()
