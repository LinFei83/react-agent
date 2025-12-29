# LangGraph ReAct 智能体模板

[![CI](https://github.com/langchain-ai/react-agent/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/react-agent/actions/workflows/unit-tests.yml)
[![Open in - LangGraph Studio](https://img.shields.io/badge/Open_in-LangGraph_Studio-00324d.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4NS4zMzMiIGhlaWdodD0iODUuMzMzIiB2ZXJzaW9uPSIxLjAiIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHBhdGggZD0iTTEzIDcuOGMtNi4zIDMuMS03LjEgNi4zLTYuOCAyNS43LjQgMjQuNi4zIDI0LjUgMjUuOSAyNC41QzU3LjUgNTggNTggNTcuNSA1OCAzMi4zIDU4IDcuMyA1Ni43IDYgMzIgNmMtMTIuOCAwLTE2LjEuMy0xOSAxLjhtMzcuNiAxNi42YzIuOCAyLjggMy40IDQuMiAzLjQgNy42cy0uNiA0LjgtMy40IDcuNkw0Ny4yIDQzSDE2LjhsLTMuNC0zLjRjLTQuOC00LjgtNC44LTEwLjQgMC0xNS4ybDMuNC0zLjRoMzAuNHoiLz48cGF0aCBkPSJNMTguOSAyNS42Yy0xLjEgMS4zLTEgMS43LjQgMi41LjkuNiAxLjcgMS44IDEuNyAyLjcgMCAxIC43IDIuOCAxLjYgNC4xIDEuNCAxLjkgMS40IDIuNS4zIDMuMi0xIC42LS42LjkgMS40LjkgMS41IDAgMi43LS41IDIuNy0xIDAtLjYgMS4xLS44IDIuNi0uNGwyLjYuNy0xLjgtMi45Yy01LjktOS4zLTkuNC0xMi4zLTExLjUtOS44TTM5IDI2YzAgMS4xLS45IDIuNS0yIDMuMi0yLjQgMS41LTIuNiAzLjQtLjUgNC4yLjguMyAyIDEuNyAyLjUgMy4xLjYgMS41IDEuNCAyLjMgMiAyIDEuNS0uOSAxLjItMy41LS40LTMuNS0yLjEgMC0yLjgtMi44LS44LTMuMyAxLjYtLjQgMS42LS41IDAtLjYtMS4xLS4xLTEuNS0uNi0xLjItMS42LjctMS43IDMuMy0yLjEgMy41LS41LjEuNS4yIDEuNi4zIDIuMiAwIC43LjkgMS40IDEuOSAxLjYgMi4xLjQgMi4zLTIuMy4yLTMuMi0uOC0uMy0yLTEuNy0yLjUtMy4xLTEuMS0zLTMtMy4zLTMtLjUiLz48L3N2Zz4=)](https://langgraph-studio.vercel.app/templates/open?githubUrl=https://github.com/langchain-ai/react-agent)

本模板展示了基于 [LangGraph](https://github.com/langchain-ai/langgraph) 实现的 [ReAct 智能体](https://arxiv.org/abs/2210.03629)，面向 [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) 使用。ReAct 智能体结构简单，可灵活扩展各类工具。

![LangGraph Studio 中的图视图](./static/studio_ui.png)

核心逻辑位于 `src/react_agent/graph.py`，展示了一个可迭代推理并执行动作的 ReAct 智能体，适合处理复杂问题。

## 功能概览

ReAct 智能体的流程：

1. 接收用户 **query**
2. 推理并决定要执行的动作
3. 使用可用工具执行动作
4. 观察执行结果
5. 重复 2-4 步直至给出最终答案

默认附带基础工具集，可按需扩展自定义工具。

## 快速开始

假设已完成 [LangGraph Studio 安装](https://github.com/langchain-ai/langgraph-studio?tab=readme-ov-file#download)：

1. 创建 `.env` 文件。

```bash
cp .env.example .env
```

2. 在 `.env` 中填入所需的 API Key。

默认的 [搜索工具](./src/react_agent/tools.py) [^1] 使用 [Tavily](https://tavily.com/)。可在 [此处](https://app.tavily.com/sign-in) 创建密钥。

### 模型配置

默认模型如下：

```yaml
model: claude-sonnet-4-5-20250929
```

按需选择其他选项，或直接使用默认设置。

#### Anthropic

如需使用 Anthropic 聊天模型：

1. 注册获取 [Anthropic API Key](https://console.anthropic.com/)。
2. 将密钥写入 `.env`：

```
ANTHROPIC_API_KEY=your-api-key
```
#### OpenAI

如需使用 OpenAI 聊天模型：

1. 注册获取 [OpenAI API Key](https://platform.openai.com/signup)。
2. 将密钥写入 `.env`：
```
OPENAI_API_KEY=your-api-key
```

3. 根据需要定制代码。
4. 打开该项目文件夹到 LangGraph Studio 中运行。

## 如何定制

1. **新增工具**：在 [tools.py](./src/react_agent/tools.py) 增加 Python 函数，扩展智能体能力。
2. **更换模型**：默认使用 Anthropic Claude 3 Sonnet，可在运行时上下文中以 `provider/model-name` 形式指定，如 `openai/gpt-4-turbo-preview`。
3. **调整提示词**：默认系统提示词见 [prompts.py](./src/react_agent/prompts.py)，可通过上下文轻松修改。

你也可以通过以下方式拓展模板：

- 在 [graph.py](./src/react_agent/graph.py) 修改智能体推理流程。
- 调整 ReAct 循环或为决策过程添加额外步骤。

## 开发提示

迭代图时，可回溯并重跑历史状态以调试特定节点，本地更改会通过热更新自动生效。可以尝试在调用工具前添加中断、在 `src/react_agent/context.py` 中更换默认 persona，或增加新的节点和边。

后续请求会附加在同一线程中，右上角 `+` 按钮可新建线程并清除历史。

更多 LangGraph（建设中）文档参考 [LangGraph 仓库](https://github.com/langchain-ai/langgraph)，其中包含示例与参考指南，可帮助选择合适的模式。

LangGraph Studio 集成了 [LangSmith](https://smith.langchain.com/)，便于更深入的追踪与团队协作。

[^1]: https://python.langchain.com/docs/concepts/#tools
