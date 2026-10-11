from typing import Type

import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from ddgs import DDGS
from pydantic import BaseModel, Field



class WebSearchInput(BaseModel):
    query: str = Field(..., description="The search query, e.g. 'latest trends in RAG'")
    max_results: int = Field(5, description="Number of results to return (1-10)")


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Search the web for up-to-date information. Returns title, URL and snippet "
        "for each result. Use it to research topics and collect sources."
    )
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        max_results = max(1, min(int(max_results), 10))
        try:
            results = DDGS().text(query, max_results=max_results)
        except Exception as e:
            return f"Search failed: {e}. Try rephrasing the query or retry shortly."
        if not results:
            return "No results found. Try a broader or differently worded query."
        return "\n\n".join(
            f"[{i}] {r.get('title', '').strip()}\n"
            f"URL: {r.get('href', '')}\n"
            f"Snippet: {r.get('body', '').strip()}"
            for i, r in enumerate(results, 1)
        )


class PageReaderInput(BaseModel):
    url: str = Field(..., description="Full URL of the page to read (include https://)")
    max_chars: int = Field(4000, description="Maximum characters of page text to return")


class PageReaderTool(BaseTool):
    name: str = "read_webpage"
    description: str = (
        "Fetch a web page and return its main text. Use on a promising URL from "
        "web_search when the snippet isn't enough."
    )
    args_schema: Type[BaseModel] = PageReaderInput

    def _run(self, url: str, max_chars: int = 4000) -> str:
        try:
            resp = requests.get(
                url, timeout=15,
                headers={"User-Agent": "Mozilla/5.0 (compatible; BlogFlowBot/1.0)"},
            )
            resp.raise_for_status()
        except Exception as e:
            return f"Could not fetch {url}: {e}"
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()
        text = " ".join(soup.get_text(separator=" ").split())
        return text[:max_chars] + ("... [truncated]" if len(text) > max_chars else "")