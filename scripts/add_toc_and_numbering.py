#!/usr/bin/env python3
"""
为案例文件添加目录和序号
"""
import os
import re
from pathlib import Path

def generate_toc(sections):
    """生成目录"""
    toc = ["## 📑 目录", ""]
    for i, (level, title, anchor) in enumerate(sections, 1):
        indent = "  " * (level - 1)
        toc.append(f"{indent}{i}. [{title}](#{anchor})")
    return "\n".join(toc) + "\n\n---\n\n"

def create_anchor(title):
    """创建锚点"""
    # 移除emoji和特殊字符
    anchor = re.sub(r'[📋📝🏗️📊🚀💡📚📑]', '', title)
    anchor = anchor.strip()
    # 转换为小写，替换空格为连字符
    anchor = anchor.lower().replace(' ', '-')
    # 移除特殊字符
    anchor = re.sub(r'[^\w\-]', '', anchor)
    return anchor

def process_file(file_path):
    """处理单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有目录
    if '## 📑 目录' in content:
        print(f"跳过 {file_path}：已有目录")
        return False
    
    lines = content.split('\n')
    new_lines = []
    sections = []
    section_num = 0
    subsection_num = {}
    in_toc = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检查是否是主标题（## 开头）
        if line.startswith('## '):
            title = line[3:].strip()
            # 跳过已有的目录标题
            if '📑' in title or '目录' in title:
                i += 1
                continue
            
            # 确定标题级别
            if '📋' in title or '案例基本信息' in title:
                section_num = 1
                subsection_num = {}
                anchor = create_anchor(title)
                sections.append((1, title.replace('📋', '').replace('案例基本信息', '案例基本信息').strip(), anchor))
                new_lines.append(f"## {section_num}. {title}")
            elif '📝' in title or '案例描述' in title:
                section_num = 2
                subsection_num = {}
                anchor = create_anchor(title)
                sections.append((1, title.replace('📝', '').replace('案例描述', '案例描述').strip(), anchor))
                new_lines.append(f"## {section_num}. {title}")
            elif '🏗️' in title or '技术栈' in title:
                section_num = 3
                subsection_num = {}
                anchor = create_anchor(title)
                sections.append((1, title.replace('🏗️', '').replace('技术栈', '技术栈').strip(), anchor))
                new_lines.append(f"## {section_num}. {title}")
            elif '📊' in title or '关键指标' in title:
                section_num = 4
                subsection_num = {}
                anchor = create_anchor(title)
                sections.append((1, title.replace('📊', '').replace('关键指标', '关键指标').strip(), anchor))
                new_lines.append(f"## {section_num}. {title}")
            elif '🚀' in title or '实施步骤' in title:
                section_num = 5
                subsection_num = {}
                anchor = create_anchor(title)
                sections.append((1, title.replace('🚀', '').replace('实施步骤', '实施步骤').strip(), anchor))
                new_lines.append(f"## {section_num}. {title}")
            elif '💡' in title or '经验总结' in title:
                section_num = 6
                subsection_num = {}
                anchor = create_anchor(title)
                sections.append((1, title.replace('💡', '').replace('经验总结', '经验总结').strip(), anchor))
                new_lines.append(f"## {section_num}. {title}")
            elif '📚' in title or '相关链接' in title:
                section_num = 7
                subsection_num = {}
                anchor = create_anchor(title)
                sections.append((1, title.replace('📚', '').replace('相关链接', '相关链接').strip(), anchor))
                new_lines.append(f"## {section_num}. {title}")
            elif '📝' in title or '更新记录' in title:
                section_num = 8
                subsection_num = {}
                anchor = create_anchor(title)
                sections.append((1, title.replace('📝', '').replace('更新记录', '更新记录').strip(), anchor))
                new_lines.append(f"## {section_num}. {title}")
            else:
                new_lines.append(line)
            i += 1
        # 检查是否是子标题（### 开头）
        elif line.startswith('### '):
            title = line[4:].strip()
            if section_num > 0:
                if section_num not in subsection_num:
                    subsection_num[section_num] = 0
                subsection_num[section_num] += 1
                sub_num = subsection_num[section_num]
                anchor = create_anchor(title)
                sections.append((2, title, f"{section_num}{sub_num}-{anchor}"))
                new_lines.append(f"### {section_num}.{sub_num} {title}")
            else:
                new_lines.append(line)
            i += 1
        else:
            # 在第一个 ## 标题后插入目录
            if i > 0 and lines[i-1].startswith('---') and not in_toc:
                # 检查是否在基本信息之后
                if section_num == 1 or (i > 10 and '收集日期' in lines[i-5:i]):
                    # 插入目录
                    toc = generate_toc(sections)
                    new_lines.append(toc)
                    in_toc = True
            new_lines.append(line)
            i += 1
    
    # 如果没有插入目录，在基本信息后插入
    if not in_toc and sections:
        # 找到基本信息结束的位置
        for idx, line in enumerate(new_lines):
            if '收集日期' in line and idx + 3 < len(new_lines):
                if new_lines[idx + 2].strip() == '---':
                    toc = generate_toc(sections)
                    new_lines.insert(idx + 3, toc)
                    break
    
    new_content = '\n'.join(new_lines)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已处理 {file_path}")
    return True

def main():
    """主函数"""
    cases_dir = Path(__file__).parent.parent / 'cases'
    
    # 获取所有案例文件（排除README和模板文件）
    case_files = [
        f for f in cases_dir.glob('*.md')
        if f.name not in ['README.md', 'case-template.md', 'CASE-PROGRESS-REPORT.md']
    ]
    
    print(f"找到 {len(case_files)} 个案例文件")
    
    processed = 0
    for case_file in sorted(case_files):
        if process_file(case_file):
            processed += 1
    
    print(f"\n处理完成：{processed}/{len(case_files)} 个文件")

if __name__ == '__main__':
    main()
