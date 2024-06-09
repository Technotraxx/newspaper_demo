# search_api.py

import requests
from bs4 import BeautifulSoup

def search_news(query):
    url = f"https://duckduckgo.com/html/?q={query}&iar=news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    for link in soup.find_all('a', class_='result__a'):
        links.append(link.get('href'))

    return links[:10]
