from duckduckgo_search import DDGS

def search_news(query):
    ddgs = DDGS()
    results = ddgs.news(keywords=query, max_results=10)
    return [result['url'] for result in results]
