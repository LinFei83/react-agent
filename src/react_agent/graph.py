"""定义自定义的 ReAct 智能体，依赖支持工具调用的聊天模型。"""

from datetime import UTC, datetime
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.runtime import Runtime

from react_agent.context import Context
from react_agent.state import InputState, State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model

# 调用模型的核心函数


async def call_model(
    state: State, runtime: Runtime[Context]
) -> Dict[str, List[AIMessage]]:
    """调用驱动智能体的 LLM。

    负责准备提示词、初始化模型并处理回复。

    Args:
        state (State): 当前对话状态。
        runtime (Runtime[Context]): 本次运行时上下文。

    Returns:
        dict: 包含模型回复的字典。
    """
    # 初始化并绑定工具，如需更换模型或添加工具在此修改
    model = load_chat_model(runtime.context.model).bind_tools(TOOLS)

    # 格式化系统提示词，可在此定制智能体行为
    system_message = runtime.context.system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )

    # 获取模型回复
    response = cast( # type: ignore[redundant-cast]
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages]
        ),
    )

    # 若已到最后一步仍尝试调用工具，则直接给出兜底回复
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="抱歉，在设定的步数内未能找到问题的答案。",
                )
            ]
        }

    # 将模型回复作为列表返回，便于附加到已有消息中
    return {"messages": [response]}


# 定义新的有向图

builder = StateGraph(State, input_schema=InputState, context_schema=Context)

# 定义会循环的两个节点
builder.add_node(call_model)
builder.add_node("tools", ToolNode(TOOLS))

# 将入口设置为 `call_model`，即从该节点开始执行
builder.add_edge("__start__", "call_model")


def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """根据模型输出决定下一个节点。

    检查最新的 AI 消息是否包含工具调用。

    Args:
        state (State): 当前对话状态。

    Returns:
        str: 下一节点名称（\"__end__\" 或 \"tools\"）。
    """
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )
    # 没有工具调用则直接结束
    if not last_message.tool_calls:
        return "__end__"
    # 否则执行所请求的工具
    return "tools"


# 条件边：决定 `call_model` 完成后的下一步
builder.add_conditional_edges(
    "call_model",
    # 依据 route_model_output 结果安排下一节点
    route_model_output,
)

# 普通边：工具执行完毕回到模型，形成循环
builder.add_edge("tools", "call_model")

# 将构建器编译为可执行图
graph = builder.compile(name="ReAct Agent")
