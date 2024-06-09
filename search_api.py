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

# Usage in Streamlit app
if option == "Search DuckDuckGo":
    st.header("Search DuckDuckGo")
    query = st.text_input("Enter a search term:")
    category = st.selectbox("Choose a category", ["news", "text", "images", "videos", "maps", "translate"])
    time = st.selectbox("Choose a time range", ["d", "w", "m", "y", None], index=4)
    site = st.text_input("Enter a specific site to search within (optional):")
    exclude_site = st.text_input("Enter a site to exclude from the search (optional):")
    if st.button("Search"):
        if query:
            results = search_duckduckgo(query, category=category, time=time, site=site, exclude_site=exclude_site)
            st.subheader("Found Articles:")
            urls = "\n".join(results)
            st.code(urls, language='text')
        else:
            st.warning("Please enter a search term.")
