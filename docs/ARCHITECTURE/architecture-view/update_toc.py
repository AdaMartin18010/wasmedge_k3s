#!/usr/bin/env python3
"""
批量更新所有 Markdown 文档的目录结构和序号
"""
import os
import re
from pathlib import Path

def extract_headers(file_path):
    """提取文档中的所有标题"""
    headers = []
    with open(file_path, 'r', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        # 匹配标题：## 1. 标题 或 ### 1.1 标题 或 #### 1.1.1 标题
        match = re.match(r'^(#{2,4})\s+(\d+(?:\.\d+)*)\.\s+(.+)$', line.strip())
        if match:
            level = len(match.group(1))
            number = match.group(2)
            title = match.group(3).strip()
            anchor = generate_anchor(title)
            headers.append({
                'line': i,
                'level': level,
                'number': number,
                'title': title,
                'anchor': anchor
            })
    
    return headers

def generate_anchor(title):
    """生成标题的锚点链接"""
    # 移除特殊字符，转换为小写，用连字符连接
    anchor = re.sub(r'[^\w\s-]', '', title.lower())
    anchor = re.sub(r'[-\s]+', '-', anchor)
    return anchor

def generate_toc(headers):
    """生成目录"""
    if not headers:
        return ""
    
    toc_lines = ["## 📑 目录", ""]
    for header in headers:
        indent = "  " * (header['level'] - 2)
        toc_lines.append(f"{indent}- [{header['number']}. {header['title']}](#{header['anchor']})")
    
    return "\n".join(toc_lines)

def update_file_toc(file_path):
    """更新文件的目录"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    headers = extract_headers(file_path)
    if not headers:
        return False
    
    # 生成新目录
    new_toc = generate_toc(headers)
    
    # 查找并替换目录部分
    # 匹配从 ## 📑 目录 到 --- 之间的内容
    toc_pattern = r'## 📑 目录.*?(?=\n---|\n## |\Z)'
    
    if re.search(toc_pattern, content, re.DOTALL):
        # 替换现有目录
        content = re.sub(toc_pattern, new_toc, content, flags=re.DOTALL)
        updated = True
    else:
        # 如果没有目录，在标题后添加
        title_pattern = r'(^# .+?\n)'
        match = re.match(title_pattern, content, re.MULTILINE)
        if match:
            insert_pos = match.end()
            # 检查是否有元数据块
            metadata_pattern = r'(^> \*\*.*?\*\*.*?\n)'
            metadata_match = re.search(metadata_pattern, content[insert_pos:], re.MULTILINE)
            if metadata_match:
                insert_pos += metadata_match.end()
            content = content[:insert_pos] + "\n" + new_toc + "\n\n---\n\n" + content[insert_pos:]
            updated = True
        else:
            updated = False
    
    if updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return updated

def main():
    """主函数"""
    base_dir = Path(__file__).parent
    md_files = list(base_dir.rglob("*.md"))
    
    updated_count = 0
    for md_file in md_files:
        if md_file.name in ['README.md', 'INDEX.md', 'SUMMARY.md']:
            continue
        
        try:
            if update_file_toc(md_file):
                print(f"Updated: {md_file.relative_to(base_dir)}")
                updated_count += 1
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    print(f"\nTotal files updated: {updated_count}")

if __name__ == "__main__":
    main()

