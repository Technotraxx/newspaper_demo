import streamlit as st
from newspaper import Article
from newspaper.configuration import Configuration
import nltk

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

            # Links sortieren und filtern
            unique_sorted_links = sorted(set(info["links"]))

            with st.expander("Links in the Article"):
                for link in unique_sorted_links:
                    st.write(link)

        except Exception as e:
            st.error(f"An error occurred: {e}")
