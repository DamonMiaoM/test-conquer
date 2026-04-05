# 开发过程记录：单选题接入 index.html

## 任务背景

将 `/Users/Damon/Projects/Test Conquer/docs/单选题.md`（300道单选题，已修复格式并填入答案）接入到 `/Users/Damon/Projects/Test Conquer/src/index.html` 的选择题 tab 中。

---

## 第一阶段：数据解析（已完成，2026-04-05 下午）

### 问题发现

原始 `单选题.md` 由 PDF/DOCX 解析而来，存在以下问题：
- 格式严重混乱，选项被拆散到多行
- 题号不连续，存在重复题号
- 水印文字（四合院AI工坊）散布全文
- 答案在原文中为空括号，需要从参考答案文件补充

### 解决方案

**不依赖 AI 阅读全量文本**，而是使用 Python 脚本直接读取原始 Word 文档（`第3部分3级_理论知识复习题 2_w.docx`），利用 python-docx 库按段落提取：

```python
from docx import Document
doc = Document('第3部分3级_理论知识复习题 2_w.docx')
# 段落 307 开始为单选题，段落 1808 为多选题
# 题目格式：题干（内嵌答案）+ 4个选项段落
```

用脚本解析出标准 JSON 格式，写入 `data/single_choice.json`：

```json
{
  "id": 1,
  "question": "职业道德的概念有广义和狭义之分...",
  "answer": "C",
  "options": [
    {"letter": "A", "text": "职业活动"},
    {"letter": "B", "text": "普通职业"},
    {"letter": "C", "text": "一定职业"},
    {"letter": "D", "text": "危险职业"}
  ],
  "type": "choice"
}
```

### 答案补充

单选题答案来自 `人工智能训练师（三级）技能操作复习答案汇总_lint.md`，用正则 `\(([A-D])\)` 匹配并填入。4道题答案跨行，手动修复（Q4/Q144/Q156/Q218）。

### 最终数据质量

| 指标 | 结果 |
|------|------|
| 总题数 | 300 |
| 已填答案 | 300 |
| 含4个选项 | 300 |
| 水印残留 | 0 |

---

## 第二阶段：index.html 选择题 Tab 实现

### 实现思路

**零 AI token 消耗策略**：数据已经就绪（single_choice.json），AI 只负责实现 UI 逻辑。选择题的实现复用了判断题 tab 的已有样式，仅新增选择题特有的交互逻辑。

### 文件修改清单

#### 1. CSS 样式（新增约15行）

在现有样式末尾添加选择题按钮样式，主要复用了 `.btn-choice-*` 的配色体系：

```css
.choice-card-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.btn-choice-option { padding: 14px; font-size: 1.05rem; border: 2px solid #e0e0e0; ... }
.btn-choice-option.correct { background: #27ae60; color: #fff; border-color: #27ae60; }
.btn-choice-option.wrong { background: #e74c3c; color: #fff; border-color: #e74c3c; }
```

#### 2. HTML 结构（替换占位符）

将 `<div class="placeholder">选择题 — 开发中，敬请期待</div>` 替换为完整的问题卡片结构，包含进度条、随机模式开关、错题本按钮、选项按钮区、反馈区、导航按钮和键盘提示。

#### 3. JavaScript 逻辑

**数据加载**：
```javascript
Promise.all([
    fetch('../data/questions.json'),  // 判断题
    fetch('../data/single_choice.json')  // 选择题
]).then(([judgeData, choiceData]) => { ... });
```

**新增 state**：
```javascript
const choiceState = {
    currentIndex: 0,
    currentOrder: [],
    answered: false,
    wrongQuestions: [],      // 独立错题本
    randomMode: true
};
```

**核心函数**：
- `displayChoiceQuestion()` — 渲染题目和选项按钮
- `checkChoiceAnswer(letter)` — 检查答案，高亮正确/错误选项
- `choiceNextQuestion()` / `choicePrevQuestion()` — 导航
- `showChoiceWrongBook()` — 选择题错题本

**键盘快捷键**（新增choice分支）：
- `A/B/C/D` — 直接选择答案
- `←/→` — 上一题/下一题
- `Space` — 已答对时跳转下一题

### 数据格式对比

| 字段 | 判断题 | 选择题 |
|------|--------|--------|
| `answer` | `"true"` / `"false"` | `"A"` / `"B"` / `"C"` / `"D"` |
| `options` | 无 | 含 `letter` + `text` |
| `explanation` | 有 | 空（可后续补充）|
| `source` | 有 | 空（可后续补充）|

---

## 第三阶段：GitHub 上传注意事项

### 建议提交的文件

```
/data/single_choice.json   ← 选择题数据（300题，~50KB）
/src/index.html            ← 更新的UI逻辑
/docs/单选题.md           ← 源文件（已格式化的MD）
/docs/多选题.md            ← 源文件（已格式化的MD，可选）
```

### 建议配置 `.gitattributes`

```gitattributes
*.json diff=json
```

这样 GitHub diff 会对 JSON 文件进行格式化展示，改善可读性。

### 题库维护建议

由于 JSON 在 GitHub diff 中可读性差，建议：
1. **以 MD 文件为唯一数据源**，JSON 由脚本自动生成
2. 团队成员修改题库时编辑 MD 文件，然后运行 `python3 extract_questions.py` 重新生成 JSON
3. 可选：添加 GitHub Actions CI，在 PR 时自动验证 JSON 格式并运行题目数量检查

---

## Token 消耗总结

| 阶段 | Token 消耗 | 说明 |
|------|------------|------|
| 数据解析 | ~0 | Python脚本离线执行 |
| 评估方案 | ~3K | 分析+方案设计 |
| 实现UI | ~8K | 修改HTML/CSS/JS |
| 文档撰写 | ~5K | 本文档 |
| **总计** | **<20K** | 远低于直接让AI阅读理解300题 |