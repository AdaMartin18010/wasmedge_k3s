#!/usr/bin/env python3
"""
分析文档内容，找出内容不足的文件
"""
import re
from pathlib import Path
from collections import defaultdict

def analyze_file(file_path):
    """分析单个文件的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None

    issues = []
    score = 100

    # 检查文件长度
    lines = content.split('\n')
    line_count = len(lines)
    non_empty_lines = len([l for l in lines if l.strip()])

    if line_count < 50:
        issues.append(f"文件过短（{line_count} 行）")
        score -= 30
    elif line_count < 100:
        issues.append(f"文件较短（{line_count} 行）")
        score -= 15

    # 检查占位符
    placeholders = [
        r'\[.*?\]',  # [占位符]
        r'TODO', r'FIXME', r'待补充', r'待完善',
        r'placeholder', r'示例', r'示例内容',
        r'XXX', r'YYY', r'ZZZ',
        r'这里需要', r'需要补充', r'待添加'
    ]

    placeholder_count = 0
    for pattern in placeholders:
        matches = re.findall(pattern, content, re.IGNORECASE)
        placeholder_count += len(matches)

    if placeholder_count > 0:
        issues.append(f"包含占位符（{placeholder_count} 处）")
        score -= min(placeholder_count * 5, 40)

    # 检查章节数量
    sections = re.findall(r'^##+ ', content, re.MULTILINE)
    section_count = len(sections)

    if section_count < 3:
        issues.append(f"章节过少（{section_count} 个）")
        score -= 20
    elif section_count < 5:
        issues.append(f"章节较少（{section_count} 个）")
        score -= 10

    # 检查代码示例
    code_blocks = re.findall(r'```', content)
    code_block_count = len(code_blocks) // 2

    if code_block_count == 0 and line_count > 100:
        issues.append("缺少代码示例")
        score -= 10

    # 检查链接
    links = re.findall(r'\[.*?\]\(.*?\)', content)
    link_count = len(links)

    if link_count == 0 and line_count > 100:
        issues.append("缺少外部链接")
        score -= 5

    # 检查实际内容（非标题、非空行）
    actual_content_lines = [
        l for l in lines
        if l.strip()
        and not l.strip().startswith('#')
        and not l.strip().startswith('-')
        and not l.strip().startswith('|')
        and not l.strip().startswith('```')
        and not l.strip().startswith('>')
    ]

    actual_content_ratio = len(actual_content_lines) / max(non_empty_lines, 1)

    if actual_content_ratio < 0.3:
        issues.append(f"实际内容比例低（{actual_content_ratio:.1%}）")
        score -= 20

    return {
        'file': file_path,
        'line_count': line_count,
        'non_empty_lines': non_empty_lines,
        'section_count': section_count,
        'code_block_count': code_block_count,
        'link_count': link_count,
        'placeholder_count': placeholder_count,
        'actual_content_ratio': actual_content_ratio,
        'issues': issues,
        'score': max(score, 0)
    }

def main():
    """主函数"""
    docs_dir = Path(__file__).parent.parent / 'docs'

    # 获取所有 markdown 文件
    md_files = list(docs_dir.rglob('*.md'))

    print(f"分析 {len(md_files)} 个 markdown 文件...\n")

    results = []
    for md_file in md_files:
        # 跳过一些特殊文件
        if 'node_modules' in str(md_file) or '.git' in str(md_file):
            continue

        result = analyze_file(md_file)
        if result:
            results.append(result)

    # 按分数排序
    results.sort(key=lambda x: x['score'])

    # 找出需要改进的文件
    needs_improvement = [r for r in results if r['score'] < 70]

    print(f"需要改进的文件：{len(needs_improvement)}/{len(results)} 个\n")

    # 按问题类型分组
    by_issue = defaultdict(list)
    for r in needs_improvement:
        for issue in r['issues']:
            by_issue[issue].append(r)

    print("问题统计：")
    for issue, files in sorted(by_issue.items(), key=lambda x: -len(x[1])):
        print(f"  - {issue}: {len(files)} 个文件")

    print(f"\n前 20 个最需要改进的文件：\n")
    for i, result in enumerate(needs_improvement[:20], 1):
        rel_path = result['file'].relative_to(docs_dir.parent)
        print(f"{i}. {rel_path} (分数: {result['score']})")
        print(f"   行数: {result['line_count']}, 章节: {result['section_count']}, 占位符: {result['placeholder_count']}")
        for issue in result['issues']:
            print(f"   - {issue}")
        print()

    # 保存详细报告
    report_file = docs_dir.parent / 'DOCUMENT-CONTENT-ANALYSIS.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 文档内容分析报告\n\n")
        f.write(f"**分析日期**：2025-11-15\n")
        f.write(f"**分析文件数**：{len(results)}\n")
        f.write(f"**需要改进文件数**：{len(needs_improvement)}\n\n")
        f.write("## 问题统计\n\n")
        for issue, files in sorted(by_issue.items(), key=lambda x: -len(x[1])):
            f.write(f"- **{issue}**：{len(files)} 个文件\n")
        f.write("\n## 需要改进的文件列表\n\n")
        for result in needs_improvement:
            rel_path = result['file'].relative_to(docs_dir.parent)
            f.write(f"### {rel_path}\n\n")
            f.write(f"- **分数**：{result['score']}\n")
            f.write(f"- **行数**：{result['line_count']}\n")
            f.write(f"- **章节数**：{result['section_count']}\n")
            f.write(f"- **占位符数**：{result['placeholder_count']}\n")
            f.write(f"- **问题**：\n")
            for issue in result['issues']:
                f.write(f"  - {issue}\n")
            f.write("\n")

    print(f"\n详细报告已保存到：{report_file}")

if __name__ == '__main__':
    main()
