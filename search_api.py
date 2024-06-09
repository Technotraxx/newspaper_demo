import requests
from bs4 import BeautifulSoup
import streamlit as st

def search_news(query):
    url = f"https://duckduckgo.com/html/?q={query}&iar=news"
    response = requests.get(url)
    
    # Debugging: Statuscode und Inhalt der Antwort anzeigen
    st.write(f"Status Code: {response.status_code}")
    st.text(f"Response Content: {response.content}")

    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    for link in soup.find_all('a', class_='result__a'):
        links.append(link.get('href'))

    return links[:10]
