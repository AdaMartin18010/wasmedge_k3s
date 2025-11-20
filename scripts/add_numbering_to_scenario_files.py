#!/usr/bin/env python3
"""
为应用场景文件添加章节序号
"""
import re
from pathlib import Path

def add_numbering_to_file(file_path):
    """为文件添加章节序号"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 定义章节映射
    section_mapping = {
        '场景描述': '1. 场景描述',
        '技术组合': '2. 技术组合',
        '关系矩阵': '3. 关系矩阵',
        '实际效果': '4. 实际效果',
        '三维坐标': '5. 三维坐标',
        '技术栈详情': '6. 技术栈详情',
        '参考文档': '7. 参考文档',
    }
    
    # 子章节映射
    sub_section_mapping = {
        '编排层': '6.1 编排层',
        '运行时层': '6.2 运行时层',
        '策略层': '6.3 策略层',
        '弹性扩展': '6.3 弹性扩展',
        '服务网格': '6.2 服务网格',
        'GPU 加速': '6.3 GPU 加速',
        '可观测性': '6.4 可观测性',
    }
    
    # 更新目录中的链接
    for old, new in section_mapping.items():
        # 更新目录中的链接
        content = re.sub(
            rf'- \[{re.escape(old)}\]\(#{re.escape(old.lower().replace(" ", "-"))}\)',
            f'- [{new}](#{new.lower().replace(" ", "-").replace(".", "")})',
            content
        )
        # 更新章节标题
        content = re.sub(
            rf'^## {re.escape(old)}$',
            f'## {new}',
            content,
            flags=re.MULTILINE
        )
    
    # 更新子章节
    for old, new in sub_section_mapping.items():
        # 更新目录中的链接
        content = re.sub(
            rf'    - \[{re.escape(old)}\]\(#{re.escape(old.lower().replace(" ", "-"))}\)',
            f'    - [{new}](#{new.lower().replace(" ", "-").replace(".", "")})',
            content
        )
        # 更新章节标题
        content = re.sub(
            rf'^### {re.escape(old)}$',
            f'### {new}',
            content,
            flags=re.MULTILINE
        )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已更新 {file_path}")
        return True
    else:
        print(f"跳过 {file_path}：无需更新")
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent.parent / 'docs' / 'TECHNICAL' / '08-architecture-analysis' / 'concept-relations-matrix' / 'applications'
    
    scenario_files = [
        base_dir / 'edge-computing-scenario.md',
        base_dir / 'ai-inference-scenario.md',
        base_dir / 'microservices-scenario.md',
    ]
    
    for file_path in scenario_files:
        if file_path.exists():
            add_numbering_to_file(file_path)

if __name__ == '__main__':
    main()
