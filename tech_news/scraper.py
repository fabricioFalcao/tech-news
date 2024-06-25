import time
import requests
from bs4 import BeautifulSoup


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    try:
        response = requests.get(url, headers=headers, timeout=3)

        if response.status_code == 200:
            return response.text
        else:
            return None

    except requests.exceptions.RequestException:
        return None

    finally:
        time.sleep(1)


# Requisito 2
def scrape_updates(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    soup.prettify()

    news = []

    for card in soup.find_all("article", {"class": "entry-preview"}):
        url = card.find("h2", {"class": "entry-title"}).a["href"]
        news.append(url)

    return news


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
