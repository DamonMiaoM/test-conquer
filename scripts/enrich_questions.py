#!/usr/bin/env python3
"""
Enrich questions.json with explanation and source fields.
Uses keyword matching to categorize questions and assigns appropriate
explanations and source URLs.
"""

import json

# Source URL mappings by topic
SOURCES = {
    "ethics": {"title": "职业道德 — 维基百科", "url": "https://zh.wikipedia.org/wiki/职业道德"},
    "data_security": {"title": "数据安全 — 维基百科", "url": "https://zh.wikipedia.org/wiki/数据安全"},
    "ml": {"title": "机器学习 — 维基百科", "url": "https://zh.wikipedia.org/wiki/机器学习"},
    "law": {"title": "中华人民共和国网络安全法 — 维基百科", "url": "https://zh.wikipedia.org/wiki/中华人民共和国网络安全法"},
    "data_labeling": {"title": "Data labeling — Wikipedia", "url": "https://en.wikipedia.org/wiki/Data_labeling"},
    "neural_network": {"title": "人工神经网络 — 维基百科", "url": "https://zh.wikipedia.org/wiki/人工神经网络"},
    "deep_learning": {"title": "深度学习 — 维基百科", "url": "https://zh.wikipedia.org/wiki/深度学习"},
    "nlp": {"title": "自然语言处理 — 维基百科", "url": "https://zh.wikipedia.org/wiki/自然语言处理"},
    "cv": {"title": "计算机视觉 — 维基百科", "url": "https://zh.wikipedia.org/wiki/计算机视觉"},
    "office": {"title": "Microsoft Office 支持", "url": "https://support.microsoft.com"},
    "data_collection": {"title": "数据采集 — 维基百科", "url": "https://zh.wikipedia.org/wiki/数据采集"},
    "data_analysis": {"title": "数据分析 — 维基百科", "url": "https://zh.wikipedia.org/wiki/数据分析"},
    "ai_general": {"title": "人工智能 — 维基百科", "url": "https://zh.wikipedia.org/wiki/人工智能"},
    "patent": {"title": "专利 — 维基百科", "url": "https://zh.wikipedia.org/wiki/专利"},
    "copyright": {"title": "著作权 — 维基百科", "url": "https://zh.wikipedia.org/wiki/著作权"},
    "hci": {"title": "人机交互 — 维基百科", "url": "https://zh.wikipedia.org/wiki/人机交互"},
    "training": {"title": "模型训练 — 维基百科", "url": "https://zh.wikipedia.org/wiki/机器学习"},
    "deployment": {"title": "模型部署 — 维基百科", "url": "https://zh.wikipedia.org/wiki/机器学习"},
    "testing": {"title": "软件测试 — 维基百科", "url": "https://zh.wikipedia.org/wiki/软件测试"},
    "design_tools": {"title": "原型设计工具", "url": "https://en.wikipedia.org/wiki/Website_wireframe"},
    "data_preprocessing": {"title": "数据预处理 — 维基百科", "url": "https://zh.wikipedia.org/wiki/数据预处理"},
    "solution_design": {"title": "系统设计 — 维基百科", "url": "https://zh.wikipedia.org/wiki/系统设计"},
}


def categorize(q):
    """Categorize a question by keywords."""
    t = q["question"]

    # Ethics / professional morals (Q1-15, Q40-42)
    if any(k in t for k in ["职业道德", "道德评价", "道德规范", "奉献社会", "爱岗敬业", "遵纪守法", "职业守则"]):
        return "ethics"
    # AI ethics / bias
    if any(k in t for k in ["歧视性", "偏见性", "伦理", "公正", "无歧视"]):
        return "ethics"

    # Windows / Office (Q16-30)
    if any(k in t for k in ["Windows", "Word", "Excel", "浏览器", "鼠标", "键盘", "Ctrl", "MAX函数", "工作簿", "宏", "PPT"]):
        return "office"

    # Labor law
    if any(k in t for k in ["劳动合同", "试用期", "用人单位", "劳动者"]):
        return "law"

    # Cybersecurity / data privacy
    if any(k in t for k in ["网络运营者", "个人信息", "网络安全", "关键信息基础设施", "网络接入", "实名制"]):
        return "data_security"

    # Patent law
    if any(k in t for k in ["专利", "发明人", "设计人", "新颖性", "创造性", "实用性", "专利申请", "专利权"]):
        return "patent"

    # Copyright / IP
    if any(k in t for k in ["著作权", "知识产权", "原创性作品", "知识产权法"]):
        return "copyright"

    # Data collection tools
    if any(k in t for k in ["数据采集", "网络爬虫", "requests库", "数据抓取", "正则表达式", "爬虫"]):
        return "data_collection"

    # Data preprocessing / cleaning
    if any(k in t for k in ["数据清洗", "数据预处理", "缺失值", "异常值", "噪声数据", "数据去重", "数据归一化", "数据白化", "数据集成", "数据变换", "数据规约", "箱型图"]):
        return "data_preprocessing"

    # Data analysis / BI
    if any(k in t for k in ["数据分析", "Power BI", "业务流程", "数据治理", "ETL", "数据存储", "云服务", "大数据", "特征工程", "数据质量", "数据审核", "数据可视化"]):
        return "data_analysis"

    # Data labeling
    if any(k in t for k in ["数据标注", "标注工具", "标注员", "主动学习", "标注规范", "标注类型", "边界框", "语义分割"]):
        return "data_labeling"

    # NLP
    if any(k in t for k in ["自然语言处理", "词袋模型", "文本分析", "分词", "NLP"]):
        return "nlp"

    # Computer vision
    if any(k in t for k in ["计算机视觉", "图像识别", "图像处理", "目标检测", "卷积神经网络", "CNN"]):
        if "卷积神经网络" in t or "CNN" in t:
            return "neural_network"
        return "cv"

    # Neural networks / deep learning
    if any(k in t for k in ["神经网络", "激活函数", "深度学习", "生成对抗网络", "GAN"]):
        return "neural_network"

    # Model training
    if any(k in t for k in ["模型训练", "学习率", "损失函数", "超参数", "交叉验证", "过拟合", "欠拟合", "训练集", "测试集", "验证集", "特征提取", "降维", "算法训练", "TensorFlow", "PyTorch", "NumPy", "训练数据集"]):
        return "training"

    # ML general
    if any(k in t for k in ["机器学习", "监督学习", "无监督学习", "强化学习", "聚类分析", "关联规则", "线性回归", "决策树", "贝叶斯", "集成学习", "主成分分析", "PCA", "k折", "算法"]):
        return "ml"

    # Data decomposition / feature engineering
    if any(k in t for k in ["数据拆解", "数据拆分", "特征选择", "递归特征消除", "时间序列数据", "多维度数据分解", "分片"]):
        return "ml"

    # Model deployment
    if any(k in t for k in ["模型部署", "部署", "TensorFlow Lite", "容器化", "容器", "虚拟机", "虚拟化", "HPC", "高性能计算", "性能监控"]):
        return "deployment"

    # Testing
    if any(k in t for k in ["测试用例", "测试框架", "自动化测试", "算法测试", "鲁棒性", "安全性测试", "可解释性", "公平性测试", "k折交叉验证", "测试报告", "调试", "日志分析", "合规性测试", "测试管理"]):
        return "testing"

    # AI general applications
    if any(k in t for k in ["智能客服", "智能家居", "自动驾驶", "智能医疗", "推荐系统", "智能搜索", "智能交互", "智能控制", "生物特征识别", "知识图谱", "知识表示", "数据挖掘", "知识发现"]):
        return "ai_general"

    # HCI / UI design
    if any(k in t for k in ["人机交互", "用户界面", "UI", "UX", "用户体验", "触摸界面", "语音交互", "增强现实", "虚拟现实", "多模态交互", "用户研究", "原型设计", "情感设计", "可用性", "交互设计", "界面设计", "用户反馈"]):
        return "hci"

    # Design tools
    if any(k in t for k in ["Adobe XD", "Axure", "Balsamiq", "Figma", "Marvel", "Sketch", "设计系统"]):
        return "design_tools"

    # Training methods
    if any(k in t for k in ["培训讲义", "讲授法", "培训方法", "教学方法"]):
        return "training"

    # Solution design / product
    if any(k in t for k in ["智能解决方案", "用户需求分析", "产品功能", "技术选型", "系统集成", "云服务集成", "性能优化", "可扩展性", "代码审计", "故障恢复", "产品维护"]):
        return "solution_design"

    # Data processing tools / platforms
    if any(k in t for k in ["数据处理", "数据融合", "异常值检测", "数据可追溯性", "分布式数据处理"]):
        return "data_analysis"

    # Default
    return "ai_general"


def generate_explanation(q, topic):
    """Generate a brief explanation for a question."""
    t = q["question"]
    ans = q["answer"]
    is_true = ans == "true"

    # Generate context-aware explanations
    explanations = {
        1: "职业道德评价的核心标准是行为是否符合社会公认的道德规范，这是职业道德的基本原则。",
        2: "人工智能训练师处理敏感数据时，必须获得用户明确同意后方可使用，这是数据隐私保护的基本要求。",
        3: "全球化背景下，不同国家和地区的职业道德规范仍存在显著差异，呈现多元化而非单一化趋势。",
        4: "人工智能训练师在职业道德建设中必须考虑数据的质量与适用性，数据质量直接影响模型的可靠性和公平性。",
        5: "人工智能训练师对模型可能产生的歧视性或偏见性结果负有责任，应在开发过程中采取措施减少偏见。",
        6: "保护用户隐私是人工智能训练师职业道德的重要组成部分，涉及数据收集、存储和使用的各个环节。",
        7: "人工智能训练师的主要任务包括数据准备、标注管理、模型训练和评估，而不仅仅是设计和开发算法。",
        8: "职业守则不仅是软约束，在某些行业和领域还具有一定的法律效力，是行业规范的重要组成部分。",
        9: "职业守则具有行业特定性，不同行业的职业守则内容和要求各不相同，并非适用于所有行业。",
        10: "职业守则核心内容通常包括遵守法律、诚实守信、爱岗敬业、服务群众等方面。",
        11: "人工智能训练师在制定职业守则时，应充分考虑AI技术发展趋势和潜在风险，以确保守则的前瞻性和适用性。",
        12: "职业守则的实施与监督需要建立制度化的机制，不能仅依靠个人自觉性。",
        13: "奉献社会强调从业人员应把社会整体利益放在首位，而非把个人利益放在首位。",
        14: "爱岗敬业不仅取决于专业技能，还取决于职业道德素养、工作态度和责任心等多方面因素。",
        15: "人工智能训练师调整模型参数应基于科学方法和数据分析，而非仅凭个人经验和直觉。",
        16: "语音输入是Windows 10及以上版本中输入法支持的智能功能之一。",
        17: "Windows系统维护工具（如磁盘清理、系统优化软件）可以帮助用户优化性能、清理垃圾文件和修复问题。",
        18: "当鼠标和键盘无法使用时，可以通过强制关机重启后按F8键（部分系统为Shift+F8）进入高级启动选项。",
        19: "Windows 10小工具中的时钟可以通过设置使其始终显示在前端（置顶显示）。",
        20: "在浏览器地址栏中输入网址并回车是访问网页的基本操作方式。",
        21: "浏览器的高级设置和开发者工具可以帮助用户深入了解和管理浏览器的功能。",
        22: "Ctrl+C是标准的复制快捷键，在大多数应用程序中用于复制选中的文本或对象。",
        23: "Microsoft Word支持同时打开多个文档进行编辑，用户可以在不同文档间切换和操作。",
        24: "Word样式库中的样式可以快速应用于文档中的多个段落，提高排版效率和一致性。",
        25: "Word图文混排中，图片和文本框的位置可以通过设置环绕方式和拖动进行灵活调整。",
        26: "Excel的核心功能之一就是使用公式（如SUM、AVERAGE、MAX等）来计算和分析单元格中的数据。",
        27: "MAX函数是Excel中的内置函数，用于返回一组数值中的最大值。",
        28: "Excel图表不仅支持静态展示，还可以通过数据透视图、切片器等实现动态交互。",
        29: "工作簿的扩展名可以是.xls（旧版）或.xlsx（新版），并非只有.xls。",
        30: "Excel宏（VBA）可以将重复性操作自动化，显著提高工作效率。",
        31: "根据《劳动合同法》，试用期包含在劳动合同期限内，不存在「试用期满后自动转正」的法律概念。",
        32: "根据《劳动合同法》第十七条，劳动合同期限是劳动合同的必备条款之一。",
        33: "劳动者在试用期内解除劳动合同需要提前3日通知用人单位，而非随时解除。",
        34: "《网络安全法》明确规定网络运营者应采取技术措施确保个人信息安全，防止泄露、损毁、丢失。",
        35: "根据我国网络管理相关规定，用户进行网络接入注册时必须使用实名制。",
        36: "《网络安全法》要求关键信息基础设施运营者每年至少进行一次网络安全检测评估。",
        37: "专利申请权主体不仅限于发明人和设计人，还包括其所在单位（职务发明）和合法受让人。",
        38: "获得专利授权还需要满足其他条件，如申请程序合规、不违反法律和社会公德等，并非仅凭三性即可。",
        39: "专利申请流程要求提交请求书、说明书、权利要求书和摘要等文件。",
        40: "遵纪守法是每个社会成员的基本义务，自觉遵守法律法规是公民的基本素养。",
        41: "根据相关法律法规，人工智能训练师享有与其他职业相同的劳动保护权益。",
        42: "在AI训练工作中使用数据、算法或模型时，必须尊重知识产权的专有性和保护期限等基本原则。",
        43: "著作权法保护具有独创性并能以一定形式表现的智力成果，不仅限于原创性作品。",
        44: "专利权主体还包括职务发明的单位、合法受让人等，不仅限于发明人或设计人。",
        45: "知识产权保护不仅针对原创性作品，还包括商标、专利、商业秘密等多种类型。",
        46: "Python（爬虫库）、Excel（电子表格）和SQL Server（数据库）都是数据采集的常用工具。",
        47: "requests是Python中常用的HTTP请求库，广泛用于编写网络爬虫来获取网页数据。",
        48: "工具在数据采集中的意义不仅限于提高速度，还包括提高数据质量、一致性和可追溯性。",
        49: "数据治理工具的主要作用是确保数据的质量、一致性和合规性，优化AI训练数据的输入。",
        50: "ETL（Extract-Transform-Load）工具按照数据抽取、数据转换和数据加载三个基本步骤工作。",
        51: "现代数据存储和管理工具通常提供自动备份和恢复功能，以确保数据的安全性和可用性。",
        52: "云计算是基于互联网的计算方式，提供共享的软硬件资源和信息按需提供给各种终端设备。",
        53: "Excel可以打开CSV文件并通过另存为或其他功能将其转换为JSON格式。",
        54: "大数据处理平台（如Hadoop、Spark）可以同时处理结构化、半结构化和非结构化数据。",
        55: "常用数据处理工具如Python、Pandas等可以处理数值型、文本型甚至图像等多种数据类型。",
        56: "特征工程中的特征选择通常需要结合人工干预和领域知识，并非完全自动化。",
        57: "数据质量监控的主要目的是确保数据的准确性、完整性和一致性，而非减少数据集大小。",
        58: "数据审核平台是专门用于审核、验证和处理数据的软件工具，确保数据质量。",
        59: "Power BI是微软推出的商业智能工具，支持数据分析、可视化和报告制作。",
        60: "业务流程管理与优化工具适用于各种行业，不仅限于制造业。",
        61: "数据采集策略应合理使用自动化工具来提高效率和准确性，自动化不等于失去数据原始性。",
        62: "数据源选择应同时考虑准确性和可靠性等多个维度，不能仅基于准确性。",
        63: "正则表达式是数据抓取中非常强大的文本匹配工具，常用于从HTML中提取特定信息。",
        64: "数据抓取策略优化包括使用更快的工具、优化请求频率、使用代理等多个方面。",
        65: "关系型数据库适合存储结构化数据，非关系型数据库（NoSQL）更适合半结构化或非结构化数据。",
        66: "数据清洗的第一步通常是数据审查和理解，了解数据的整体情况后再进行缺失值处理等操作。",
        67: "数据清洗的主要目的确实是解决重复值、缺失值和异常值问题，以提高数据质量。",
        68: "加密技术保证数据的机密性，但数据泄露涉及多个环节（传输、存储、访问控制等），仅加密不能完全防止。",
        69: "实时数据处理技术（如流处理框架）能够处理大量数据并在极短时间内产生结果。",
        70: "主成分分析（PCA）和线性判别分析（LDA）是特征提取和降维的经典方法。",
        71: "容器化技术虽然优势明显，但不能完全替代虚拟化技术，两者各有适用场景。",
        72: "数据质量评估通常通过对数据进行抽样检查、统计分析等方法来进行。",
        73: "数据校验和异常数据检测都是为了确保数据的准确性和完整性，是数据质量保障的重要环节。",
        74: "高效业务流程设计的第一步是对现有流程进行详细分析，找出瓶颈和改进点。",
        75: "合规性检查应同时关注数据的安全性、完整性和可用性三个维度。",
        76: "业务数据产生于企业内部（如ERP系统）和外部（如客户交互、市场数据）的各种业务流程中。",
        77: "人工智能业务按应用场景可分为智能客服、智能家居、自动驾驶、智能医疗等多种类别。",
        78: "智能控制模块的核心功能之一就是实现设备控制，包括自动化控制和远程控制。",
        79: "推荐系统通常由用户画像、物品画像和推荐算法三个核心功能模块组成。",
        80: "智能搜索业务可以且经常通过自然语言处理技术来解析和理解用户搜索查询。",
        81: "智能交互功能模块具备自然语言处理能力，可以理解用户的语音指令和文本输入。",
        82: "自动数据处理结合AI模型和算力，可以从海量数据中挖掘出稳定且准确的分析结果。",
        83: "最优化决策支持利用AI计算来实现系统最优性能，找到最优业务指标的分配或决策方案。",
        84: "智能控制模块通过传感器感知环境、控制器做出决策、执行器执行动作来实现自动控制。",
        85: "NLP技术可以自动分析和理解人类语言的语法、语义，从而实现人机交互。",
        86: "生物特征识别必须在获得用户许可的前提下进行，未经许可获取生物特征侵犯隐私权。",
        87: "计算机视觉的功能包括图像处理、目标检测、图像识别、图像分割等多种任务。",
        88: "图像识别是计算机视觉领域的核心应用之一，也是智能计算的重要应用方向。",
        89: "数据清洗和预处理是数据挖掘流程中的必要步骤，不是可选步骤。",
        90: "监督学习、无监督学习和强化学习是数据挖掘和机器学习的三大基本方法。",
        91: "业务模块构建应遵循可扩展性、可重用性和可维护性等设计原则。",
        92: "业务流程优化方法主要包括流程再造（BPR）、流程改进（BPI）和流程分析三种。",
        93: "业务数据收集方法多样，包括问卷调查、访谈、观察、传感器采集、日志记录等多种方式。",
        94: "单据流（如订单流、发票流）是企业业务流程中的核心流程之一。",
        95: "简单业务流程分析的第一步是对现有流程进行详细记录和描述（As-Is分析）。",
        96: "简化业务流程不仅是减少环节和步骤，还要确保流程效率和质量的提升。",
        97: "监测和评估阶段的目的是评估优化效果，而非确定优化目标（目标在分析阶段确定）。",
        98: "控制图和帕累托图是复杂业务流程分析中常用的统计分析工具。",
        99: "复杂业务系统改进措施包括技术更新、流程优化、人员培训等多种方法。",
        100: "综合业务流程优化应遵循以客户为中心、以流程为导向和持续改进的原则。",
    }

    if q["id"] in explanations:
        return explanations[q["id"]]

    # Generic explanations based on topic and answer
    if topic == "ethics":
        if is_true:
            return "该说法正确。职业道德是从业人员在职业活动中应遵循的行为准则，包括诚实守信、爱岗敬业、服务社会等方面。"
        return "该说法错误。职业道德要求从业人员在工作中遵循社会道德规范，正确处理个人与社会的关系。"

    if topic == "office":
        if is_true:
            return "该说法正确。这是Windows/Office软件的基本功能之一，用户可以通过相应操作实现。"
        return "该说法错误。该描述不符合Windows/Office软件的实际功能和操作方式。"

    if topic == "law":
        if is_true:
            return "该说法正确。根据我国相关法律法规的规定，这是劳动者和用人单位应遵守的基本要求。"
        return "该说法错误。该描述不符合我国相关法律法规的规定。"

    if topic == "data_security":
        if is_true:
            return "该说法正确。根据《网络安全法》等相关法规，网络运营者应采取必要措施保障数据安全和用户隐私。"
        return "该说法错误。该描述不符合《网络安全法》等相关法规对数据安全的要求。"

    if topic == "patent":
        if is_true:
            return "该说法正确。这是专利法中的基本规定，符合专利申请和保护的相关要求。"
        return "该说法错误。该描述不符合专利法的相关规定，专利权的主体和客体有明确的法律界定。"

    if topic == "copyright":
        if is_true:
            return "该说法正确。这是著作权法或知识产权法中的基本规定。"
        return "该说法错误。知识产权保护的范围不仅限于原创性作品，还包括专利、商标等多种类型。"

    if topic == "data_collection":
        if is_true:
            return "该说法正确。这是数据采集领域的基本知识和常用方法。"
        return "该说法错误。数据采集工具和方法多样，应根据具体场景合理选择。"

    if topic == "data_preprocessing":
        if is_true:
            return "该说法正确。这是数据清洗与预处理中的基本操作和方法。"
        return "该说法错误。数据预处理需要根据数据特点选择合适的方法，不能一概而论。"

    if topic == "data_analysis":
        if is_true:
            return "该说法正确。这是数据分析和业务流程管理中的基本概念和常用方法。"
        return "该说法错误。该描述对数据分析工具或方法的理解不够准确。"

    if topic == "data_labeling":
        if is_true:
            return "该说法正确。数据标注是AI训练数据准备的关键环节，需要遵循规范的流程和标准。"
        return "该说法错误。数据标注需要综合考虑标注规范、工具选择和质量控制等因素。"

    if topic == "nlp":
        if is_true:
            return "该说法正确。自然语言处理技术可以分析和理解人类语言，是实现人机交互的重要技术。"
        return "该说法错误。该描述对NLP技术的理解不够准确。"

    if topic == "neural_network":
        if is_true:
            return "该说法正确。这是神经网络或深度学习的基本原理和特性。"
        return "该说法错误。该描述对神经网络的理解不够准确。"

    if topic == "ml":
        if is_true:
            return "该说法正确。这是机器学习领域的基本概念和常用方法。"
        return "该说法错误。该描述对机器学习方法或概念的理解有误。"

    if topic == "cv":
        if is_true:
            return "该说法正确。计算机视觉技术广泛应用于图像处理、目标检测和识别等领域。"
        return "该说法错误。该描述对计算机视觉技术的理解不够准确。"

    if topic == "training":
        if is_true:
            return "该说法正确。这是模型训练过程中的基本概念和常用方法。"
        return "该说法错误。模型训练应基于科学方法，不能仅凭经验或直觉判断。"

    if topic == "deployment":
        if is_true:
            return "该说法正确。这是模型部署和系统运维中的基本方法和最佳实践。"
        return "该说法错误。模型部署涉及多个环节，需要综合考虑环境配置、性能优化等因素。"

    if topic == "testing":
        if is_true:
            return "该说法正确。这是算法测试和模型评估中的基本原则和常用方法。"
        return "该说法错误。该描述对测试方法或评估指标的理解有误。"

    if topic == "ai_general":
        if is_true:
            return "该说法正确。这是人工智能领域的基本概念和应用方向。"
        return "该说法错误。该描述对人工智能技术或应用的理解不够准确。"

    if topic == "hci":
        if is_true:
            return "该说法正确。人机交互设计应遵循以用户为中心的原则，关注用户的操作习惯和体验。"
        return "该说法错误。该描述对人机交互设计原则的理解有误。"

    if topic == "design_tools":
        if is_true:
            return "该说法正确。这是原型设计工具的基本功能和使用方法。"
        return "该说法错误。该描述对该设计工具的功能理解有误。"

    if topic == "solution_design":
        if is_true:
            return "该说法正确。这是智能解决方案设计和系统开发中的基本原则和方法。"
        return "该说法错误。该描述对系统设计或产品开发的理解不够准确。"

    # Fallback
    if is_true:
        return "该说法正确。"
    return "该说法错误。"


def main():
    with open("data/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    enriched = []
    for q in questions:
        topic = categorize(q)
        explanation = generate_explanation(q, topic)
        source = SOURCES.get(topic, SOURCES["ai_general"])

        enriched.append({
            "id": q["id"],
            "question": q["question"],
            "answer": q["answer"],
            "explanation": explanation,
            "source": source,
            "topic": topic,
        })

    with open("data/questions_enriched.json", "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    print(f"Enriched {len(enriched)} questions → data/questions_enriched.json")

    # Print topic distribution
    from collections import Counter
    topic_counts = Counter(q["topic"] for q in enriched)
    print("\nTopic distribution:")
    for topic, count in sorted(topic_counts.items(), key=lambda x: -x[1]):
        print(f"  {topic}: {count}")


if __name__ == "__main__":
    main()
