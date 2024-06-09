import streamlit as st
from article_utils import get_article_info_with_retry, generate_markdown, filter_and_adjust_links
from search_api import search_duckduckgo

def single_article_option():
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            info = get_article_info_with_retry(url)
            markdown = generate_markdown(info, url, include_summary=False)
            markdown_with_summary = generate_markdown(info, url, include_summary=True)

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

            return markdown, markdown_with_summary

        except Exception as e:
            st.error(f"An error occurred: {e}")
    return "", ""

def multiple_articles_option():
    urls = st.text_area("Enter the URLs of the news articles (one per line):")
    if urls:
        url_list = urls.split('\n')
        all_info = []
        for idx, url in enumerate(url_list):
            url = url.strip()
            if url:
                try:
                    info = get_article_info_with_retry(url)
                    all_info.append((idx, info, url))  # Speichere idx mit der info und url
                except Exception as e:
                    st.error(f"An error occurred with URL {url}: {e}")

        markdown = ""
        markdown_with_summary = ""
        for idx, info, url in all_info:
            markdown += generate_markdown(info, url, include_summary=False) + "\n\n"
            markdown_with_summary += generate_markdown(info, url, include_summary=True) + "\n\n"

        for idx, info, url in all_info:
            st.header(info['title'])
            st.write(url)
            st.write(f"Authors: {', '.join(info['authors'])} | Publish Date: {info['publish_date']}")
            st.text_area("Article Text", info["text"], height=300, key=f"text_{idx}")

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

        return markdown, markdown_with_summary
    return "", ""

def links_in_article_option():
    url = st.text_input("Enter the URL of the news article:")
    if url:
        try:
            info = get_article_info_with_retry(url)
            links = filter_and_adjust_links(info['links'], url)
            markdown = generate_markdown(info, url, include_summary=False)
            markdown_with_summary = generate_markdown(info, url, include_summary=True)

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

            return markdown, markdown_with_summary

        except Exception as e:
            st.error(f"An error occurred: {e}")
    return "", ""

def search_duckduckgo_option():
    st.header("Search DuckDuckGo")
    query = st.text_input("Enter a search term:")
    category = st.selectbox("Choose a category", ["news", "text", "images", "videos", "maps", "translate"])
    time = st.selectbox("Choose a time range", ["d", "w", "m", "y", None], index=4)
    site = st.text_input("Enter a specific site to search within (optional):")
    exclude_site = st.text_input("Enter a site to exclude from the search (optional):")
    region = st.selectbox("Choose a region", ["wt-wt", "us-en", "uk-en", "de-de", "fr-fr", "es-es", "it-it", "nl-nl", "ru-ru", "jp-jp", "cn-zh"])

    if st.button("Search"):
        if query:
            results = search_duckduckgo(query, category=category, time=time, site=site, exclude_site=exclude_site, region=region)
            st.subheader("Found Articles:")
            urls = "\n".join(results)
            st.code(urls, language='text')
        else:
            st.warning("Please enter a search term.")
