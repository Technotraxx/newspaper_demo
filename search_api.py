from duckduckgo_search import DDGS

def search_news(query):
    ddgs = DDGS()
    results = ddgs.news(keywords=f"{query} -site:msn.com", max_results=15)
    return [result['url'] for result in results if 'msn.com' not in result['url']]
