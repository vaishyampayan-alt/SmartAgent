from langchain.tools import tool
from duckduckgo_search import DDGS


@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return the top 3 results.
    Use this tool when you need to find current information, facts, news,
    or anything that requires looking up information online.
    Input should be a clear search query string.
    """
    try:
        results = []
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=3))

        if not search_results:
            return "No results found for the given query."

        for i, result in enumerate(search_results, 1):
            title = result.get("title", "No title")
            body = result.get("body", "No description available")
            href = result.get("href", "")
            results.append(
                f"Result {i}:\n"
                f"  Title: {title}\n"
                f"  Summary: {body}\n"
                f"  URL: {href}"
            )

        return "\n\n".join(results)

    except Exception as e:
        return f"Search failed with error: {str(e)}"
