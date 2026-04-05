#!/usr/bin/env python3
"""修复单选题.md的格式问题"""
import re

INPUT = "/Users/Damon/Projects/Test Conquer/docs/单选题.md"
OUTPUT = "/Users/Damon/Projects/Test Conquer/docs/单选题_fixed.md"

with open(INPUT, 'r', encoding='utf-8') as f:
    raw = f.read()

# Remove watermarks like "23四合院AI工坊"
raw = re.sub(r'\d*四合院AI工坊', '', raw)

# Remove "(E) 以我为主" at end
raw = raw.replace('(E) 以我为主', '')

# Remove trailing "(C)伪造数据\n(D)不使用未经授权的算法库" orphan lines issue
# First normalize line endings
raw = raw.replace('\r\n', '\n').replace('\r', '\n')

lines = raw.split('\n')

# Parse questions
questions = []
current_q = None  # (number, stem, options_lines, has_answer)
current_options = []

def flush_question():
    global current_q, current_options
    if current_q is not None:
        num, stem, opts_text, has_answer = current_q
        questions.append((num, stem, opts_text, has_answer))
    current_q = None
    current_options = []

def is_option_line(line):
    stripped = line.strip()
    if not stripped:
        return False
    # Option line: (A)xxx, (B)xxx, etc.
    if re.match(r'^\([A-D]\)', stripped):
        return True
    # Sometimes option lines start with just letter like "(A " or "A)"
    if re.match(r'^[A-D]\)', stripped):
        return True
    # Multiple options on one line: "(A)... (B)... (C)... (D)..."
    if re.match(r'^\([A-D]\).*\([A-D]\)', stripped):
        return True
    return False

def extract_options_from_line(line):
    """Extract option text from a line that may contain multiple options"""
    stripped = line.strip()
    # Find all (X) patterns
    options = re.findall(r'\([A-D]\)[^()]*', stripped)
    return options

def extract_answer_from_stem(stem):
    """Extract answer like (C) or ( A ) from stem"""
    match = re.search(r'\(\s*([A-D])\s*\)', stem)
    if match:
        return match.group(1)
    # Also try format like "( C )"
    match = re.search(r'\(\s*([A-D])\s*\)', stem)
    if match:
        return match.group(1)
    return None

# Pattern for question start: "number. stem" or "number stem"
# Also handles "number. (A ) answer" format
q_start_pattern = re.compile(r'^(\d+)\s*[\.\。]\s*(.*)')

for line in lines:
    stripped = line.strip()
    
    if not stripped:
        # Empty line - could be separator
        continue
    
    # Check if this is a question start
    match = q_start_pattern.match(stripped)
    if match:
        # Flush previous question
        flush_question()
        
        num = int(match.group(1))
        rest = match.group(2)
        
        # Check if rest contains inline options
        inline_opts = extract_options_from_line(rest)
        if inline_opts and len(inline_opts) >= 3:
            # All options are inline
            answer = extract_answer_from_stem(rest)
            # Remove answer from stem
            stem_clean = re.sub(r'\(\s*[A-D]\s*\)', '()', rest)
            # Remove inline options from stem, keep only the question text
            stem_only = re.split(r'\([A-D]\)', rest)[0].strip()
            # Re-add answer
            if answer:
                stem_final = stem_only.rstrip() + '(' + answer + ')'
            else:
                stem_final = stem_only.rstrip() + '()'
            
            current_q = (num, stem_final, ' '.join(inline_opts), answer is not None)
            current_options = []
        else:
            # Stem with answer embedded
            answer = extract_answer_from_stem(rest)
            if answer:
                stem_clean = re.sub(r'\(\s*[A-D]\s*\)', '()', rest)
                current_q = (num, stem_clean, '', answer is not None)
            else:
                current_q = (num, rest, '', False)
            current_options = []
    elif is_option_line(stripped):
        if current_q is not None:
            opts = extract_options_from_line(stripped)
            current_options.extend(opts)
        # else: orphan option, will be attached later
    else:
        # Could be continuation of stem or orphan text
        if current_q is not None:
            num, stem, opts_text, has_answer = current_q
            # Append to stem if no options collected yet
            if not opts_text and not current_options:
                current_q = (num, stem + ' ' + stripped, opts_text, has_answer)
            else:
                # This might be an orphan stem - treat as new question context
                # or continuation
                pass

flush_question()

# Now rebuild the questions with consistent formatting
output_lines = []
output_lines.append('# 人工智能训练师（三级）')
output_lines.append('')
output_lines.append('## 单选题')
output_lines.append('')
output_lines.append('（选择一个正确的答案，将相应的字母填入题内的括号中。）')
output_lines.append('')

# Renumber questions
for idx, (num, stem, opts_text, has_answer) in enumerate(questions, 1):
    # Clean stem
    stem_clean = stem.strip()
    
    # Ensure answer is in stem
    answer = extract_answer_from_stem(stem_clean)
    if answer:
        # Replace answer placeholder with actual answer
        stem_final = re.sub(r'\(\s*\)', '(' + answer + ')', stem_clean)
        if '(' not in stem_final or ')' not in stem_final:
            stem_final = stem_clean.rstrip().rstrip(')') + answer + ')'
    else:
        # Try to find answer at end
        match = re.search(r'([A-D])\s*$', stem_clean)
        if match:
            answer = match.group(1)
            stem_final = stem_clean[:match.start()].strip() + '(' + answer + ')'
        else:
            stem_final = stem_clean
    
    # Collect options from opts_text
    all_options = []
    if opts_text:
        opts = extract_options_from_line(opts_text)
        all_options.extend(opts)
    if current_options:
        pass  # already flushed
    
    # Re-extract options from opts_text more carefully
    if opts_text:
        all_options = re.findall(r'\([A-D]\)[^()]*', opts_text)
    
    # Format
    output_lines.append(f'{idx}. {stem_final}')
    output_lines.append('')
    if all_options:
        output_lines.append('   ' + ' '.join(all_options))
        output_lines.append('')

# Write output
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Processed {len(questions)} questions")
print(f"Output written to {OUTPUT}")

# Print first 10 questions for review
for i, (num, stem, opts_text, has_answer) in enumerate(questions[:10], 1):
    print(f"\nQ{i}: {stem[:80]}...")
    print(f"  Options: {opts_text[:100]}..." if opts_text else "  Options: (none)")
    print(f"  Has answer: {has_answer}")
