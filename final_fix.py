#!/usr/bin/env python3
import re

# 读取文件
with open('doctor-credentials-verification.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到第一个</html>标签的位置
html_end_index = -1
for i, line in enumerate(lines):
    if '</html>' in line:
        html_end_index = i
        break

if html_end_index != -1:
    print(f"找到</html>标签在第 {html_end_index+1} 行")
    # 只保留到</html>标签（包含该标签）
    clean_lines = lines[:html_end_index+1]
else:
    print("未找到</html>标签，使用所有行")
    clean_lines = lines

# 写入清理后的内容
with open('doctor-clean.html', 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)

print("文件清理完成")

# 现在添加标准底部信息栏
with open('doctor-clean.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 删除可能存在的旧底部信息栏
content = re.sub(r'<footer class="main-footer">[\s\S]*?</footer>', '', content)

# 确保</body></html>在正确位置
if '</body>' not in content:
    content = content.replace('</html>', '</body></html>')
elif '</body></html>' not in content:
    content = content.replace('</body>', '').replace('</html>', '')

# 添加标准底部信息栏
with open('standard_footer.html', 'r', encoding='utf-8') as f:
    standard_footer = f.read()

final_content = content.replace('</body></html>', standard_footer)

with open('doctor-credentials-verification-final.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("标准底部信息栏已添加")