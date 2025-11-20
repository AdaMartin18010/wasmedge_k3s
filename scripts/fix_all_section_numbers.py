#!/usr/bin/env python3
"""
修复所有案例文件的章节序号，确保"更新记录"是最后一个章节
"""
import re
from pathlib import Path

def fix_file(file_path):
    """修复单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找所有主标题，找到最大的序号
    # 排除"更新记录"章节，因为它应该是最后一个
    main_titles = []
    for match in re.finditer(r'^## (\d+)\.', content, re.MULTILINE):
        # 检查这一行是否包含"更新记录"
        line_start = match.start()
        line_end = content.find('\n', line_start)
        if line_end == -1:
            line_end = len(content)
        line = content[line_start:line_end]
        if '更新记录' not in line:
            main_titles.append(int(match.group(1)))

    if not main_titles:
        return False

    # 最大序号应该是"相关链接"章节的序号，更新记录应该是 max_num + 1
    max_num = max(main_titles) + 1

    # 如果"更新记录"章节的序号不是最大序号，需要修复
    # 检查"更新记录"章节的当前序号
    update_record_match = re.search(r'^## (\d+)\.\s*📝\s*更新记录', content, re.MULTILINE)
    if update_record_match:
        current_num = int(update_record_match.group(1))
        if current_num != max_num:
            # 修复章节标题
            content = re.sub(
                r'^## (\d+)\.\s*📝\s*更新记录',
                f'## {max_num}. 📝 更新记录',
                content,
                flags=re.MULTILINE
            )

            # 修复目录中的链接（支持嵌套格式）
            # 匹配格式：  - [7. 📝 更新记录](#7-更新记录)
            toc_pattern = r'  - \[(\d+)\.\s*📝\s*更新记录\]\(#\d+-更新记录\)'
            replacement = f'  - [{max_num}. 📝 更新记录](#{max_num}-更新记录)'
            content = re.sub(toc_pattern, replacement, content)

            print(f"已修复 {file_path}：更新记录章节序号从 {current_num} 改为 {max_num}")
        else:
            # 只修复目录中的链接（如果目录中的序号不对）
            toc_match = re.search(r'  - \[(\d+)\.\s*📝\s*更新记录\]\(#\d+-更新记录\)', content)
            if toc_match:
                toc_num = int(toc_match.group(1))
                if toc_num != max_num:
                    toc_pattern = r'  - \[(\d+)\.\s*📝\s*更新记录\]\(#\d+-更新记录\)'
                    replacement = f'  - [{max_num}. 📝 更新记录](#{max_num}-更新记录)'
                    content = re.sub(toc_pattern, replacement, content)
                    print(f"已修复 {file_path}：目录中更新记录链接序号从 {toc_num} 改为 {max_num}")

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

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
