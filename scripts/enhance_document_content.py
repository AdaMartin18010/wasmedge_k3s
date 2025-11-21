#!/usr/bin/env python3
"""
增强文档内容：补充实质性内容、添加代码示例、更新最新信息
"""
import re
import os
from pathlib import Path
from collections import defaultdict

def identify_content_gaps(content):
    """识别内容空白"""
    gaps = []

    # 检查占位符
    placeholder_patterns = [
        r'TODO',
        r'FIXME',
        r'待补充',
        r'待完善',
        r'待添加',
        r'\[待补充\]',
        r'\[待完善\]',
        r'\[待添加\]',
    ]

    for pattern in placeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            gaps.append(f"占位符：{len(matches)} 处")

    # 检查空章节
    sections = re.findall(r'^##+ (.+)$', content, re.MULTILINE)
    for section in sections:
        # 检查章节内容
        section_match = re.search(rf'^##+ {re.escape(section)}.*?$', content, re.MULTILINE)
        if section_match:
            start = section_match.end()
            next_section = re.search(r'^##+ ', content[start:], re.MULTILINE)
            end = start + next_section.start() if next_section else len(content)
            section_content = content[start:end].strip()
            if len(section_content) < 50:
                gaps.append(f"空章节：{section}")

    # 检查缺少代码示例（技术文档）
    if 'TECHNICAL' in content or 'ARCHITECTURE' in content:
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        if len(code_blocks) == 0:
            gaps.append("缺少代码示例")

    return gaps

def suggest_improvements(file_path, content):
    """建议改进内容"""
    suggestions = []

    # 根据文件路径和内容建议改进
    if 'spark' in str(file_path).lower():
        suggestions.append("补充 Spark 3.5/4.0 最新特性")
        suggestions.append("添加 Kubernetes 部署示例")
        suggestions.append("添加性能优化配置")

    if 'wasmedge' in str(file_path).lower():
        suggestions.append("更新 WasmEdge 0.14+ 最新特性")
        suggestions.append("添加 Wasm 应用示例")
        suggestions.append("补充性能基准数据")

    if 'k3s' in str(file_path).lower():
        suggestions.append("更新 K3s 1.30+ 最新特性")
        suggestions.append("添加边缘部署示例")
        suggestions.append("补充最佳实践")

    if 'kubernetes' in str(file_path).lower():
        suggestions.append("更新 Kubernetes 1.30+ 最新特性")
        suggestions.append("添加部署配置示例")
        suggestions.append("补充安全最佳实践")

    return suggestions

def main():
    """主函数"""
    docs_dir = Path(__file__).parent.parent / 'docs'

    # 获取需要改进的文件
    md_files = list(docs_dir.rglob('*.md'))

    print(f"分析 {len(md_files)} 个文件...\n")

    files_needing_improvement = []

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        gaps = identify_content_gaps(content)
        suggestions = suggest_improvements(md_file, content)

        if gaps or suggestions:
            files_needing_improvement.append({
                'path': str(md_file.relative_to(docs_dir.parent)),
                'gaps': gaps,
                'suggestions': suggestions
            })

    # 生成改进报告
    report_file = Path(__file__).parent.parent / 'DOCUMENT-ENHANCEMENT-PLAN.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 文档内容增强计划\n\n")
        f.write(f"**生成时间**：2025-11-15\n\n")
        f.write(f"**需要改进的文件数**：{len(files_needing_improvement)}\n\n")

        f.write("## 改进优先级\n\n")
        f.write("### 高优先级（核心文档）\n\n")

        high_priority = [f for f in files_needing_improvement
                        if any(keyword in f['path'].lower()
                              for keyword in ['spark', 'wasmedge', 'k3s', 'kubernetes', 'README'])]

        for i, file_info in enumerate(high_priority[:20], 1):
            f.write(f"### {i}. {file_info['path']}\n\n")
            if file_info['gaps']:
                f.write("**内容空白**：\n")
                for gap in file_info['gaps']:
                    f.write(f"- {gap}\n")
                f.write("\n")
            if file_info['suggestions']:
                f.write("**改进建议**：\n")
                for suggestion in file_info['suggestions']:
                    f.write(f"- {suggestion}\n")
                f.write("\n")

        f.write("\n### 中优先级（重要文档）\n\n")
        medium_priority = [f for f in files_needing_improvement if f not in high_priority]
        for i, file_info in enumerate(medium_priority[:30], 1):
            f.write(f"{i}. {file_info['path']}\n")
            if file_info['gaps']:
                f.write(f"  - 内容空白：{', '.join(file_info['gaps'][:2])}\n")
            if file_info['suggestions']:
                f.write(f"  - 改进建议：{', '.join(file_info['suggestions'][:2])}\n")
            f.write("\n")

    print(f"改进计划已保存到：{report_file}")
    print(f"\n需要改进的文件：{len(files_needing_improvement)}")
    print(f"高优先级文件：{len(high_priority)}")

if __name__ == '__main__':
    main()
