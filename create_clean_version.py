#!/usr/bin/env python3
import re

# 读取备份文件
with open('doctor-credentials-verification.html.backup.20260318_163143', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 删除所有中文内容
# 找到"医生具体资质信息"的位置
chinese_start = content.find('医生具体资质信息')
if chinese_start != -1:
    # 找到下一个主要英文部分开始的位置
    # 查找"</section>"后的下一个"<section"或"<footer"
    section_end = content.find('</section>', chinese_start)
    if section_end != -1:
        # 删除从chinese_start到section_end+9的内容
        content = content[:chinese_start] + content[section_end+9:]
        print("已删除中文内容部分")
    else:
        # 如果找不到</section>，删除从chinese_start到文件结尾
        content = content[:chinese_start]
        print("已删除从中文内容开始到文件结尾")

# 2. 删除多余的底部信息栏
# 查找第一个底部信息栏
footer_pattern = r'<footer[^>]*>[\s\S]*?</footer>'
footers = list(re.finditer(footer_pattern, content))

if len(footers) > 1:
    print(f"找到 {len(footers)} 个底部信息栏")
    # 只保留最后一个
    for i in range(len(footers)-1):
        content = content.replace(footers[i].group(0), '', 1)
    print("已删除多余的底部信息栏，只保留最后一个")
elif len(footers) == 1:
    print("找到 1 个底部信息栏")
else:
    print("未找到底部信息栏")

# 3. 确保文件以正确的HTML结构结束
if not content.strip().endswith('</html>'):
    # 添加缺失的结束标签
    content = content.rstrip() + '\n</body>\n</html>'
    print("已添加缺失的HTML结束标签")

# 写入新文件
with open('doctor-credentials-verification-clean.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("干净版本创建完成")