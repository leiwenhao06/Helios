# Helios

基于 LangChain + Ollama 的本地通用 AI Agent，使用 `deepseek-r1:7b` 推理模型。

## 项目结构

```
Helios/
├── config/
│   ├── .env.example          # 环境变量模板
│   └── settings.yaml         # Agent 配置 (模型、工具、记忆)
├── data/
│   ├── long_term_memory/     # Chroma 向量数据库持久化目录
│   └── user_profiles/        # 用户偏好文件
├── docs/                     # 文档
├── src/
│   ├── agent/                # AgentExecutor 构建 (ReAct) + 任务规划
│   ├── llm/                  # Ollama 模型加载 (ChatOllama)
│   ├── memory/               # 短期记忆 (滑动窗口) + 长期记忆 (RAG 向量检索)
│   ├── tools/                # 内置工具 + 环境感知工具
│   ├── rag/                  # 嵌入模型 + Chroma 向量库管理
│   └── utils/                # YAML + .env 配置加载
├── tests/                    # 单元测试 + 集成测试
├── requirements.txt
├── main.py                   # 入口：交互式对话
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境
cp config/.env.example config/.env
# 编辑 config/.env (按需修改)

# 3. 拉取模型
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text

# 4. 启动对话
python main.py
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OLLAMA_BASE_URL` | Ollama 服务地址 | `http://localhost:11434` |
| `OLLAMA_MODEL` | 对话模型 | `deepseek-r1:7b` |
| `OLLAMA_TEMPERATURE` | 生成温度 | `0.8` |
| `OLLAMA_MAX_TOKENS` | 最大输出 token | `4096` |
| `EMBEDDING_MODEL` | 嵌入模型 | `nomic-embed-text` |

## 配置系统

`config/settings.yaml` 为主配置文件，支持 `${VAR:default}` 语法从环境变量注入值。`ConfigLoader` 类负责加载 YAML 并解析环境变量引用。

## Agent 架构

```
用户输入
    → 长期记忆检索 (Chroma 向量搜索 top-3)
    → 注入 ShortTermMemory (滑动窗口 k=10)
    → AgentExecutor (ReAct 模式)
    → 工具调用 (循环直到得出答案)
    → [helios]: 最终回答
```

## 工具系统

工具通过 `@tool` 装饰器定义，docstring 即为 Agent 的调用说明，注册在 `src/tools/__init__.py` 的 `ALL_TOOLS` 列表。

## 测试

```bash
pytest tests/ -v                        # 单元测试
pytest tests/ -v --run-integration      # 含 Ollama 集成测试
```

集成测试用 `@pytest.mark.integration` 装饰，CI 默认跳过。
