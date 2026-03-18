#!/usr/bin/env python3
import re

# 读取文件
with open('doctor-credentials-verification.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找第一个底部信息栏的位置
pattern = r'(<footer class="main-footer">[\s\S]*?</footer>\s*</body>\s*</html>\s*)(<footer class="main-footer">[\s\S]*?</footer>\s*</body>\s*</html>\s*)'

match = re.search(pattern, content)
if match:
    print("找到两个底部信息栏")
    # 只保留第二个底部信息栏
    new_content = content.replace(match.group(1), '', 1)
    print("已删除第一个底部信息栏")
else:
    # 检查是否有其他格式的重复
    pattern2 = r'</html>\s*<footer class="main-footer">'
    if re.search(pattern2, content):
        print("找到在</html>标签后的底部信息栏")
        # 删除</html>标签前的所有footer
        parts = content.split('</html>')
        if len(parts) > 1:
            # 保留最后一个</html>标签后的内容
            new_content = parts[0].split('<footer class="main-footer">')[0] + '</html>' + parts[1]
            print("已删除多余的底部信息栏")
        else:
            new_content = content
            print("未找到重复的底部信息栏")
    else:
        new_content = content
        print("未找到重复的底部信息栏")

# 写入新文件
with open('doctor-credentials-verification-fixed.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("修复完成")
