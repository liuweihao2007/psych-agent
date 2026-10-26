# 心理支持 Agent

## 项目简介
本项目是一个基于大模型和本地知识库的可交互心理支持 Agent。系统能够根据用户需求，自动调用工具完成任务，包括情绪记录、计划管理、知识检索和风险预警。

## 运行环境
- Python 3.10
- 详见 `requirements.txt`

## 启动说明
1. 安装依赖：`pip install -r requirements.txt`
2. 在根目录创建 `.env` 文件，填入智谱 API Key：`ZHIPU_API_KEY=你的密钥`
3. 初始化数据库：`python database.py`
4. 构建本地检索库：`python build_rag.py`
5. 启动 Web 界面：`python app.py`

## 核心功能与工具
Agent 内置了 7 个真实工具：
1. `save_mood`：保存情绪记录
2. `query_mood`：查询情绪记录
3. `save_plan`：保存行动计划
4. `get_plans`：查询计划
5. `update_plan`：修改计划
6. `assess_risk`：危机风险预警（引导拨打 12356）
7. `search_knowledge`：本地知识检索

## 项目特色
- **RAG 增强**：通过本地心理问答库进行检索增强。
- **真实工具调用**：所有工具均连接本地 SQLite 数据库或 JSON 文件，真实读写。
- **状态管理**：支持同一会话内的多轮连续交互。
- **异常恢复**：工具或 API 失败时，自动记录日志（`logs/failures.log`）并保持程序继续运行。

## 测试日志
- `logs/tool_calls.jsonl`：记录了多轮连续的工具调用成功日志。
- `logs/failures.log`：记录了异常恢复的测试日志。