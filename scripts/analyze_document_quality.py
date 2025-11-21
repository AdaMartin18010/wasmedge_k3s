#!/usr/bin/env python3
"""
全面分析文档质量，识别内容空洞的文件
"""
import re
import os
from pathlib import Path
from collections import defaultdict

def analyze_file(file_path):
    """分析单个文件的质量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None

    stats = {
        'path': str(file_path),
        'lines': len(content.splitlines()),
        'chars': len(content),
        'words': len(content.split()),
        'placeholders': 0,
        'code_blocks': 0,
        'sections': 0,
        'empty_sections': 0,
        'todos': 0,
        'issues': []
    }

    # 检查占位符
    placeholder_patterns = [
        r'TODO',
        r'FIXME',
        r'待补充',
        r'待完善',
        r'待添加',
        r'待实现',
        r'待更新',
        r'占位符',
        r'placeholder',
        r'\[待补充\]',
        r'\[待完善\]',
        r'\[待添加\]',
        r'\[待实现\]',
        r'\[待更新\]',
        r'\[TODO\]',
        r'\[FIXME\]',
        r'<!--.*?-->',  # HTML 注释
        r'//.*?TODO',
        r'#.*?TODO',
    ]

    for pattern in placeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        stats['placeholders'] += len(matches)

    # 检查代码块
    code_blocks = re.findall(r'```[\s\S]*?```', content)
    stats['code_blocks'] = len(code_blocks)

    # 检查章节
    sections = re.findall(r'^##+ ', content, re.MULTILINE)
    stats['sections'] = len(sections)

    # 检查空章节（只有标题，没有内容）
    for section in sections:
        section_match = re.search(rf'^{re.escape(section)}.*?$', content, re.MULTILINE)
        if section_match:
            start = section_match.end()
            next_section = re.search(r'^##+ ', content[start:], re.MULTILINE)
            end = start + next_section.start() if next_section else len(content)
            section_content = content[start:end].strip()
            if len(section_content) < 50:  # 少于50字符认为是空章节
                stats['empty_sections'] += 1

    # 检查 TODO/FIXME
    todos = re.findall(r'TODO|FIXME', content, re.IGNORECASE)
    stats['todos'] = len(todos)

    # 计算内容质量分数
    score = 100

    # 文件太短扣分
    if stats['lines'] < 50:
        score -= 30
        stats['issues'].append(f"文件过短（{stats['lines']} 行）")
    elif stats['lines'] < 100:
        score -= 15
        stats['issues'].append(f"文件较短（{stats['lines']} 行）")

    # 占位符过多扣分
    if stats['placeholders'] > 10:
        score -= 40
        stats['issues'].append(f"占位符过多（{stats['placeholders']} 处）")
    elif stats['placeholders'] > 5:
        score -= 20
        stats['issues'].append(f"占位符较多（{stats['placeholders']} 处）")
    elif stats['placeholders'] > 0:
        score -= 10
        stats['issues'].append(f"存在占位符（{stats['placeholders']} 处）")

    # 章节太少扣分
    if stats['sections'] < 3:
        score -= 20
        stats['issues'].append(f"章节过少（{stats['sections']} 个）")

    # 空章节过多扣分
    if stats['empty_sections'] > stats['sections'] * 0.3:
        score -= 15
        stats['issues'].append(f"空章节过多（{stats['empty_sections']}/{stats['sections']}）")

    # 没有代码示例扣分（技术文档）
    if 'TECHNICAL' in str(file_path) or 'ARCHITECTURE' in str(file_path):
        if stats['code_blocks'] == 0:
            score -= 15
            stats['issues'].append("缺少代码示例")

    # 内容比例过低扣分
    if stats['words'] < 200:
        score -= 20
        stats['issues'].append(f"内容过少（{stats['words']} 词）")

    stats['score'] = max(0, score)
    stats['needs_improvement'] = score < 70 or stats['placeholders'] > 0

    return stats

def main():
    """主函数"""
    docs_dir = Path(__file__).parent.parent / 'docs'

    # 获取所有 markdown 文件
    md_files = list(docs_dir.rglob('*.md'))

    print(f"找到 {len(md_files)} 个 markdown 文件\n")
    print("正在分析文档质量...\n")

    results = []
    for md_file in md_files:
        stats = analyze_file(md_file)
        if stats:
            results.append(stats)

    # 按分数排序
    results.sort(key=lambda x: x['score'])

    # 统计
    total_files = len(results)
    needs_improvement = sum(1 for r in results if r['needs_improvement'])
    low_score = sum(1 for r in results if r['score'] < 50)
    high_placeholders = sum(1 for r in results if r['placeholders'] > 10)

    print("=" * 80)
    print("文档质量分析报告")
    print("=" * 80)
    print(f"\n总文件数：{total_files}")
    print(f"需要改进：{needs_improvement} ({needs_improvement/total_files*100:.1f}%)")
    print(f"低质量文件（<50分）：{low_score} ({low_score/total_files*100:.1f}%)")
    print(f"占位符过多（>10处）：{high_placeholders} ({high_placeholders/total_files*100:.1f}%)")

    # 按问题类型分组
    issues_by_type = defaultdict(list)
    for r in results:
        for issue in r['issues']:
            issue_type = issue.split('（')[0] if '（' in issue else issue.split('（')[0]
            issues_by_type[issue_type].append(r['path'])

    print("\n" + "=" * 80)
    print("问题类型统计")
    print("=" * 80)
    for issue_type, files in sorted(issues_by_type.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n{issue_type}: {len(files)} 个文件")
        if len(files) <= 10:
            for f in files[:10]:
                print(f"  - {f}")
        else:
            for f in files[:5]:
                print(f"  - {f}")
            print(f"  ... 还有 {len(files) - 5} 个文件")

    # 输出最需要改进的文件
    print("\n" + "=" * 80)
    print("最需要改进的文件（前20个）")
    print("=" * 80)
    for i, r in enumerate(results[:20], 1):
        print(f"\n{i}. {r['path']}")
        print(f"   分数：{r['score']}/100")
        print(f"   行数：{r['lines']}, 占位符：{r['placeholders']}, 章节：{r['sections']}")
        if r['issues']:
            print(f"   问题：{', '.join(r['issues'][:3])}")

    # 保存详细报告
    report_file = Path(__file__).parent.parent / 'DOCUMENT-QUALITY-ANALYSIS.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 文档质量分析报告\n\n")
        f.write(f"**分析时间**：{Path(__file__).stat().st_mtime}\n\n")
        f.write(f"**总文件数**：{total_files}\n\n")
        f.write(f"**需要改进**：{needs_improvement} ({needs_improvement/total_files*100:.1f}%)\n\n")
        f.write(f"**低质量文件（<50分）**：{low_score} ({low_score/total_files*100:.1f}%)\n\n")
        f.write(f"**占位符过多（>10处）**：{high_placeholders} ({high_placeholders/total_files*100:.1f}%)\n\n")

        f.write("## 最需要改进的文件\n\n")
        for i, r in enumerate(results[:50], 1):
            f.write(f"### {i}. {r['path']}\n\n")
            f.write(f"- **分数**：{r['score']}/100\n")
            f.write(f"- **行数**：{r['lines']}\n")
            f.write(f"- **占位符**：{r['placeholders']}\n")
            f.write(f"- **章节数**：{r['sections']}\n")
            if r['issues']:
                f.write(f"- **问题**：{', '.join(r['issues'])}\n")
            f.write("\n")

    print(f"\n详细报告已保存到：{report_file}")

if __name__ == '__main__':
    main()
