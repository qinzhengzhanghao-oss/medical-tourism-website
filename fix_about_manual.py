#!/usr/bin/env python3

# 读取原始备份文件
with open('about-original.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到要删除的范围
start_delete = None  # 安全信息部分开始
end_delete = None    # 安全信息部分结束
simple_footer_start = None  # 简单底部信息栏开始
simple_footer_end = None    # 简单底部信息栏结束

# 查找安全信息部分
for i, line in enumerate(lines):
    if 'Important Safety Information & Patient Responsibilities' in line:
        # 向前找开始位置
        for j in range(i, max(0, i-20), -1):
            if '<!-- OpenAI优化：安全性披露与患者责任 -->' in lines[j]:
                start_delete = j
                break
        # 向后找结束位置
        for j in range(i, min(len(lines), i+100)):
            if '</div>' in lines[j] and '</div>' in lines[j+1] and '</div>' in lines[j+2] and '</div>' in lines[j+3]:
                end_delete = j + 4  # 包括4个</div>
                break
        break

# 查找简单底部信息栏
for i, line in enumerate(lines):
    if 'bg-gray-900 text-white py-8' in line:
        simple_footer_start = i
        # 向后找结束位置（找到包含</div></div></div>的行）
        for j in range(i, min(len(lines), i+20)):
            if '</div>' in lines[j] and '</div>' in lines[j+1] and '</div>' in lines[j+2]:
                simple_footer_end = j + 3
                break
        break

print(f"安全信息部分: {start_delete} - {end_delete}")
print(f"简单底部信息栏: {simple_footer_start} - {simple_footer_end}")

# 删除这些部分（从后往前删除，避免索引变化）
if simple_footer_end and simple_footer_start:
    del lines[simple_footer_start:simple_footer_end]
    print("✅ 已删除简单底部信息栏")

if end_delete and start_delete:
    del lines[start_delete:end_delete]
    print("✅ 已删除安全信息部分")

# 保存修复后的文件
with open('about-fixed-correct.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ 修复完成，已保存为 about-fixed-correct.html")