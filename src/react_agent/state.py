"""定义智能体使用的状态结构。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep
from typing_extensions import Annotated


@dataclass
class InputState:
    """定义智能体的输入状态，作为对外部世界的收敛接口。

    用于约束初始状态及传入数据的结构。
    """

    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    """
    消息列表记录智能体的主执行状态，通常累积如下模式：
    1. HumanMessage：用户输入
    2. 带 .tool_calls 的 AIMessage：智能体选择工具收集信息
    3. ToolMessage：工具执行后的结果或错误
    4. 不含 .tool_calls 的 AIMessage：智能体向用户给出非结构化回复
    5. HumanMessage：用户开启下一轮对话

    步骤 2-5 会按需重复。

    `add_messages` 注解确保新消息会与现有消息按 ID 归并，保持“追加优先”的状态。
    """


@dataclass
class State(InputState):
    """代表智能体的完整状态，在输入状态基础上拓展额外属性。

    可用于存储智能体生命周期内的各类信息。
    """

    is_last_step: IsLastStep = field(default=False)
    """
    指示当前步骤是否已到达图抛出错误前的最后一步。

    这是由状态机托管的变量，非用户代码直接控制。
    当步数达到 recursion_limit - 1 时置为 True。
    """

    # 可按需在此扩展更多属性，例如：
    # retrieved_documents: List[Document] = field(default_factory=list)
    # extracted_entities: Dict[str, Any] = field(default_factory=dict)
    # api_connections: Dict[str, Any] = field(default_factory=dict)
