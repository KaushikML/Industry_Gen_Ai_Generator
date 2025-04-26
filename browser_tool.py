import requests
from bs4 import BeautifulSoup

class BrowserTool:
    """
    A simple browser tool using Wikipedia API for search and requests+BeautifulSoup for web scraping.
    """
    WIKI_SEARCH_URL = 'https://en.wikipedia.org/w/api.php'

    def search_wikipedia(self, query: str) -> str:
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json'
        }
        res = requests.get(self.WIKI_SEARCH_URL, params=params).json()
        first = res['query']['search'][0]['title']
        return first

    def fetch_summary(self, title: str) -> str:
        params = {
            'action': 'query',
            'prop': 'extracts',
            'exintro': True,
            'titles': title,
            'format': 'json',
            'explaintext': True
        }
        res = requests.get(self.WIKI_SEARCH_URL, params=params).json()
        pages = res['query']['pages']
        extract = next(iter(pages.values()))['extract']
        return extract

    def scrape_segments(self, url: str) -> list:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        segments = []
        for header in soup.find_all(['h2', 'h3']):
            if 'Products' in header.text or 'Segments' in header.text:
                ul = header.find_next_sibling('ul')
                if ul:
                    segments = [li.text.strip() for li in ul.find_all('li')]
                    break
        return segments