#!/usr/bin/env python3
"""从参考答案文件中提取答案，填入Markdown文件（改进版）"""
import re

ANSWER_FILE = "/Users/Damon/Projects/Test Conquer/docs/人工智能训练师（三级）技能操作复习答案汇总_lint.md"
SINGLE_MD = "/Users/Damon/Projects/Test Conquer/docs/单选题.md"
MULTI_MD = "/Users/Damon/Projects/Test Conquer/docs/多选题.md"

with open(ANSWER_FILE, 'r', encoding='utf-8') as f:
    text = f.read()

# ===== Extract Single Choice Answers =====
single_start = text.find('单选题')
multi_start = text.find('多选题')
single_section = text[single_start:multi_start] if multi_start > 0 else text[single_start:]

single_answers = {}

# Pattern: "( X )" where X is a single letter, preceded by question context
# We need to be careful to only match the answer, not option letters like "(A)职业活动"
# Key difference: answer is "( C )" with spaces, option is "(A)职业活动" without space after letter

# Strategy: find question numbers, then look for the answer pattern nearby
# Pattern 1: "number. stem ( X )"
for m in re.finditer(r'(\d+)[\.\。\\\.]\s*.*?\(\s*([A-D])\s*\)', single_section):
    num = int(m.group(1))
    ans = m.group(2)
    if num not in single_answers:
        single_answers[num] = ans

# Pattern 2: "### number. stem ( X )"
for m in re.finditer(r'###\s*(\d+)[\.\。\\\.]\s*.*?\(\s*([A-D])\s*\)', single_section):
    num = int(m.group(1))
    ans = m.group(2)
    single_answers[num] = ans

print(f"Extracted {len(single_answers)} single choice answers")
# Show some
for i in [1, 2, 3, 10, 50, 100, 200, 300]:
    print(f"  Q{i}: {single_answers.get(i, '???')}")

# ===== Extract Multi Choice Answers =====
multi_section = text[multi_start:] if multi_start > 0 else ''

multi_answers = {}

# Multi-choice answers are like (ABCDE), (ABCD), etc. - 2+ consecutive uppercase letters
# Pattern 1: "number. stem (ABCDE)"
for m in re.finditer(r'(\d+)[\.\。\\\.]\s*.*?\(([A-E]{2,})\)', multi_section):
    num = int(m.group(1))
    ans = m.group(2)
    if num not in multi_answers:
        multi_answers[num] = ans

# Pattern 2: "### number. stem (ABCDE)"
for m in re.finditer(r'###\s*(\d+)[\.\。\\\.]\s*.*?\(([A-E]{2,})\)', multi_section):
    num = int(m.group(1))
    ans = m.group(2)
    if num not in multi_answers:
        multi_answers[num] = ans

print(f"\nExtracted {len(multi_answers)} multi choice answers")
for i in [1, 2, 3, 7, 8, 50, 100, 200, 300]:
    print(f"  Q{i}: {multi_answers.get(i, '???')}")

# For unnumbered multi-choice questions, match by content
# Find lines ending with (ABC...) that don't start with a number
unnumbered_multi = []
for m in re.finditer(r'^([^\d#\n][^\n]*?)\(([A-E]{2,})\)\s*$', multi_section, re.MULTILINE):
    content = m.group(1).strip()
    ans = m.group(2)
    # Filter out option-only lines and empty content
    if len(content) > 5 and re.search(r'[\u4e00-\u9fff]', content):
        unnumbered_multi.append((content, ans))

print(f"Found {len(unnumbered_multi)} unnumbered multi-choice answers")
for i, (content, ans) in enumerate(unnumbered_multi[:10]):
    print(f"  [{ans}] {content[:80]}")

# ===== Fill answers into Single Choice MD =====
with open(SINGLE_MD, 'r', encoding='utf-8') as f:
    single_text = f.read()

def fill_single(text, answers):
    lines = text.split('\n')
    result = []
    q_num = 0
    
    for line in lines:
        m = re.match(r'^(\d+)\.\s*(.*)', line)
        if m:
            q_num = int(m.group(1))
            rest = m.group(2)
            ans = answers.get(q_num, '')
            if ans:
                # Replace (    ) or () with (X)
                rest = re.sub(r'\(\s{2,}\)', f'({ans})', rest)
                rest = re.sub(r'\(\s*\)', f'({ans})', rest)
            result.append(f'{q_num}. {rest}')
        else:
            result.append(line)
    
    return '\n'.join(result)

single_filled = fill_single(single_text, single_answers)
with open(SINGLE_MD, 'w', encoding='utf-8') as f:
    f.write(single_filled)

# ===== Fill answers into Multi Choice MD =====
with open(MULTI_MD, 'r', encoding='utf-8') as f:
    multi_text = f.read()

def fill_multi(text, answers):
    lines = text.split('\n')
    result = []
    q_num = 0
    
    for line in lines:
        m = re.match(r'^(\d+)\.\s*(.*)', line)
        if m:
            q_num = int(m.group(1))
            rest = m.group(2)
            ans = answers.get(q_num, '')
            if ans:
                rest = re.sub(r'\(\s{2,}\)', f'({ans})', rest)
                rest = re.sub(r'\(\s*\)', f'({ans})', rest)
            result.append(f'{q_num}. {rest}')
        else:
            result.append(line)
    
    return '\n'.join(result)

multi_filled = fill_multi(multi_text, multi_answers)
with open(MULTI_MD, 'w', encoding='utf-8') as f:
    f.write(multi_filled)

# ===== Summary =====
print("\n===== Summary =====")
single_q_count = len(re.findall(r'^\d+\.', single_filled, re.MULTILINE))
single_with_ans = len(re.findall(r'\(\s*[A-D]\s*\)', single_filled))
single_empty = len(re.findall(r'\(\s{2,}\)', single_filled))
print(f"Single: {single_q_count} questions, {single_with_ans} answered, {single_empty} empty")

multi_q_count = len(re.findall(r'^\d+\.', multi_filled, re.MULTILINE))
multi_with_ans = len(re.findall(r'\([A-E]{2,}\)', multi_filled))
multi_empty = len(re.findall(r'\(\s{2,}\)', multi_filled))
print(f"Multi: {multi_q_count} questions, {multi_with_ans} answered, {multi_empty} empty")
