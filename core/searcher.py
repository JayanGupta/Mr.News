"""
searcher.py — Web search and content scraping module for Mr.News.
Uses DuckDuckGo (no API key required) + BeautifulSoup for content extraction.
Comprehensive query coverage with robust URL fallback handling.
"""

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import time
import datetime


# Max characters of scraped content to pass to Gemini
MAX_CONTEXT_CHARS = 35000
# Timeout for each URL fetch
REQUEST_TIMEOUT = 10
# Max URLs to scrape per query
MAX_URLS_PER_QUERY = 3

CURRENT_YEAR = datetime.datetime.now().year

# Common headers to mimic a real browser for better scraping success
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def _fetch_page_text(url: str) -> str:
    """Fetch a URL and return clean visible text. Handles redirects and encoding."""
    try:
        resp = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
            verify=True,
        )
        resp.raise_for_status()

        # Handle encoding
        if resp.encoding and resp.encoding.lower() != "utf-8":
            resp.encoding = resp.apparent_encoding

        soup = BeautifulSoup(resp.text, "lxml")

        # Remove clutter tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside",
                         "form", "noscript", "iframe", "svg", "button"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        # Collapse excessive blank lines
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        return "\n".join(lines)
    except Exception:
        return ""


def _get_url(result: dict) -> str:
    """Extract URL from a DuckDuckGo result, handling different key names."""
    return result.get("href", "") or result.get("link", "") or result.get("url", "")


def search_topic(topic: str, status_callback=None) -> dict:
    """
    Run multiple DuckDuckGo searches for a topic and scrape results.
    Uses 12 diverse query variants covering technical, business, financial,
    and trending news angles.

    Returns:
        {
            "raw_context": str,    # Combined scraped text
            "sources": list[dict]  # [{title, url, snippet}, ...]
        }
    """
    # Mix of quoted and unquoted queries for better coverage
    queries = [
        # ── Core knowledge (unquoted for broader results) ──
        f"{topic} what is overview explained",
        f"{topic} features capabilities key specifications",
        f"{topic} how to use tutorial getting started",
        f"{topic} technical architecture how it works",

        # ── Business & market ──
        f"{topic} who uses companies customers use cases",
        f"{topic} vs competitors comparison alternatives {CURRENT_YEAR}",
        f"{topic} market share revenue valuation {CURRENT_YEAR}",

        # ── Trending & financial news ──
        f"{topic} latest news {CURRENT_YEAR}",
        f"{topic} revenue profit loss financial {CURRENT_YEAR}",
        f"{topic} controversy layoffs challenges {CURRENT_YEAR}",
        f"{topic} partnerships acquisitions deals {CURRENT_YEAR}",

        # ── Reviews & sentiment ──
        f"{topic} review pros cons user feedback {CURRENT_YEAR}",
    ]

    all_sources = []
    all_text_chunks = []
    seen_urls = set()

    ddgs = DDGS()

    for i, query in enumerate(queries):
        if status_callback:
            status_callback(f"🌐 Searching: *{query}*", step=i, total=len(queries))

        try:
            results = list(ddgs.text(query, max_results=MAX_URLS_PER_QUERY))
        except Exception:
            results = []

        for r in results:
            url = _get_url(r)
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            title = r.get("title", "") or url
            snippet = r.get("body", "") or r.get("snippet", "") or ""

            all_sources.append({
                "title": title,
                "url": url,
                "snippet": snippet,
            })

            # Try scraping the full page
            page_text = _fetch_page_text(url)

            if page_text and len(page_text) > 100:
                # Got real content from the page
                all_text_chunks.append(
                    f"\n\n--- SOURCE: {title} ({url}) ---\n{page_text[:4000]}"
                )
            elif snippet:
                # Fallback: use DuckDuckGo's snippet as context
                all_text_chunks.append(
                    f"\n\n--- SOURCE (snippet): {title} ({url}) ---\n{snippet}"
                )

        time.sleep(0.25)  # polite delay

    raw_context = "\n".join(all_text_chunks)[:MAX_CONTEXT_CHARS]

    return {
        "raw_context": raw_context,
        "sources": all_sources,
    }
