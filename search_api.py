from duckduckgo_search import DDGS

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

    # Filter out MSN results
    filtered_results = [result for result in results if "msn.com" not in result.get('href', '')]

    # Use 'href' instead of 'url' for text category
    if category == "text":
        return [result['href'] for result in filtered_results]
    else:
        return [result['url'] for result in filtered_results]
