#!/usr/bin/env python3
"""
Phase 0: 解析判断题.md权威答案，与HTML中的questions[]对比，生成差异报告。
"""

import re
import json
import sys

def parse_answer_key(md_path):
    """从判断题.md解析出 {题号: 'true'/'false'} 的映射"""
    answers = {}
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配模式: （ √ ）123.  或  （ × ）123.
    # 排除标题行中的"1.判断题"
    pattern = r'（\s*([√×])\s*）\s*(\d+)\s*[.．]'
    for match in re.finditer(pattern, content):
        mark = match.group(1).strip()
        qid = int(match.group(2))
        # 题号必须 >= 1 且 <= 500（排除标题行干扰）
        if 1 <= qid <= 500:
            if mark == '√':
                answers[qid] = 'true'
            elif mark == '×':
                answers[qid] = 'false'
    
    return answers


def extract_questions_from_html(html_path):
    """从HTML文件中提取questions数组"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 questions = [ 和对应的结束 ]; 或 ]\n
    start_marker = 'const questions = ['
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("ERROR: 未找到 questions 数组")
        sys.exit(1)
    
    start_idx += len(start_marker)
    
    # 找到匹配的结束位置 - 从start_idx开始计算括号深度
    depth = 1
    i = start_idx
    while i < len(content) and depth > 0:
        if content[i] == '[':
            depth += 1
        elif content[i] == ']':
            depth -= 1
        i += 1
    
    json_str = content[start_idx:i-1]
    
    # 修复JSON: 处理单引号key和尾逗号
    # 先把JS对象转成合法JSON
    # 用eval比较危险，但这里数据是自己的，先用简单替换
    json_str = json_str.replace("'", '"')  # 单引号转双引号
    # 移除尾逗号 (},] 或 },\n] 这种)
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # 尝试直接解析
    try:
        questions = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        # 尝试用正则提取每道题的关键字段
        questions = extract_via_regex(content[start_idx:i-1])
    
    return questions


def extract_via_regex(text):
    """备用方案：用正则提取question数据"""
    questions = []
    # 提取每个对象的id, answer
    pattern = r'"id"\s*:\s*(\d+).*?"answer"\s*:\s*"(true|false)"'
    for match in re.finditer(pattern, text, re.DOTALL):
        questions.append({
            'id': int(match.group(1)),
            'answer': match.group(2)
        })
    return questions


def main():
    md_path = '/Users/Damon/Projects/Test Conquer/docs/判断题.md'
    html_path = '/Users/Damon/Projects/Test Conquer/src/index.html'
    
    # 1. 解析权威答案
    answer_key = parse_answer_key(md_path)
    print(f"从判断题.md解析到 {len(answer_key)} 道题的答案")
    
    # 2. 提取HTML中的题目
    html_questions = extract_questions_from_html(html_path)
    print(f"从HTML中提取到 {len(html_questions)} 道题")
    
    # 3. 对比
    html_map = {q['id']: q['answer'] for q in html_questions}
    
    mismatches = []
    missing_from_md = []
    missing_from_html = []
    
    for qid in sorted(set(list(answer_key.keys()) + list(html_map.keys()))):
        md_ans = answer_key.get(qid)
        html_ans = html_map.get(qid)
        
        if md_ans is None:
            missing_from_md.append(qid)
        elif html_ans is None:
            missing_from_html.append(qid)
        elif md_ans != html_ans:
            mismatches.append({
                'id': qid,
                'md_answer': md_ans,
                'html_answer': html_ans
            })
    
    # 4. 报告
    print("\n" + "="*60)
    print("差异报告")
    print("="*60)
    
    print(f"\n答案不一致的题目: {len(mismatches)} 道")
    for m in mismatches:
        print(f"  第{m['id']:3d}题: 判断题.md={m['md_answer']:5s} | HTML={m['html_answer']:5s} | 需修正为 {m['md_answer']}")
    
    if missing_from_md:
        print(f"\n判断题.md中缺失的题目: {missing_from_md}")
    if missing_from_html:
        print(f"\nHTML中缺失的题目: {missing_from_html}")
    
    if not mismatches:
        print("\n所有答案一致！")
    
    # 5. 输出JSON格式差异
    report = {
        'total_in_md': len(answer_key),
        'total_in_html': len(html_questions),
        'mismatches': mismatches,
        'missing_from_md': missing_from_md,
        'missing_from_html': missing_from_html,
        'answer_key': {str(k): v for k, v in sorted(answer_key.items())}
    }
    
    output_path = '/Users/Damon/Projects/Test Conquer/data/answer_diff_report.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存到: {output_path}")


if __name__ == '__main__':
    main()
