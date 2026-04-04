#!/usr/bin/env python3
"""
Build src/index.html from questions_enriched.json.
Embeds all 300 questions as a JS array inside a single-file flashcard app.
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE, 'data', 'questions_enriched.json')
OUT_PATH = os.path.join(BASE, 'src', 'index.html')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Escape for JS embedding
questions_js = json.dumps(questions, ensure_ascii=False, indent=2)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Test Conquer - 人工智能训练师（三级）模拟练习</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', sans-serif; background: #f5f7fa; color: #333; }}
.container {{ max-width: 720px; margin: 0 auto; padding: 20px; }}
h1 {{ text-align: center; font-size: 1.5rem; margin-bottom: 20px; color: #2c3e50; }}

/* Tab navigation */
.tabs {{ display: flex; border-bottom: 2px solid #e0e0e0; margin-bottom: 24px; }}
.tab {{ padding: 12px 24px; cursor: pointer; border: none; background: none; font-size: 1rem; color: #666; border-bottom: 3px solid transparent; transition: all 0.2s; }}
.tab:hover {{ color: #333; }}
.tab.active {{ color: #4A90D9; border-bottom-color: #4A90D9; font-weight: 600; }}
.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}
.placeholder {{ text-align: center; padding: 80px 20px; color: #999; font-size: 1.2rem; }}

/* Progress bar */
.progress-container {{ position: relative; background: #e0e0e0; border-radius: 8px; height: 24px; margin-bottom: 16px; }}
.progress-bar {{ height: 100%; background: linear-gradient(90deg, #4A90D9, #357ABD); border-radius: 8px; transition: width 0.3s; }}
.progress-text {{ position: absolute; top: 0; left: 0; right: 0; text-align: center; line-height: 24px; font-size: 0.8rem; color: #fff; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.3); }}

/* Mode toggle */
.mode-toggle {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-size: 0.9rem; }}

/* Question card */
.card {{ background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; }}
.card-header {{ background: #4A90D9; color: #fff; padding: 12px 20px; font-size: 0.9rem; }}
.card-body {{ padding: 24px 20px; }}
.question-text {{ font-size: 1.1rem; line-height: 1.8; color: #2c3e50; }}
.card-actions {{ display: flex; gap: 16px; padding: 0 20px 24px; }}

/* Choice buttons */
.btn-choice {{ flex: 1; padding: 14px; font-size: 1.1rem; border: 2px solid #e0e0e0; border-radius: 8px; cursor: pointer; background: #fff; transition: all 0.2s; font-weight: 600; }}
.btn-true:hover {{ border-color: #27ae60; color: #27ae60; }}
.btn-false:hover {{ border-color: #e74c3c; color: #e74c3c; }}
.btn-true.selected {{ background: #27ae60; color: #fff; border-color: #27ae60; }}
.btn-false.selected {{ background: #e74c3c; color: #fff; border-color: #e74c3c; }}
.btn-choice:disabled {{ opacity: 0.6; cursor: default; }}

/* Feedback */
.feedback {{ margin-top: 16px; padding: 20px; background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
.feedback-result {{ font-size: 1.1rem; font-weight: 700; margin-bottom: 12px; padding: 8px 16px; border-radius: 6px; }}
.feedback-result.correct {{ background: #d4edda; color: #155724; }}
.feedback-result.wrong {{ background: #f8d7da; color: #721c24; }}
.feedback-explanation {{ font-size: 0.95rem; line-height: 1.7; color: #555; margin-bottom: 12px; }}
.feedback-source {{ font-size: 0.85rem; }}
.feedback-source a {{ color: #4A90D9; text-decoration: none; }}
.feedback-source a:hover {{ text-decoration: underline; }}

/* Navigation */
.nav-buttons {{ display: flex; gap: 12px; margin-top: 16px; }}
.btn-nav {{ flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 8px; background: #fff; cursor: pointer; font-size: 0.95rem; transition: background 0.2s; }}
.btn-nav:hover {{ background: #f0f0f0; }}

/* Secondary button */
.btn-secondary {{ padding: 6px 12px; border: 1px solid #ddd; border-radius: 6px; background: #fff; cursor: pointer; font-size: 0.85rem; }}

/* Keyboard hint */
.keyboard-hint {{ text-align: center; margin-top: 16px; font-size: 0.8rem; color: #aaa; }}

/* Modal */
.modal {{ position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 100; display: flex; align-items: center; justify-content: center; }}
.modal-overlay {{ position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); }}
.modal-content {{ position: relative; background: #fff; border-radius: 12px; max-width: 600px; width: 90%; max-height: 80vh; display: flex; flex-direction: column; }}
.modal-header {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 1px solid #eee; }}
.modal-header h2 {{ font-size: 1.2rem; }}
.modal-close {{ background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #999; }}
.modal-body {{ padding: 16px 20px; overflow-y: auto; flex: 1; }}
.modal-footer {{ padding: 12px 20px; border-top: 1px solid #eee; display: flex; gap: 12px; justify-content: flex-end; }}

.wrong-item {{ padding: 12px; border-bottom: 1px solid #f0f0f0; cursor: pointer; transition: background 0.2s; }}
.wrong-item:hover {{ background: #f9f9f9; }}
.wrong-item-id {{ font-size: 0.8rem; color: #999; margin-bottom: 4px; }}
.wrong-item-text {{ font-size: 0.95rem; color: #333; }}
.wrong-empty {{ text-align: center; padding: 40px; color: #999; }}

/* Utility */
.hidden {{ display: none !important; }}

/* Responsive */
@media (max-width: 480px) {{
    .container {{ padding: 12px; }}
    h1 {{ font-size: 1.2rem; }}
    .tab {{ padding: 10px 12px; font-size: 0.9rem; }}
    .question-text {{ font-size: 1rem; }}
    .btn-choice {{ padding: 12px; font-size: 1rem; }}
    .card-actions {{ flex-direction: column; }}
    .keyboard-hint {{ display: none; }}
}}
</style>
</head>
<body>
<div class="container">
    <h1>Test Conquer - 人工智能训练师（三级）</h1>

    <div class="tabs">
        <button class="tab active" data-tab="judge">判断题</button>
        <button class="tab" data-tab="choice">选择题</button>
        <button class="tab" data-tab="operation">操作题</button>
    </div>

    <div id="tab-judge" class="tab-content active">
        <div id="flashcard-area">
            <div class="progress-container">
                <div class="progress-bar" id="progress-bar"></div>
                <span class="progress-text" id="progress-text">0/{len(questions)}</span>
            </div>

            <div class="mode-toggle">
                <label><input type="checkbox" id="random-mode" checked> 随机出题</label>
                <button id="wrong-book-btn" class="btn-secondary">错题本 (<span id="wrong-count">0</span>)</button>
            </div>

            <div class="card" id="question-card">
                <div class="card-header">
                    <span id="question-number">第 1 题 / 共 {len(questions)} 题</span>
                </div>
                <div class="card-body">
                    <p id="question-text" class="question-text"></p>
                </div>
                <div class="card-actions" id="card-actions">
                    <button class="btn-choice btn-true" id="btn-true">对 ✓</button>
                    <button class="btn-choice btn-false" id="btn-false">错 ✗</button>
                </div>
            </div>

            <div class="feedback hidden" id="feedback-area">
                <div id="feedback-result" class="feedback-result"></div>
                <div id="feedback-explanation" class="feedback-explanation"></div>
                <div id="feedback-source" class="feedback-source"></div>
            </div>

            <div class="nav-buttons">
                <button class="btn-nav" id="btn-prev">上一题</button>
                <button class="btn-nav" id="btn-next">下一题</button>
            </div>

            <div class="keyboard-hint">
                快捷键: ← 错 | → 对 | Space 下一题
            </div>
        </div>
    </div>

    <div id="tab-choice" class="tab-content">
        <div class="placeholder">选择题 — 开发中，敬请期待</div>
    </div>

    <div id="tab-operation" class="tab-content">
        <div class="placeholder">操作题 — 开发中，敬请期待</div>
    </div>
</div>

<!-- Wrong question modal -->
<div class="modal hidden" id="wrong-modal">
    <div class="modal-overlay" id="modal-overlay"></div>
    <div class="modal-content">
        <div class="modal-header">
            <h2>错题本</h2>
            <button class="modal-close" id="modal-close">&times;</button>
        </div>
        <div class="modal-body" id="wrong-list"></div>
        <div class="modal-footer">
            <button class="btn-secondary" id="clear-wrong">清空错题</button>
            <button class="btn-secondary" id="retry-wrong">重做错题</button>
        </div>
    </div>
</div>

<script>
// ===== Question Data =====
const questions = {questions_js};

// ===== State =====
const state = {{
    currentIndex: 0,
    currentOrder: [],
    answered: false,
    wrongQuestions: [],
    randomMode: true,
    history: []
}};

// ===== Persistence =====
function loadState() {{
    const saved = localStorage.getItem('test-conquer-wrong');
    if (saved) state.wrongQuestions = JSON.parse(saved);
}}

function saveState() {{
    localStorage.setItem('test-conquer-wrong', JSON.stringify(state.wrongQuestions));
}}

// ===== Question Ordering =====
function generateOrder(random = true) {{
    const indices = Array.from({{ length: questions.length }}, (_, i) => i);
    if (random) {{
        for (let i = indices.length - 1; i > 0; i--) {{
            const j = Math.floor(Math.random() * (i + 1));
            [indices[i], indices[j]] = [indices[j], indices[i]];
        }}
    }}
    return indices;
}}

// ===== Display =====
function displayQuestion() {{
    const q = questions[state.currentOrder[state.currentIndex]];
    document.getElementById('question-number').textContent =
        `第 ${{state.currentIndex + 1}} 题 / 共 ${{state.currentOrder.length}} 题`;
    document.getElementById('question-text').textContent = q.question;
    const pct = ((state.currentIndex) / state.currentOrder.length) * 100;
    document.getElementById('progress-bar').style.width = pct + '%';
    document.getElementById('progress-text').textContent =
        `${{state.currentIndex}}/${{state.currentOrder.length}}`;
    document.querySelectorAll('.btn-choice').forEach(b => {{
        b.disabled = false;
        b.classList.remove('selected');
    }});
    document.getElementById('feedback-area').classList.add('hidden');
    state.answered = false;
}}

// ===== Answer Checking =====
function checkAnswer(userChoice) {{
    if (state.answered) return;
    state.answered = true;
    const q = questions[state.currentOrder[state.currentIndex]];
    const isCorrect = (userChoice === q.answer);

    document.querySelectorAll('.btn-choice').forEach(b => b.disabled = true);
    const selectedBtn = userChoice === 'true'
        ? document.getElementById('btn-true')
        : document.getElementById('btn-false');
    selectedBtn.classList.add('selected');

    const feedbackResult = document.getElementById('feedback-result');
    const feedbackExplanation = document.getElementById('feedback-explanation');
    const feedbackSource = document.getElementById('feedback-source');

    if (isCorrect) {{
        feedbackResult.className = 'feedback-result correct';
        feedbackResult.textContent = '✓ 回答正确！';
    }} else {{
        feedbackResult.className = 'feedback-result wrong';
        feedbackResult.textContent = `✗ 回答错误 — 正确答案：${{q.answer === 'true' ? '对' : '错'}}`;
        if (!state.wrongQuestions.includes(q.id)) {{
            state.wrongQuestions.push(q.id);
            saveState();
            updateWrongCount();
        }}
    }}

    feedbackExplanation.textContent = q.explanation || '';
    feedbackSource.innerHTML = q.source
        ? `🔗 学习资料：<a href="${{q.source.url}}" target="_blank" rel="noopener">${{q.source.title}}</a>`
        : '';
    document.getElementById('feedback-area').classList.remove('hidden');
}}

// ===== Navigation =====
function nextQuestion() {{
    if (state.currentIndex < state.currentOrder.length - 1) {{
        state.currentIndex++;
        displayQuestion();
    }} else {{
        state.currentOrder = generateOrder(state.randomMode);
        state.currentIndex = 0;
        displayQuestion();
    }}
}}

function prevQuestion() {{
    if (state.currentIndex > 0) {{
        state.currentIndex--;
        displayQuestion();
    }}
}}

// ===== Wrong Question Book =====
function updateWrongCount() {{
    document.getElementById('wrong-count').textContent = state.wrongQuestions.length;
}}

function showWrongBook() {{
    const list = document.getElementById('wrong-list');
    if (state.wrongQuestions.length === 0) {{
        list.innerHTML = '<div class="wrong-empty">还没有错题哦，继续加油！</div>';
    }} else {{
        list.innerHTML = state.wrongQuestions.map(id => {{
            const q = questions.find(q => q.id === id);
            return `<div class="wrong-item" data-id="${{id}}">
                <div class="wrong-item-id">第 ${{id}} 题</div>
                <div class="wrong-item-text">${{q.question}}</div>
            </div>`;
        }}).join('');
    }}
    document.getElementById('wrong-modal').classList.remove('hidden');
}}

// ===== Tab Switching =====
document.querySelectorAll('.tab').forEach(tab => {{
    tab.addEventListener('click', () => {{
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
    }});
}});

// ===== Event Listeners =====
document.getElementById('btn-true').addEventListener('click', () => checkAnswer('true'));
document.getElementById('btn-false').addEventListener('click', () => checkAnswer('false'));
document.getElementById('btn-next').addEventListener('click', nextQuestion);
document.getElementById('btn-prev').addEventListener('click', prevQuestion);
document.getElementById('random-mode').addEventListener('change', (e) => {{
    state.randomMode = e.target.checked;
    state.currentOrder = generateOrder(state.randomMode);
    state.currentIndex = 0;
    displayQuestion();
}});

document.getElementById('wrong-book-btn').addEventListener('click', showWrongBook);
document.getElementById('modal-close').addEventListener('click', () => {{
    document.getElementById('wrong-modal').classList.add('hidden');
}});
document.getElementById('modal-overlay').addEventListener('click', () => {{
    document.getElementById('wrong-modal').classList.add('hidden');
}});
document.getElementById('clear-wrong').addEventListener('click', () => {{
    if (confirm('确定要清空所有错题记录吗？')) {{
        state.wrongQuestions = [];
        saveState();
        updateWrongCount();
        showWrongBook();
    }}
}});
document.getElementById('retry-wrong').addEventListener('click', () => {{
    if (state.wrongQuestions.length === 0) return;
    state.currentOrder = state.wrongQuestions.map(id => questions.findIndex(q => q.id === id));
    state.currentIndex = 0;
    document.getElementById('wrong-modal').classList.add('hidden');
    displayQuestion();
}});
document.getElementById('wrong-list').addEventListener('click', (e) => {{
    const item = e.target.closest('.wrong-item');
    if (!item) return;
    const id = parseInt(item.dataset.id);
    const idx = questions.findIndex(q => q.id === id);
    if (idx >= 0) {{
        state.currentOrder = [idx];
        state.currentIndex = 0;
        document.getElementById('wrong-modal').classList.add('hidden');
        displayQuestion();
    }}
}});

// ===== Keyboard Shortcuts =====
document.addEventListener('keydown', (e) => {{
    if (!document.getElementById('tab-judge').classList.contains('active')) return;
    if (e.key === 'ArrowLeft') {{
        e.preventDefault();
        checkAnswer('false');
    }} else if (e.key === 'ArrowRight') {{
        e.preventDefault();
        checkAnswer('true');
    }} else if (e.key === ' ') {{
        e.preventDefault();
        if (state.answered) nextQuestion();
    }}
}});

// ===== Init =====
loadState();
updateWrongCount();
state.currentOrder = generateOrder(state.randomMode);
displayQuestion();
</script>
</body>
</html>'''

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Built {OUT_PATH} with {len(questions)} questions")
