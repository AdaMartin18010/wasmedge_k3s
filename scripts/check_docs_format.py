#!/usr/bin/env python3
"""
检查 docs 目录下的文件，找出缺少目录或章节序号的文件
"""
import re
from pathlib import Path

def check_file(file_path):
    """检查单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # 检查是否有目录
    has_toc = '## 📑 目录' in content or '## 目录' in content or '## TOC' in content

    # 检查主章节是否有序号
    main_sections = re.findall(r'^## ([^📑📖📚🚀📊🔗\d])', content, re.MULTILINE)
    sections_without_number = []
    for match in main_sections:
        line_start = content.rfind('\n## ', 0, content.find(match))
        if line_start >= 0:
            line = content[line_start:content.find('\n', line_start + 1)]
            # 检查是否以数字开头
            if not re.match(r'^## \d+\.', line):
                sections_without_number.append(line.strip())

    # 检查子章节是否有序号
    sub_sections = re.findall(r'^### ([^📑📖📚🚀📊🔗\d])', content, re.MULTILINE)
    sub_sections_without_number = []
    for match in sub_sections:
        line_start = content.rfind('\n### ', 0, content.find(match))
        if line_start >= 0:
            line = content[line_start:content.find('\n', line_start + 1)]
            # 检查是否以数字开头
            if not re.match(r'^### \d+\.\d+', line):
                sub_sections_without_number.append(line.strip())

    if not has_toc:
        issues.append("缺少目录")

    if sections_without_number:
        issues.append(f"主章节缺少序号: {len(sections_without_number)} 个")

    if sub_sections_without_number:
        issues.append(f"子章节缺少序号: {len(sub_sections_without_number)} 个")

    return issues

def main():
    """主函数"""
    docs_dir = Path(__file__).parent.parent / 'docs'

    # 获取所有 markdown 文件
    md_files = list(docs_dir.rglob('*.md'))

    print(f"找到 {len(md_files)} 个 markdown 文件")
    print("\n检查文件格式...\n")

    files_with_issues = []
    for md_file in sorted(md_files):
        # 跳过一些特殊文件
        if 'node_modules' in str(md_file) or '.git' in str(md_file):
            continue

        issues = check_file(md_file)
        if issues:
            files_with_issues.append((md_file, issues))
            print(f"❌ {md_file.relative_to(docs_dir.parent)}")
            for issue in issues:
                print(f"   - {issue}")

    print(f"\n总结：{len(files_with_issues)}/{len(md_files)} 个文件需要优化")

    # 按问题类型分组
    no_toc = [f for f, issues in files_with_issues if "缺少目录" in str(issues)]
    no_numbering = [f for f, issues in files_with_issues if "缺少序号" in str(issues)]

    print(f"\n详细统计：")
    print(f"  - 缺少目录：{len(no_toc)} 个文件")
    print(f"  - 缺少序号：{len(no_numbering)} 个文件")

if __name__ == '__main__':
    main()
