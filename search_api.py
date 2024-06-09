from duckduckgo_search import DDGS
from urllib.parse import urlparse

def search_duckduckgo(query, category="news", time=None, site=None, exclude_site=None, region="wt-wt"):
    ddgs = DDGS()
    results = []

    if category == "news":
        results = ddgs.news(
            keywords=query,
            region=region,
            safesearch="moderate",
            timelimit=time,
            max_results=15,
        )
    elif category == "text":
        results = ddgs.text(
            keywords=query,
            region=region,
            safesearch="moderate",
            timelimit=time,
            backend="api",
            max_results=15,
        )
    elif category == "images":
        results = ddgs.images(
            keywords=query,
            region=region,
            safesearch="moderate",
            timelimit=time,
            max_results=15,
        )
    elif category == "videos":
        results = ddgs.videos(
            keywords=query,
            region=region,
            safesearch="moderate",
            timelimit=time,
            max_results=15,
        )
    elif category == "maps":
        results = ddgs.maps(
            keywords=query,
            region=region,
            max_results=15,
        )
    elif category == "translate":
        results = ddgs.translate(
            keywords=query,
            to="en",
        )

    # Filter out MSN results and the exclude_site
    filtered_results = []
    for result in results:
        url = result.get('url') or result.get('href')
        if url:
            domain = urlparse(url).netloc
            if "msn.com" not in domain and (not exclude_site or exclude_site not in domain):
                filtered_results.append(result)

    # Use 'href' instead of 'url' for text category
    if category == "text":
        return [result['href'] for result in filtered_results]
    else:
        return [result['url'] for result in filtered_results]

