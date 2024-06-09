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
        "links": article.extractor.get_urls(article.html),
        "images": filter_images(article.images),
        "videos": article.movies
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

if option == "Single Article":
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            # Informationen extrahieren
            info = get_article_info(url)
            
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

            st.text_area("Article Text", info["text"], height=300)

            with st.expander("Summary"):
                st.write(info["summary"])

            if info['images']:
                st.header("Images")
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
                info = get_article_info(url)
                
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

                st.text_area("Article Text", info["text"], height=300)

                with st.expander("Summary"):
                    st.write(info["summary"])

                if info['images']:
                    st.header("Images")
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
            info = get_article_info(url)
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

            st.text_area("Article Text", info["text"], height=300)

            with st.expander("Summary"):
                st.write(info["summary"])

            with st.expander("Links in the Article"):
                for link in unique_sorted_links:
                    st.write(link)

            if info['images']:
                st.header("Images")
                for img in info['images']:
                    st.image(img, use_column_width=True)

            if info['videos']:
                st.header("Videos")
                for video in info['videos']:
                    st.video(video)

        except Exception as e:
            st.error(f"An error occurred: {e}")
