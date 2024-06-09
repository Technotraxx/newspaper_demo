from duckduckgo_search import DDGS

def search_duckduckgo(query, category='news', time=None, site=None, exclude_site=None, max_results=15):
    ddgs = DDGS()
    
    if exclude_site:
        query += f" -site:{exclude_site}"
    if site:
        query += f" site:{site}"
    
    search_function = {
        'news': ddgs.news,
        'text': ddgs.text,
        'images': ddgs.images,
        'videos': ddgs.videos,
        'maps': ddgs.maps,
        'translate': ddgs.translate
    }.get(category, ddgs.text)

    try:
        results = search_function(keywords=query, timelimit=time, max_results=max_results)
        return [result['url'] for result in results if 'url' in result]
    except Exception as e:
        print(f"Error during search: {e}")
        return []

# Testen Sie die Funktion
if __name__ == "__main__":
    # Beispielabfrage
    query = "python programming"
    category = "text"
    results = search_duckduckgo(query, category=category, max_results=10)
    print(results)
