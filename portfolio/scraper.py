from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup

def scrape_news(query):
    url = 'https://www.bbc.com/search?q=' + query
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        headlines = []
        for headline in soup.find_all('h3'):
            headlines.append(headline.text)

        return headlines
    
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {e}")
        return []