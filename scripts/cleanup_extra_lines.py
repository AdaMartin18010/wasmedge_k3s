#!/usr/bin/env python3
"""
清理文件中的多余空行
"""
import re
from pathlib import Path

def cleanup_file(file_path):
    """清理单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换多个连续空行为两个空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # 替换目录后的多余空行
    content = re.sub(r'(---\n\n## 📑 目录.*?---)\n{3,}', r'\1\n\n', content, flags=re.DOTALL)

    # 替换目录和基本信息之间的多余空行
    content = re.sub(r'(---\n\n)\n+## 1\. 📋 案例基本信息', r'\1## 1. 📋 案例基本信息', content)

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
        if cleanup_file(case_file):
            processed += 1

    print(f"\n处理完成：{processed}/{len(case_files)} 个文件")

if __name__ == '__main__':
    main()
