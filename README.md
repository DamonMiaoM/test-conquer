# Test Conquer

在线模拟考试平台 — 人工智能训练师（三级）模拟练习

## 功能

- 300 道判断题，逐题练习
- 即时反馈 + 知识点解释 + 学习链接
- 随机出题 / 顺序出题切换
- 错题记录与错题回顾
- 键盘快捷键（← 错、→ 对、Space 下一题）
- 响应式设计，支持手机端

## 快速开始

### 本地预览

```bash
# 直接用浏览器打开
open src/index.html

# 或用 Python 起一个本地服务器
cd src && python3 -m http.server 8000
# 然后访问 http://localhost:8000
```

### 重新生成

如果修改了题库数据，重新构建：

```bash
python3 scripts/build_html.py
```

### 部署到 GitHub Pages

1. 推送到 GitHub 仓库
2. 进入仓库 Settings → Pages
3. Source 选择 "Deploy from a branch"
4. Branch 选择 `main`，目录选择 `/src`
5. 保存后几分钟即可访问

## 项目结构

```
Test Conquer/
├── data/
│   ├── questions.json           # 原始题库
│   └── questions_enriched.json  # 含解释和来源的题库
├── scripts/
│   └── build_html.py            # 构建脚本
├── src/
│   └── index.html               # 生成的单文件 Web App
├── docs/                        # 项目文档
├── notes/                       # 开发笔记
├── public/                      # 静态资源
├── CLAUDE.md                    # Claude Code 指南
└── README.md                    # 本文件
```
