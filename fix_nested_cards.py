#!/usr/bin/env python3
import re

with open('patient-testimonials.html', 'r') as f:
    content = f.read()

print("修复嵌套的白色卡片问题...")

# 查找并修复嵌套的testimonial-card
# 模式：一个testimonial-card内部包含另一个testimonial-card
pattern = r'<div class="testimonial-card">\s*<div class="testimonial-card">'

# 统计修复次数
fix_count = 0
while re.search(pattern, content):
    content = re.sub(pattern, '<div class="testimonial-card">', content, count=1)
    fix_count += 1

print(f"移除了 {fix_count} 个嵌套的testimonial-card")

# 修复案例17的特殊问题（之前已经部分修复）
# 移除可能的多余闭合标签
content = re.sub(r'</div>\s*</div>\s*<div class="testimonial-card">', '</div><div class="testimonial-card">', content)

# 确保每个案例只有一个testimonial-card
# 统计案例数量
case_count = len(re.findall(r'<!-- 案例\d+', content))
print(f"页面共有 {case_count} 个案例")

# 保存修复后的文件
with open('patient-testimonials.html', 'w') as f:
    f.write(content)

print("修复完成！")
print("现在每个案例应该只有一层白色卡片（testimonial-card）")