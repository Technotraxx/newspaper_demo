import streamlit as st
from newspaper import Article
from newspaper.configuration import Configuration

# Streamlit App
st.title("Newspaper Article Extractor")

# URL Eingabefeld
url = st.text_input("Enter the URL of the news article:")

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
        "summary": article.summary
    }

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
