"""定义智能体可配置的参数。"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated

from . import prompts


@dataclass(kw_only=True)
class Context:
    """智能体运行时的上下文配置。"""

    system_prompt: str = field(
        default=prompts.SYSTEM_PROMPT,
        metadata={
            "description": "智能体交互所使用的系统提示词，决定整体的语气与行为。"
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="anthropic/claude-sonnet-4-5-20250929",
        metadata={
            "description": "智能体主要对话所用的语言模型名称，格式：provider/model-name。"
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "单次搜索返回的最大结果数量。"
        },
    )

    def __post_init__(self) -> None:
        """为未显式传入的属性自动读取环境变量。"""
        for f in fields(self):
            if not f.init:
                continue

            if getattr(self, f.name) == f.default:
                setattr(self, f.name, os.environ.get(f.name.upper(), f.default))
