#!/usr/bin/env python3
"""
从 index.html 提取 questions 数组，按批次保存为独立JSON文件。
每批50题，供 subagent 并行处理。
"""
import re
import json
import os

HTML_PATH = '/Users/Damon/Projects/Test Conquer/src/index.html'
OUTPUT_DIR = '/Users/Damon/Projects/Test Conquer/data/batches'

def extract_questions(html_path):
    """提取HTML中完整的questions数组"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = 'const questions = ['
    start_idx = content.find(start_marker)
    if start_idx == -1:
        raise ValueError("未找到 questions 数组")
    
    start_idx += len(start_marker)
    depth = 1
    i = start_idx
    while i < len(content) and depth > 0:
        if content[i] == '[':
            depth += 1
        elif content[i] == ']':
            depth -= 1
        i += 1
    
    raw = content[start_idx:i-1]
    
    # 用正则逐条提取，避免JSON解析问题
    # 匹配 { "id": N, "question": "...", "answer": "...", "explanation": "...", "source": {...}, "topic": "..." }
    questions = []
    
    # 简化方案：逐个id提取
    id_pattern = r'"id"\s*:\s*(\d+)'
    for id_match in re.finditer(id_pattern, raw):
        qid = int(id_match.group(1))
        # 从这个id开始提取到下一个id之前
        seg_start = id_match.start()
        next_match = re.search(r'"id"\s*:\s*\d+', raw[id_match.end():])
        if next_match:
            seg_end = id_match.end() + next_match.start()
        else:
            seg_end = len(raw)
        segment = raw[seg_start:seg_end]
        
        # 提取字段
        q = {'id': qid}
        
        question_match = re.search(r'"question"\s*:\s*"((?:[^"\\]|\\.)*)"', segment)
        if question_match:
            q['question'] = question_match.group(1).replace('\\"', '"').replace('\\n', '\n')
        
        answer_match = re.search(r'"answer"\s*:\s*"(true|false)"', segment)
        if answer_match:
            q['answer'] = answer_match.group(1)
        
        topic_match = re.search(r'"topic"\s*:\s*"([^"]*)"', segment)
        if topic_match:
            q['topic'] = topic_match.group(1)
        
        if 'question' in q and 'answer' in q:
            questions.append(q)
    
    # 按id排序
    questions.sort(key=lambda x: x['id'])
    return questions

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    questions = extract_questions(HTML_PATH)
    print(f"提取到 {len(questions)} 道题")
    
    # 验证完整性
    ids = [q['id'] for q in questions]
    expected = list(range(1, 301))
    if ids == expected:
        print("ID连续完整: 1-300 ✓")
    else:
        missing = set(expected) - set(ids)
        print(f"缺失ID: {missing}")
    
    # 按批次保存
    batches = [
        (1, 50, "A_职业道德与法律法规"),
        (51, 100, "B_数据工具与AI业务"),
        (101, 150, "C_机器学习基础"),
        (151, 200, "D_部署与测试"),
        (201, 250, "E_特征工程与系统设计"),
        (251, 300, "F_人机交互与培训"),
    ]
    
    for start, end, label in batches:
        batch = [q for q in questions if start <= q['id'] <= end]
        filename = f"batch_{start:03d}-{end:03d}_{label}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
        print(f"  {filename}: {len(batch)} 题")
    
    # 也保存完整列表（不含explanation/source，仅id+question+answer+topic）
    all_path = os.path.join(OUTPUT_DIR, 'all_questions_brief.json')
    with open(all_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"\n完整列表: {all_path}")

if __name__ == '__main__':
    main()
