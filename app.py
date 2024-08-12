import streamlit as st
from options import single_article_option, multiple_articles_option, links_in_article_option, search_duckduckgo_option
from jina_reader import jina_reader_option

# Streamlit App
st.title("Newspaper Article Extractor & Searcher")

# Sidebar Options-Selector
option = st.sidebar.selectbox(
    "Choose an option",
    ("Single Article", "Multiple Articles", "Links in Article", "Search DuckDuckGo", "Jina.AI Reader")
)

# Globale Variablen für Markdown zum Download
markdown_to_download = ""
markdown_with_summary_to_download = ""

# Optionen für die verschiedenen Modi
if option == "Single Article":
    markdown_to_download, markdown_with_summary_to_download = single_article_option()

elif option == "Multiple Articles":
    markdown_to_download, markdown_with_summary_to_download = multiple_articles_option()

elif option == "Links in Article":
    markdown_to_download, markdown_with_summary_to_download = links_in_article_option()

elif option == "Search DuckDuckGo":
    search_duckduckgo_option()

elif option == "Jina.AI Reader":
    jina_reader_option()

# Platz für den Download-Button oben
st.divider()
if markdown_to_download:
    st.download_button(
        label="Download Articles (Text Only)",
        data=markdown_to_download,
        file_name="articles.md",
        mime="text/markdown"
    )
    st.download_button(
        label="Download with Summary and Media",
        data=markdown_with_summary_to_download,
        file_name="articles_with_summary.md",
        mime="text/markdown"
    )
