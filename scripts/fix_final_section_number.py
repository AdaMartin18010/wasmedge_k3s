#!/usr/bin/env python3
"""
修复所有案例文件的最后一个章节序号
"""
import re
from pathlib import Path

def fix_file(file_path):
    """修复单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找所有主标题，找到最大的序号
    main_titles = re.findall(r'^## (\d+)\.', content, re.MULTILINE)
    if not main_titles:
        return False

    max_num = max(int(n) for n in main_titles)

    # 修复更新记录章节的序号
    content = re.sub(
        r'^## (\d+)\.\s*📝\s*更新记录',
        f'## {max_num}. 📝 更新记录',
        content,
        flags=re.MULTILINE
    )

    # 修复目录中更新记录的序号
    # 查找目录中的更新记录链接（支持嵌套格式）
    # 匹配格式：  - [7. 📝 更新记录](#7-更新记录)
    toc_pattern = r'  - \[(\d+)\.\s*📝\s*更新记录\]\(#\d+-更新记录\)'
    replacement = f'  - [{max_num}. 📝 更新记录](#{max_num}-更新记录)'
    content = re.sub(toc_pattern, replacement, content)

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"已修复 {file_path}：更新记录章节序号为 {max_num}")
    return True

def main():
    """主函数"""
    cases_dir = Path(__file__).parent.parent / 'cases'

    # 获取所有案例文件
    case_files = [
        f for f in cases_dir.glob('*.md')
        if f.name not in ['README.md', 'case-template.md', 'CASE-PROGRESS-REPORT.md']
    ]

    print(f"找到 {len(case_files)} 个案例文件")

    processed = 0
    for case_file in sorted(case_files):
        if fix_file(case_file):
            processed += 1

    print(f"\n处理完成：{processed}/{len(case_files)} 个文件")

if __name__ == '__main__':
    main()
