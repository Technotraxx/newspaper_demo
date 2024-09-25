import streamlit as st
from options import single_article_option, multiple_articles_option, links_in_article_option, search_duckduckgo_option
from jina_reader import jina_reader_option

import nltk
import os

@st.cache_resource
def ensure_nltk_data():
    nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
    os.makedirs(nltk_data_dir, exist_ok=True)
    nltk.data.path.append(nltk_data_dir)
    nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)

ensure_nltk_data()

# Streamlit App
st.title("Newspaper Article Extractor & Searcher")

# Sidebar API Key Inputs
st.sidebar.header("API Keys")
jina_api_key = st.sidebar.text_input("Enter your Jina.AI API key:", type="password", key="jina_api_key")
gemini_api_key = st.sidebar.text_input("Enter your Google Gemini LLM API key:", type="password", key="gemini_api_key")

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
    jina_reader_option(jina_api_key, gemini_api_key)

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
