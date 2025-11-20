#!/usr/bin/env python3
"""
修复"技术栈"章节的锚点链接格式
"""
import re
from pathlib import Path

def fix_file(file_path):
    """修复单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 修复技术栈的锚点链接
    # 从 #3-️-技术栈 或 #3-技术栈 改为 #3-技术栈（单连字符，因为 emoji 后面有空格但会被移除）
    # 实际上，Markdown 生成锚点时，emoji 会被移除，空格变成连字符
    # 所以 "3. 🏗️ 技术栈" 应该生成 "#3-技术栈"

    # 修复格式：从 #3-️-技术栈 改为 #3-技术栈
    content = re.sub(r'\(#(\d+)-️-技术栈\)', r'(#\1-技术栈)', content)

    # 如果内容有变化，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已修复 {file_path}")
        return True
    else:
        print(f"跳过 {file_path}：格式已正确")
        return False

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
