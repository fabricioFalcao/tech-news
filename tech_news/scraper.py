import time
import requests
from bs4 import BeautifulSoup

from tech_news.database import create_news


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
    soup = BeautifulSoup(html_content, "html.parser")
    soup.prettify()

    try:
        return soup.find("a", {"class": "next page-numbers"})["href"]
    except TypeError:
        return None


# Requisito 4
def scrape_news(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    soup.prettify()

    scrape_news = {}

    scrape_news["url"] = soup.find("link", {"rel": "canonical"})["href"]

    scrape_news["title"] = soup.find(
        "h1", {"class": "entry-title"}
    ).text.strip()

    scrape_news["timestamp"] = soup.find(
        "li", {"class": "meta-date"}
    ).text.strip()

    scrape_news["writer"] = soup.find("span", {"class": "author"}).text.strip()

    scrape_news["reading_time"] = int(
        soup.find("li", {"class": "meta-reading-time"}).text.split()[0]
    )

    scrape_news["summary"] = soup.find(
        "div", {"class": "entry-content"}
    ).p.text.strip()

    scrape_news["category"] = (
        soup.find("a", {"class": "category-style"})
        .find("span", {"class": "label"})
        .text.strip()
    )

    return scrape_news


# Requisito 5
def get_tech_news(amount):
    news = []
    html_content = fetch("https://blog.betrybe.com/")

    while len(news) < amount:
        news_urls = scrape_updates(html_content)

        for url in news_urls:
            if len(news) >= amount:
                break

            news.append(scrape_news(fetch(url)))

        next_page = scrape_next_page_link(html_content)
        if next_page:
            html_content = fetch(next_page)
        else:
            break

    create_news(news)
    return news
