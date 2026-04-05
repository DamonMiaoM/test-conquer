#!/usr/bin/env python3
"""
修复 subagent 生成的 JSON 文件中的语法错误。
常见问题：JSON字符串中包含未转义的换行、引号等。
"""
import re
import json
import os

BATCH_DIR = '/Users/Damon/Projects/Test Conquer/data/batches'
FILES = [
    'batch_001-050_RESULT.json',
    'batch_051-100_RESULT.json',
    'batch_101-150_RESULT.json',
    'batch_151-200_RESULT.json',
    'batch_201-250_RESULT.json',
    'batch_251-300_RESULT.json',
]

def fix_and_parse(filepath):
    """尝试修复JSON语法错误并解析"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 先尝试直接解析
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
    # 尝试修复策略：
    # 1. 找到错误位置附近，检查是否有未转义的特殊字符
    
    # 策略：逐条提取 question 对象
    # 从 [ 开始，找到每个 { ... } 块
    items = []
    depth = 0
    current = ''
    in_string = False
    escape_next = False
    
    for i, ch in enumerate(content):
        if escape_next:
            current += ch
            escape_next = False
            continue
        
        if ch == '\\' and in_string:
            current += ch
            escape_next = True
            continue
        
        if ch == '"' and not escape_next:
            in_string = not in_string
            current += ch
            continue
        
        if not in_string:
            if ch == '{':
                if depth == 0:
                    current = '{'
                else:
                    current += ch
                depth += 1
            elif ch == '}':
                depth -= 1
                current += ch
                if depth == 0:
                    # 尝试解析这个对象
                    try:
                        obj = json.loads(current)
                        items.append(obj)
                    except json.JSONDecodeError:
                        # 尝试修复：在字符串值中替换未转义的换行
                        fixed = re.sub(r'(?<=": ")(.*?)(?=",\s*")', lambda m: m.group(0).replace('\n', ' ').replace('\r', ''), current, flags=re.DOTALL)
                        try:
                            obj = json.loads(fixed)
                            items.append(obj)
                        except json.JSONDecodeError:
                            print(f"  无法修复: 位置 {i}, 内容前100字符: {current[:100]}")
                    current = ''
            elif depth > 0:
                current += ch
    
    return items


def main():
    total = 0
    total_issues = 0
    
    for fname in FILES:
        filepath = os.path.join(BATCH_DIR, fname)
        if not os.path.exists(filepath):
            print(f"{fname}: 文件不存在")
            continue
        
        print(f"\n处理 {fname}...")
        
        items = fix_and_parse(filepath)
        print(f"  解析到 {len(items)} 道题")
        
        if items:
            # 验证
            issues = []
            for item in items:
                for field in ['id', 'question', 'answer', 'explanation', 'source']:
                    if field not in item:
                        issues.append(f"  Q{item.get('id','?')}: 缺少字段 {field}")
                if 'source' in item and ('url' not in item['source'] or not item['source']['url'].startswith('http')):
                    issues.append(f"  Q{item.get('id','?')}: source.url无效")
                if 'answer' in item and item['answer'] not in ('true', 'false'):
                    issues.append(f"  Q{item.get('id','?')}: answer值异常")
                if 'explanation' in item and len(item['explanation'].strip()) < 10:
                    issues.append(f"  Q{item.get('id','?')}: explanation太短")
            
            if issues:
                total_issues += len(issues)
                for issue in issues:
                    print(f"  {issue}")
            else:
                print(f"  质量检查通过 ✓")
            
            # 重新写入修复后的JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            print(f"  已重新写入修复后的JSON")
            
            total += len(items)
    
    print(f"\n总计: {total} 道题, {total_issues} 个问题")


if __name__ == '__main__':
    main()
