import streamlit as st
from newspaper import Article
from newspaper.configuration import Configuration
import nltk
from urllib.parse import urljoin, urlparse
import base64
from search_api import search_news
import requests

# Sicherstellen, dass der Punkt-Tokenizer heruntergeladen ist
nltk.download('punkt', quiet=True)

# Streamlit App
st.title("Newspaper Article Extractor & Searcher")

# Sidebar Options-Selector
option = st.sidebar.selectbox(
    "Choose an option",
    ("Single Article", "Multiple Articles", "Links in Article", "Search News")
)

def get_article_info_with_retry(url, retries=3):
    config = Configuration()
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    article = Article(url, config=config)
    for _ in range(retries):
        try:
            article.download()
            article.parse()
            article.nlp()
            if not article.text:  # Falls der Artikeltext leer ist, den HTML-Inhalt debuggen
                st.write(f"HTML content for debugging: {article.html}")
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
        markdowns = []
        markdowns_with_summary = []
        for idx, url in enumerate(url_list):
            try:
                # Informationen extrahieren
                info = get_article_info_with_retry(url)
                
                # Markdown generieren
                markdown = generate_markdown(info, url, include_summary=False)
                markdown_with_summary = generate_markdown(info, url, include_summary=True)
                markdowns.append(markdown)
                markdowns_with_summary.append(markdown_with_summary)

                # Divider zwischen Artikeln
                if idx > 0:
                    st.divider()

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
                st.error(f"An error occurred with URL {url}: {e}")

        # Gesamtes Markdown für alle Artikel generieren
        full_markdown = "\n\n---\n\n".join(markdowns)
        full_markdown_with_summary = "\n\n---\n\n".join(markdowns_with_summary)
        markdown_to_download = full_markdown
        markdown_with_summary_to_download = full_markdown_with_summary

        st.divider()
        st.download_button(
            label="Download Articles",
            data=full_markdown,
            file_name="articles.md",
            mime="text/markdown"
        )
        st.download_button(
            label="Download with Summary",
            data=full_markdown_with_summary,
            file_name="articles_with_summary.md",
            mime="text/markdown"
        )

elif option == "Links in Article":
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            # Informationen extrahieren
            info = get_article_info_with_retry(url)
            # Links sortieren, filtern und anpassen
            unique_sorted_links = filter_and_adjust_links(info["links"], url)
            
            # Markdown generieren
            markdown = generate_markdown(info, url, include_summary=False)
            markdown_with_summary = generate_markdown(info, url, include_summary=True)
            markdown += "\n\n## Links in the Article\n\n"
            markdown_with_summary += "\n\n## Links in the Article\n\n"
            markdown += "\n".join(unique_sorted_links)
            markdown_with_summary += "\n".join(unique_sorted_links)
            markdown_to_download = markdown
            markdown_with_summary_to_download = markdown_with_summary

            st.divider()
            st.download_button(
                label="Download Articles",
                data=markdown,
                file_name="article_with_links.md",
                mime="text/markdown"
            )
            st.download_button(
                label="Download with Summary",
                data=markdown_with_summary,
                file_name="article_with_links_and_summary.md",
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
                for link in unique_sorted_links:
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

elif option == "Search News":
    st.header("Search News Articles")
    query = st.text_input("Enter a search term:")
    if st.button("Search"):
        if query:
            results = search_news(query)
            st.subheader("Found Articles:")
            urls = "\n".join(results)
            st.code(urls, language='text')
        else:
            st.warning("Please enter a search term.")
