from newspaper import Article
from newspaper.configuration import Configuration
from urllib.parse import urljoin, urlparse

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

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
def generate_markdown(info, url, include_summary=True, include_media=True):
    markdown = f"# {info['title']} \n\n"
    markdown += f"**URL:** {url}\n\n"
    markdown += f"**Authors:** {', '.join(info['authors'])}\n\n"
    markdown += f"**Publish Date:** {info['publish_date']}\n\n"
    markdown += f"**Article Text:**\n\n{info['text']}\n\n"
    
    if include_summary:
        markdown += f"**Summary:**\n\n{info['summary']}\n\n"
    
    if include_media:
        if info['images']:
            markdown += "\n\n## Images\n\n"
            for img in info['images']:
                markdown += f"![Image]({img})\n\n"
        if info['videos']:
            markdown += "\n\n## Videos\n\n"
            for video in info['videos']:
                markdown += f"[Video]({video})\n\n"
                
    return markdown

