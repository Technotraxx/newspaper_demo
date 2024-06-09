import streamlit as st
from newspaper import Article
from newspaper.configuration import Configuration
import nltk
from urllib.parse import urljoin, urlparse
import base64  # Importiere das base64 Modul

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

def generate_markdown(info, url):
    markdown = f"# {info['title']} \n\n"
    markdown += f"**URL:** {url}\n\n"
    markdown += f"**Authors:** {', '.join(info['authors'])}\n\n"
    markdown += f"**Publish Date:** {info['publish_date']}\n\n"
    markdown += f"**Article Text:**\n\n{info['text']}\n\n"
    markdown += f"**Summary:**\n\n{info['summary']}\n\n"
    return markdown

def download_button(text, filename, label):
    b64 = base64.b64encode(text.encode()).decode()  # some strings
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

if option == "Single Article":
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            # Informationen extrahieren
            info = get_article_info(url)
            # Anzeige der extrahierten Informationen
            st.header(f"Title: {info['title']}")
            st.write(f"URL: {url}")

            st.header("Authors")
            st.write(", ".join(info["authors"]))

            st.header("Publish Date")
            st.write(info["publish_date"])

            st.header("Article Text")
            st.write(info["text"])

            st.header("Summary")
            st.write(info["summary"])

            # Markdown generieren
            markdown = generate_markdown(info, url)
            
            # Download-Button
            download_button(markdown, "article.md", "Download Article as Markdown")

        except Exception as e:
            st.error(f"An error occurred: {e}")

elif option == "Multiple Articles":
    urls = st.text_area("Enter the URLs of the news articles (one per line):")
    if urls:
        url_list = urls.split('\n')
        markdowns = []
        for url in url_list:
            try:
                # Informationen extrahieren
                info = get_article_info(url)
                # Anzeige der extrahierten Informationen
                st.header(f"Title: {info['title']}")
                st.write(f"URL: {url}")

                st.header("Authors")
                st.write(", ".join(info["authors"]))

                st.header("Publish Date")
                st.write(info["publish_date"])

                st.header("Article Text")
                st.write(info["text"])

                st.header("Summary")
                st.write(info["summary"])

                # Markdown generieren
                markdown = generate_markdown(info, url)
                markdowns.append(markdown)

            except Exception as e:
                st.error(f"An error occurred with URL {url}: {e}")

        # Gesamtes Markdown für alle Artikel generieren
        full_markdown = "\n\n---\n\n".join(markdowns)
        download_button(full_markdown, "articles.md", "Download Articles as Markdown")

elif option == "Links in Article":
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            # Informationen extrahieren
            info = get_article_info(url)
            # Links sortieren, filtern und anpassen
            unique_sorted_links = filter_and_adjust_links(info["links"], url)
            
            # Anzeige der extrahierten Informationen
            st.header(f"Title: {info['title']}")
            st.write(f"URL: {url}")

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

            # Markdown generieren
            markdown = generate_markdown(info, url)
            markdown += "\n\n## Links in the Article\n\n"
            markdown += "\n".join(unique_sorted_links)

            # Download-Button
            download_button(markdown, "article_with_links.md", "Download Article with Links as Markdown")

        except Exception as e:
            st.error(f"An error occurred: {e}")
