# PersonalAssistant - 个性化智能工作助手

一个集成了**性格分析**、**习惯学习**、**任务执行**、**质量审查**和**个性化优化**的智能工作助手系统。

## 🎯 核心特性

### 1. 🧠 性格与习惯分析
- **5大维度性格分析**：时间管理风格、工作偏好、沟通风格、决策风格、输出偏好
- **实时学习**：从交互对话和任务执行记录中自动识别习惯
- **动态更新**：随着使用深度学习用户特征

### 2. 📋 工作流规划与执行
- **智能规划**：根据工作计划自动生成执行步骤
- **异步执行**：支持多任务并行执行
- **实时反馈**：每步执行后提供反馈

### 3. ✅ 质量审查与评分
- **多维度评分**：功能完成度、代码质量、执行效率等
- **个性化权重**：根据用户习惯调整评分标准
- **自动优化建议**：基于习惯提供改进方案

### 4. 📄 个性化文档生成
- **风格自适应**：自动调整文档格式和语言风格
- **粒度控制**：细致/概览两种任务分解方式
- **习惯匹配**：生成的文档符合用户阅读习惯

### 5. 🔄 工作流优化
- **模式识别**：识别用户工作模式和瓶颈
- **自动建议**：提出工作流改进方案
- **性格融合**：优化方案与用户性格相匹配

## 📁 项目结构

```
PersonalAssistant/
├── core/
│   ├── personality_analyzer.py      # 5维度性格分析
│   ├── habit_engine.py              # 习惯识别与追踪
│   ├── behavior_learner.py          # 行为学习系统
│   └── preference_manager.py        # 偏好管理和存储
├── agents/
│   ├── planner_agent.py             # 任务规划Agent
│   ├── executor_agent.py            # 任务执行Agent
│   ├── reviewer_agent.py            # 质量审查Agent
│   └── optimizer_agent.py           # 工作流优化Agent
├── document_generation/
│   ├── personalized_generator.py    # 个性化文档生成
│   ├── style_adapter.py             # 风格适配器
│   └── template_manager.py          # 模板管理
├── scoring/
│   ├── quality_scorer.py            # 基础质量评分
│   ├── personalized_scorer.py       # 个性化评分权重
│   └── recommendation_engine.py     # 建议优化引擎
├── data/
│   ├── interaction_history.py       # 交互历史
│   ├── task_history.py              # 任务历史
│   └── user_profile.py              # 用户档案
├── config/
│   └── config.yaml                  # 配置文件
├── main.py                          # 主程序入口
├── requirements.txt                 # 依赖文件
└── README.md                        # 项目说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化系统

```python
from main import PersonalAssistant

assistant = PersonalAssistant()
```

### 3. 设置工作计划

```python
tasks = [
    "完成项目文档",
    "代码审查",
    "性能优化"
]

result = assistant.execute_plan(tasks)
```

### 4. 查看个性化报告

```python
report = assistant.generate_report()
print(report)
```

## 📊 系统工作流

```
┌─────────────────┐
│  用户输入计划   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  交互历史 + 任务历史 分析   │
│  ↓                          │
│  识别用户习惯和性格特征     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  智能规划       │──→   │  异步并行执行    │
│  (Plan Agent)   │      │  (Exec Agent)    │
└─────────────────┘      └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  质量审查        │
                         │  (Review Agent)  │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
            ┌────────────┐ ┌────────────┐ ┌────────────┐
            │ 个性化评分 │ │  文档生成  │ │  优化建议  │
            │ (权重调整) │ │ (风格适配) │ │ (自动推荐) │
            └────────────┘ └────────────┘ └────────────┘
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │  个性化报告输出  │
                        └──────────────────┘
```

## 🎨 性格维度说明

### 1. 时间管理风格
- 早鸟型/夜猫型
- 拖延症/完美主义
- 计划性/灵活性

### 2. 工作偏好
- 学习方式：视觉/听觉/动觉
- 协作模式：独立/团队
- 任务类型：创意/分析/执行

### 3. 沟通风格
- 详细/简洁
- 正式/随意
- 直接/委婉

### 4. 决策风格
- 数据驱动/直觉型
- 谨慎/风险偏好
- 独立/征询意见

### 5. 输出偏好
- 文字/表格/图表
- 语言风格（专业/友好/学术等）
- 细节深度（概览/详细/极详细）

## 📈 学习与优化

系统会从以下方面学习：

1. **实时对话**
   - 用户反馈
   - 问题表述方式
   - 需求优先级

2. **任务执行记录**
   - 完成时间分布
   - 出错模式
   - 效率趋势

3. **文档偏好**
   - 格式选择
   - 阅读标记
   - 修改建议

4. **评分反馈**
   - 权重调整
   - 标准修正
   - 优先级变化

## 🔧 配置文件

编辑 `config/config.yaml` 来定制系统行为：

```yaml
# 性格分析配置
personality:
  update_frequency: "realtime"  # 实时/每日/每周
  sensitivity: 0.8              # 敏感度 0-1
  dimensions: ["time_style", "work_preference", "communication", "decision", "output"]

# 评分权重
scoring:
  functionality: 0.4
  quality: 0.3
  efficiency: 0.2
  user_satisfaction: 0.1

# 文档生成
document:
  auto_adapt: true
  style_options: ["detailed", "overview"]
  language: "zh_CN"

# 优化
optimization:
  auto_suggest: true
  learning_rate: 0.1
```

## 💡 使用示例

### 场景1：日常任务规划

```python
assistant = PersonalAssistant()

# 输入工作计划
plan = """
今天需要完成：
1. 完成项目文档
2. 代码审查
3. 修复3个bug
"""

# 执行
result = assistant.execute_plan(plan)

# 自动调整（基于用户习惯）
# - 如果是夜猫型，建议重排时间表
# - 如果喜欢详细说明，生成详细版
# - 如果完美主义，评分标准更严格
```

### 场景2：性能优化建议

```python
# 分析历史数据
insights = assistant.analyze_work_patterns()

# 自动生成优化方案
recommendations = assistant.generate_recommendations()

# 输出个性化报告
report = assistant.generate_personalized_report()
print(report)
```

## 📝 API文档

### PersonalAssistant 主类

```python
class PersonalAssistant:
    def __init__(self, config_path: str = "config/config.yaml")
    def execute_plan(self, plan: str) -> dict
    def analyze_personality(self) -> dict
    def generate_report(self, style: str = "auto") -> str
    def get_recommendations(self) -> List[str]
    def update_preferences(self, feedback: dict) -> None
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License
