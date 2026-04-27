from typing import Any, Dict, List, Tuple

import httpx

from .common import clean_text

schema = {
    "type": "function",
    "function": {
        "name": "bocha_search",
        "description": "Search the web ONLY when the user explicitly asks about recent news, real-time events, or facts you are clearly unsure about.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "count": {"type": "integer", "description": "Number of results to return (1-15)"},
            },
            "required": ["query"],
        },
    },
}


async def run(args: Dict[str, Any], config) -> Tuple[str, List[Dict[str, Any]]]:
    if not config.BOCHA_API_KEY:
        return "博查搜索未配置 BOCHA_API_KEY。", []

    query = str(args.get("query") or "").strip()
    count = int(args.get("count") or config.BOCHA_SEARCH_COUNT)
    count = max(1, min(count, config.BOCHA_SEARCH_COUNT))
    payload = {"query": query, "count": count}
    headers = {"Authorization": f"Bearer {config.BOCHA_API_KEY}", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=config.WEB_FETCH_TIMEOUT) as client:
        resp = await client.post(config.BOCHA_API_BASE, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    # 提取摘要格式返回
    web_pages = []
    try:
        web_pages = data.get("data", {}).get("webPages", {}).get("value", [])
    except (AttributeError, TypeError):
        pass

    if not web_pages:
        return f"搜索「{query}」未找到相关结果。", []

    # 格式化返回摘要
    results = []
    for i, page in enumerate(web_pages[:count], 1):
        title = page.get("name", "未知标题")
        url = page.get("url", "")
        snippet = page.get("snippet", "无摘要")
        results.append(f"{i}. {title}\n   {snippet}\n   {url}")

    summary = f"搜索「{query}」找到 {len(results)} 条结果：\n\n" + "\n\n".join(results)
    return summary, []
