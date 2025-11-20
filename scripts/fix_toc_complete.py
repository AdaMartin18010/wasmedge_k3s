#!/usr/bin/env python3
"""
修复所有案例文件的目录，生成完整目录
"""
import os
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

def extract_sections(content):
    """提取所有章节"""
    sections = []
    lines = content.split('\n')
    
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
    
    return sections

def generate_toc(sections):
    """生成完整目录"""
    toc = ["## 📑 目录", ""]
    current_main = 0
    current_sub = 0
    
    for section in sections:
        if section[0] == 1:  # 主标题
            main_num, title, anchor = section[1], section[2], section[3]
            toc.append(f"{main_num}. [{title}](#{anchor})")
            current_main = main_num
            current_sub = 0
        elif section[0] == 2:  # 子标题
            main_num, sub_num, title, anchor = section[1], section[2], section[3], section[4]
            if main_num == current_main:
                toc.append(f"   - {main_num}.{sub_num} [{title}](#{anchor})")
            else:
                toc.append(f"{main_num}.{sub_num} [{title}](#{anchor})")
                current_main = main_num
            current_sub = sub_num
    
    return "\n".join(toc) + "\n\n---\n\n"

def fix_file(file_path):
    """修复单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有章节
    sections = extract_sections(content)
    
    if not sections:
        print(f"跳过 {file_path}：未找到章节")
        return False
    
    # 生成完整目录
    new_toc = generate_toc(sections)
    
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
    
    # 修复最后一个章节的序号（如果错误）
    # 查找所有主标题，找到最大的序号
    main_titles = re.findall(r'^## (\d+)\.', content, re.MULTILINE)
    if main_titles:
        max_num = max(int(n) for n in main_titles)
        # 检查更新记录章节
        content = re.sub(
            r'^## (\d+)\.\s*📝\s*更新记录',
            f'## {max_num}. 📝 更新记录',
            content,
            flags=re.MULTILINE
        )
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修复 {file_path}")
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
