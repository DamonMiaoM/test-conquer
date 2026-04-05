"""
将 index.html 中的内联 questions 数组替换为从外部 JSON 加载
保留原始代码结构，只替换数据源
"""

import re

HTML_FILE = "/Users/Damon/Projects/Test Conquer/src/index.html"

def main():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the entire questions array with fetch-based loading
    old_block = re.search(
        r'// ===== Question Data =====\s*\nconst questions = \[.*?\];',
        content, re.DOTALL
    )

    if not old_block:
        print("ERROR: Could not find questions data block")
        return False

    new_block = '''// ===== Question Data =====
let questions = [];

// Load questions from external JSON
fetch('data/questions.json')
    .then(r => { if (!r.ok) throw new Error('Failed to load questions'); return r.json(); })
    .then(data => {
        questions = data;
        // Initialize app after data loads
        loadState();
        updateWrongCount();
        state.currentOrder = generateOrder(state.randomMode);
        displayQuestion();
    })
    .catch(err => {
        console.error('Error loading questions:', err);
        document.getElementById('question-text').textContent = '题目加载失败，请刷新页面重试。';
    });'''

    content = content[:old_block.start()] + new_block + content[old_block.end():]

    # Remove the old Init block at the bottom (it's now inside the fetch callback)
    old_init = re.search(
        r'// ===== Init =====\s*\nloadState\(\);\s*\nupdateWrongCount\(\);\s*\nstate\.currentOrder = generateOrder\(state\.randomMode\);\s*\ndisplayQuestion\(\);',
        content
    )

    if old_init:
        content = content[:old_init.start()] + content[old_init.end():]
        print("✅ Removed old Init block")
    else:
        print("⚠ Could not find old Init block (may already be removed)")

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated {HTML_FILE}")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
