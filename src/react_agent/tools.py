"""提供网页抓取与搜索的示例工具。

内置基础的 Tavily 搜索功能，供快速上手。
这些工具仅用于示范，生产环境建议实现更健壮、场景化的定制工具。
"""

from typing import Any, Callable, List, Optional, cast

from langchain_tavily import TavilySearch
from langgraph.runtime import get_runtime

from react_agent.context import Context


async def search(query: str) -> Optional[dict[str, Any]]:
    """执行通用网页搜索。

    使用 Tavily 搜索引擎，便于获得全面、准确、可信的结果，尤其适合查询时效性问题。
    """
    runtime = get_runtime(Context)
    wrapped = TavilySearch(max_results=runtime.context.max_search_results)
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))


TOOLS: List[Callable[..., Any]] = [search]
