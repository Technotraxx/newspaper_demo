import streamlit as st
from newspaper import Article
from newspaper.configuration import Configuration
import nltk
from urllib.parse import urljoin, urlparse

# Sicherstellen, dass der Punkt-Tokenizer heruntergeladen ist
nltk.download('punkt')

# Streamlit App
st.title("Newspaper Article Extractor")

# Sidebar Options-Selector
option = st.sidebar.selectbox(
    "Choose an option",
    ("Single Article", "Multiple Articles", "Links in Article")
)

# Funktion zum Extrahieren von Artikelinformationen
def get_article_info(url):
    config = Configuration()
    article = Article(url, config=config)
    article.download()
    article.parse()
    article.nlp()
    return {
        "title": article.title,
        "authors": article.authors,
        "publish_date": article.publish_date,
        "text": article.text,
        "summary": article.summary,
        "links": article.extractor.get_urls(article.html)
    }

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

if option == "Single Article":
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            # Informationen extrahieren
            info = get_article_info(url)
            # Anzeige der extrahierten Informationen
            st.header("Title")
            st.write(info["title"])

            st.header("Authors")
            st.write(", ".join(info["authors"]))

            st.header("Publish Date")
            st.write(info["publish_date"])

            st.header("Article Text")
            st.write(info["text"])

            st.header("Summary")
            st.write(info["summary"])

        except Exception as e:
            st.error(f"An error occurred: {e}")

elif option == "Multiple Articles":
    urls = st.text_area("Enter the URLs of the news articles (one per line):")
    if urls:
        url_list = urls.split('\n')
        for url in url_list:
            try:
                # Informationen extrahieren
                info = get_article_info(url)
                # Anzeige der extrahierten Informationen
                st.header("Title")
                st.write(info["title"])

                st.header("Authors")
                st.write(", ".join(info["authors"]))

                st.header("Publish Date")
                st.write(info["publish_date"])

                st.header("Article Text")
                st.write(info["text"])

                st.header("Summary")
                st.write(info["summary"])

            except Exception as e:
                st.error(f"An error occurred with URL {url}: {e}")

elif option == "Links in Article":
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            # Informationen extrahieren
            info = get_article_info(url)
            # Links sortieren, filtern und anpassen
            unique_sorted_links = filter_and_adjust_links(info["links"], url)
            
            # Anzeige der extrahierten Informationen
            st.header("Title")
            st.write(info["title"])

            st.header("Authors")
            st.write(", ".join(info["authors"]))

            st.header("Publish Date")
            st.write(info["publish_date"])

            st.header("Article Text")
            st.write(info["text"])

            st.header("Summary")
            st.write(info["summary"])

            with st.expander("Links in the Article"):
                for link in unique_sorted_links:
                    st.write(link)

        except Exception as e:
            st.error(f"An error occurred: {e}")
