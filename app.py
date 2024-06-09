import streamlit as st
from search_api import search_duckduckgo
import requests
from newspaper import Article
from newspaper.configuration import Configuration
import nltk
from urllib.parse import urljoin, urlparse
import base64
from bs4 import BeautifulSoup

# Sicherstellen, dass der Punkt-Tokenizer heruntergeladen ist
nltk.download('punkt', quiet=True)

# Streamlit App
st.title("Newspaper Article Extractor & Searcher")

# Sidebar Options-Selector
option = st.sidebar.selectbox(
    "Choose an option",
    ("Single Article", "Multiple Articles", "Links in Article", "Search DuckDuckGo")
)

# Funktion zum Extrahieren von Artikelinformationen mit Wiederholungslogik
def get_article_info_with_retry(url, retries=3):
    config = Configuration()
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    article = Article(url, config=config)
    for _ in range(retries):
        try:
            article.download()
            article.parse()
            article.nlp()
            return {
                "title": article.title,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "text": article.text,
                "summary": article.summary,
                "links": article.extractor.get_urls(article.html),
                "images": filter_images(article.images),
                "videos": article.movies
            }
        except Exception as e:
            error_message = str(e)
    raise Exception(f"Article download() failed with {error_message} on URL {url}")

# Funktion zum Filtern und Anpassen der Links
def filter_and_adjust_links(links, base_url):
    filtered_links = []
    parsed_base_url = urlparse(base_url)
    base_domain = f"{parsed_base_url.scheme}://{parsed_base_url.netloc}"
    
    for link in links:
        if link.startswith("#") or link.startswith("javascript"):
            continue
        if link.startswith("/"):
            link = urljoin(base_domain, link)
        filtered_links.append(link)
    
    return sorted(set(filtered_links))

# Funktion zum Filtern von Bildern
def filter_images(images):
    filtered_images = []
    for img in images:
        if ("logo" in img.lower() or
            "banner" in img.lower() or
            "icon" in img.lower() or
            "assets" in img.lower() or
            img.lower().endswith('.svg')):
            continue
        filtered_images.append(img)
    return filtered_images

# Funktion zum Generieren von Markdown
def generate_markdown(info, url, include_summary=True):
    markdown = f"# {info['title']} \n\n"
    markdown += f"**URL:** {url}\n\n"
    markdown += f"**Authors:** {', '.join(info['authors'])}\n\n"
    markdown += f"**Publish Date:** {info['publish_date']}\n\n"
    markdown += f"**Article Text:**\n\n{info['text']}\n\n"
    if include_summary:
        markdown += f"**Summary:**\n\n{info['summary']}\n\n"
    if info['images']:
        markdown += "\n\n## Images\n\n"
        for img in info['images']:
            markdown += f"![Image]({img})\n\n"
    if info['videos']:
        markdown += "\n\n## Videos\n\n"
        for video in info['videos']:
            markdown += f"[Video]({video})\n\n"
    return markdown

# Globale Variablen für Markdown zum Download
markdown_to_download = ""
markdown_with_summary_to_download = ""

# Platz für den Download-Button oben
st.divider()
if markdown_to_download:
    st.download_button(
        label="Download Articles",
        data=markdown_to_download,
        file_name="articles.md",
        mime="text/markdown"
    )
    st.download_button(
        label="Download with Summary",
        data=markdown_with_summary_to_download,
        file_name="articles_with_summary.md",
        mime="text/markdown"
    )

# Optionen für die verschiedenen Modi
if option == "Single Article":
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            # Informationen extrahieren
            info = get_article_info_with_retry(url)
            
            # Markdown generieren
            markdown = generate_markdown(info, url, include_summary=False)
            markdown_with_summary = generate_markdown(info, url, include_summary=True)
            markdown_to_download = markdown
            markdown_with_summary_to_download = markdown_with_summary

            # Platz für den Download-Button
            st.divider()
            st.download_button(
                label="Download Articles",
                data=markdown,
                file_name="article.md",
                mime="text/markdown"
            )
            st.download_button(
                label="Download with Summary",
                data=markdown_with_summary,
                file_name="article_with_summary.md",
                mime="text/markdown"
            )

            # Anzeige der extrahierten Informationen
            st.header(info['title'])
            st.write(url)

            st.write(f"Authors: {', '.join(info['authors'])} | Publish Date: {info['publish_date']}")

            st.text_area("Article Text", info["text"], height=300, key=url)

            with st.expander("Summary"):
                st.write(info["summary"])

            if info['images']:
                with st.expander("Images"):
                    for img in info['images']:
                        st.image(img, use_column_width=True)

            if info['videos']:
                st.header("Videos")
                for video in info['videos']:
                    st.video(video)

        except Exception as e:
            st.error(f"An error occurred: {e}")

elif option == "Multiple Articles":
    urls = st.text_area("Enter the URLs of the news articles (one per line):")
    if urls:
        url_list = urls.split('\n')
        all_info = []
        for url in url_list:
            url = url.strip()
            if url:
                try:
                    info = get_article_info_with_retry(url)
                    all_info.append(info)
                except Exception as e:
                    st.error(f"An error occurred with URL {url}: {e}")

        # Markdown für alle Artikel generieren
        markdown = ""
        markdown_with_summary = ""
        for info in all_info:
            markdown += generate_markdown(info, url, include_summary=False) + "\n\n"
            markdown_with_summary += generate_markdown(info, url, include_summary=True) + "\n\n"
        
        markdown_to_download = markdown
        markdown_with_summary_to_download = markdown_with_summary

        # Platz für den Download-Button
        st.divider()
        st.download_button(
            label="Download Articles",
            data=markdown,
            file_name="articles.md",
            mime="text/markdown"
        )
        st.download_button(
            label="Download with Summary",
            data=markdown_with_summary,
            file_name="articles_with_summary.md",
            mime="text/markdown"
        )

        # Anzeigen der extrahierten Informationen für alle Artikel
        for info in all_info:
            st.header(info['title'])
            st.write(url)

            st.write(f"Authors: {', '.join(info['authors'])} | Publish Date: {info['publish_date']}")

            st.text_area("Article Text", info["text"], height=300, key=url)

            with st.expander("Summary"):
                st.write(info["summary"])

            if info['images']:
                with st.expander("Images"):
                    for img in info['images']:
                        st.image(img, use_column_width=True)

            if info['videos']:
                st.header("Videos")
                for video in info['videos']:
                    st.video(video)

elif option == "Links in Article":
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            # Informationen extrahieren
            info = get_article_info_with_retry(url)
            links = filter_and_adjust_links(info['links'], url)
            
            # Markdown generieren
            markdown = generate_markdown(info, url, include_summary=False)
            markdown_with_summary = generate_markdown(info, url, include_summary=True)
            markdown_to_download = markdown
            markdown_with_summary_to_download = markdown_with_summary

            # Platz für den Download-Button
            st.divider()
            st.download_button(
                label="Download Articles",
                data=markdown,
                file_name="article.md",
                mime="text/markdown"
            )
            st.download_button(
                label="Download with Summary",
                data=markdown_with_summary,
                file_name="article_with_summary.md",
                mime="text/markdown"
            )

            # Anzeige der extrahierten Informationen
            st.header(info['title'])
            st.write(url)

            st.write(f"Authors: {', '.join(info['authors'])} | Publish Date: {info['publish_date']}")

            st.text_area("Article Text", info["text"], height=300, key=url)

            with st.expander("Summary"):
                st.write(info["summary"])

            with st.expander("Links in the Article"):
                for link in links:
                    st.write(link)

            if info['images']:
                with st.expander("Images"):
                    for img in info['images']:
                        st.image(img, use_column_width=True)

            if info['videos']:
                st.header("Videos")
                for video in info['videos']:
                    st.video(video)

        except Exception as e:
            st.error(f"An error occurred: {e}")

elif option == "Search DuckDuckGo":
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
