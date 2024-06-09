from duckduckgo_search import DDGS
import streamlit as st

def search_duckduckgo(query, category="news", time=None, site=None, exclude_site=None):
    ddgs = DDGS()
    results = []

    if category == "news":
        results = ddgs.news(
            keywords=query,
            region="wt-wt",
            safesearch="moderate",
            timelimit=time,
            max_results=15,
        )
    elif category == "text":
        results = ddgs.text(
            keywords=query,
            region="wt-wt",
            safesearch="moderate",
            timelimit=time,
            backend="api",
            max_results=15,
        )
    elif category == "images":
        results = ddgs.images(
            keywords=query,
            region="wt-wt",
            safesearch="moderate",
            timelimit=time,
            max_results=15,
        )
    elif category == "videos":
        results = ddgs.videos(
            keywords=query,
            region="wt-wt",
            safesearch="moderate",
            timelimit=time,
            max_results=15,
        )
    elif category == "maps":
        results = ddgs.maps(
            keywords=query,
            region="wt-wt",
            max_results=15,
        )
    elif category == "translate":
        results = ddgs.translate(
            keywords=query,
            to="en",
        )

    # Debugging: Print the raw results
    st.write("Raw results from DuckDuckGo API:", results)

    # Filter out MSN results
    filtered_results = [result for result in results if "msn.com" not in result.get('url', '')]

    return [result['url'] for result in filtered_results]
