#!/usr/bin/env python3
"""从md版答案文件中提取多选题答案并填入（修复换行符问题）"""
import re

ANSWER_FILE = "/Users/Damon/Projects/Test Conquer/docs/人工智能训练师（三级）技能操作复习答案汇总.md"
MULTI_MD = "/Users/Damon/Projects/Test Conquer/docs/多选题.md"

with open(ANSWER_FILE, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize line endings!
text = text.replace('\r\n', '\n').replace('\r', '\n')

# Find multi choice section
multi_start = text.find('多选题')
multi_section = text[multi_start:]

multi_answers = {}

# Pattern: "number. stem (ABC)" - 2+ consecutive uppercase letters in parens
for m in re.finditer(r'(\d+)[\.\。\\\.]\s*.*?\(\s*([A-E]{2,})\s*\)', multi_section):
    num = int(m.group(1))
    ans = m.group(2)
    if num not in multi_answers:
        multi_answers[num] = ans

# Pattern: "### number. stem (ABC)"
for m in re.finditer(r'###\s*(\d+)[\.\。\\\.]\s*.*?\(\s*([A-E]{2,})\s*\)', multi_section):
    num = int(m.group(1))
    ans = m.group(2)
    if num not in multi_answers:
        multi_answers[num] = ans

print(f"Extracted {len(multi_answers)} multi choice answers")

# Find missing
missing = [i for i in range(1, 301) if i not in multi_answers]
if missing:
    print(f"Missing answers for {len(missing)} questions: {missing}")

# Fill answers
with open(MULTI_MD, 'r', encoding='utf-8') as f:
    multi_text = f.read()

lines = multi_text.split('\n')
result = []
q_num = 0

for line in lines:
    m = re.match(r'^(\d+)\.\s*(.*)', line)
    if m:
        q_num = int(m.group(1))
        rest = m.group(2)
        ans = multi_answers.get(q_num, '')
        if ans:
            rest = re.sub(r'\(\s{2,}\)', f'({ans})', rest)
            rest = re.sub(r'\(\s*\)', f'({ans})', rest)
        result.append(f'{q_num}. {rest}')
    else:
        result.append(line)

multi_filled = '\n'.join(result)
with open(MULTI_MD, 'w', encoding='utf-8') as f:
    f.write(multi_filled)

# Summary
multi_q_count = len(re.findall(r'^\d+\.', multi_filled, re.MULTILINE))
multi_with_ans = len(re.findall(r'\([A-E]{2,}\)', multi_filled))
multi_empty = len(re.findall(r'\(\s{2,}\)', multi_filled))
print(f"\nResult: {multi_q_count} questions, {multi_with_ans} answered, {multi_empty} empty")
