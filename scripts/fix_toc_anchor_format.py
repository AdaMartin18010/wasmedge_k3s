#!/usr/bin/env python3
"""
统一所有案例文件的目录锚点链接格式为双连字符格式
"""
import re
from pathlib import Path

def fix_anchor_format(content):
    """修复锚点链接格式"""
    # 修复主章节的锚点链接（带 emoji 的章节）
    # 格式：从 #1-案例基本信息 改为 #1--案例基本信息
    patterns = [
        # 主章节：1. 📋 案例基本信息 -> #1--案例基本信息
        (r'\(#(\d+)-案例基本信息\)', r'(#\1--案例基本信息)'),
        (r'\(#(\d+)-案例描述\)', r'(#\1--案例描述)'),
        (r'\(#(\d+)-技术栈\)', r'(#\1-技术栈)'),  # 技术栈的 emoji 后面没有空格，所以保持单连字符
        (r'\(#(\d+)-关键指标\)', r'(#\1--关键指标)'),
        (r'\(#(\d+)-实施步骤\)', r'(#\1--实施步骤)'),
        (r'\(#(\d+)-经验总结\)', r'(#\1--经验总结)'),
        (r'\(#(\d+)-相关链接\)', r'(#\1--相关链接)'),
        (r'\(#(\d+)-更新记录\)', r'(#\1--更新记录)'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    return content

def fix_file(file_path):
    """修复单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 修复锚点链接格式
    content = fix_anchor_format(content)

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
