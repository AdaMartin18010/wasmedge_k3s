#!/usr/bin/env python3
"""
将所有案例文件的目录格式统一为详细嵌套格式
"""
import re
from pathlib import Path

def create_anchor(text):
    """创建锚点"""
    # 移除emoji和特殊字符
    anchor = re.sub(r'[📋📝🏗️📊🚀💡📚📑]', '', text)
    anchor = anchor.strip()
    # 转换为小写，替换空格为连字符
    anchor = anchor.lower().replace(' ', '-')
    # 移除特殊字符
    anchor = re.sub(r'[^\w\-]', '', anchor)
    # 移除序号前缀（如 "1. " 或 "2.1 "）
    anchor = re.sub(r'^\d+\.?\d*\s*', '', anchor)
    return anchor

def extract_title_and_sections(content):
    """提取标题和所有章节"""
    lines = content.split('\n')

    # 提取主标题
    main_title = None
    for line in lines[:10]:
        if line.startswith('# '):
            main_title = line[2:].strip()
            break

    sections = []
    for line in lines:
        # 主标题
        if line.startswith('## '):
            title = line[3:].strip()
            # 跳过目录标题
            if '📑' in title or '目录' in title:
                continue
            # 提取序号
            match = re.match(r'^(\d+)\.\s*(.+)', title)
            if match:
                num = int(match.group(1))
                title_text = match.group(2).strip()
                anchor = create_anchor(title_text)
                sections.append((1, num, title_text, f"{num}-{anchor}"))
        # 子标题
        elif line.startswith('### '):
            title = line[4:].strip()
            # 提取序号
            match = re.match(r'^(\d+)\.(\d+)\s*(.+)', title)
            if match:
                main_num = int(match.group(1))
                sub_num = int(match.group(2))
                title_text = match.group(3).strip()
                anchor = create_anchor(title_text)
                sections.append((2, main_num, sub_num, title_text, f"{main_num}{sub_num}-{anchor}"))

    return main_title, sections

def generate_detailed_toc(main_title, sections):
    """生成详细嵌套目录"""
    if not main_title:
        main_title = "案例文档"

    main_title_anchor = create_anchor(main_title)

    toc = ["## 📑 目录", ""]
    toc.append(f"- [{main_title}](#{main_title_anchor})")
    toc.append(f"  - [📑 目录](#-目录)")

    current_main = 0
    for section in sections:
        if section[0] == 1:  # 主标题
            main_num, title, anchor = section[1], section[2], section[3]
            toc.append(f"  - [{main_num}. {title}](#{anchor})")
            current_main = main_num
        elif section[0] == 2:  # 子标题
            main_num, sub_num, title, anchor = section[1], section[2], section[3], section[4]
            if main_num == current_main:
                toc.append(f"    - [{main_num}.{sub_num} {title}](#{anchor})")
            else:
                toc.append(f"  - [{main_num}.{sub_num} {title}](#{anchor})")
                current_main = main_num

    return "\n".join(toc) + "\n\n---\n\n"

def update_file(file_path):
    """更新单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取标题和章节
    main_title, sections = extract_title_and_sections(content)

    if not sections:
        print(f"跳过 {file_path}：未找到章节")
        return False

    # 生成新目录
    new_toc = generate_detailed_toc(main_title, sections)

    # 替换现有目录
    # 查找目录开始和结束位置
    toc_pattern = r'## 📑 目录.*?---\s*\n'
    if re.search(toc_pattern, content, re.DOTALL):
        content = re.sub(toc_pattern, new_toc, content, flags=re.DOTALL)
    else:
        # 如果没有目录，在基本信息后插入
        pattern = r'(收集日期.*?\n\n)---\n'
        replacement = r'\1---\n' + new_toc
        content = re.sub(pattern, replacement, content)

    # 确保目录在基本信息之前
    # 如果目录在基本信息之后，移动到前面
    if '## 📑 目录' in content and '## 1. 📋 案例基本信息' in content:
        toc_match = re.search(r'## 📑 目录.*?---\s*\n', content, re.DOTALL)
        basic_info_match = re.search(r'## 1\. 📋 案例基本信息', content)

        if toc_match and basic_info_match:
            toc_start = toc_match.start()
            toc_end = toc_match.end()
            basic_info_start = basic_info_match.start()

            # 如果目录在基本信息之后，需要移动
            if toc_start > basic_info_start:
                toc_content = content[toc_start:toc_end]
                # 移除旧目录
                content = content[:toc_start] + content[toc_end:]
                # 在基本信息前插入
                basic_info_pos = content.find('## 1. 📋 案例基本信息')
                if basic_info_pos > 0:
                    # 找到前面的 ---
                    prev_sep = content.rfind('---', 0, basic_info_pos)
                    if prev_sep > 0:
                        insert_pos = prev_sep + 3  # 在 --- 之后
                        content = content[:insert_pos] + '\n\n' + toc_content + content[insert_pos:]

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"已更新 {file_path}")
    return True

def main():
    """主函数"""
    cases_dir = Path(__file__).parent.parent / 'cases'

    # 获取所有案例文件（排除已更新的文件）
    case_files = [
        f for f in cases_dir.glob('*.md')
        if f.name not in ['README.md', 'case-template.md', 'CASE-PROGRESS-REPORT.md',
                          'finance-trading-system.md']  # 跳过已更新的文件
    ]

    print(f"找到 {len(case_files)} 个案例文件需要更新")

    processed = 0
    for case_file in sorted(case_files):
        if update_file(case_file):
            processed += 1

    print(f"\n处理完成：{processed}/{len(case_files)} 个文件")

if __name__ == '__main__':
    main()
