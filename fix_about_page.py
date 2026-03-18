#!/usr/bin/env python3
import re

# 读取原文件
with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 删除"Important Safety Information & Patient Responsibilities"部分
# 找到开始位置
start_pattern = r'<!-- OpenAI优化：安全性披露与患者责任 -->\s*<div class="mt-12 bg-red-50 border border-red-200 rounded-xl p-6 mb-8">'
end_pattern = r'</div>\s*</div>\s*</div>\s*</div>\s*<div class="mt-12 text-center">'

# 使用正则表达式删除这个部分
# 先找到开始位置
start_match = re.search(start_pattern, content, re.DOTALL)
if start_match:
    start_pos = start_match.start()
    # 从开始位置向后查找最近的</div></div></div></div>
    temp_content = content[start_pos:]
    # 查找连续的4个</div>标签
    div_pattern = r'</div>\s*</div>\s*</div>\s*</div>'
    div_match = re.search(div_pattern, temp_content, re.DOTALL)
    if div_match:
        end_pos = start_pos + div_match.end()
        # 删除这个部分
        content = content[:start_pos] + content[end_pos:]
        print("✅ 已删除安全信息部分")
    else:
        print("❌ 未找到安全信息部分的结束位置")
else:
    print("❌ 未找到安全信息部分")

# 2. 删除简单的底部信息栏（保留完整的footer）
# 查找 <div class="bg-gray-900 text-white py-8"> 到下一个 <footer 或 </body>
simple_footer_pattern = r'<div class="bg-gray-900 text-white py-8">.*?</div>\s*</div>\s*</div>'
simple_footer_match = re.search(simple_footer_pattern, content, re.DOTALL)
if simple_footer_match:
    content = content[:simple_footer_match.start()] + content[simple_footer_match.end():]
    print("✅ 已删除简单的底部信息栏")
else:
    print("❌ 未找到简单的底部信息栏")

# 保存修复后的文件
with open('about-fixed.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修复完成，已保存为 about-fixed.html")