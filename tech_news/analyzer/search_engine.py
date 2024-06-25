from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    found_news = search_news({"title": {"$regex": title, "$options": "i"}})
    return [(news["title"], news["url"]) for news in found_news]


# Requisito 8
def search_by_date(date):
    try:
        timestamp = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    found_news = search_news({"timestamp": timestamp})
    return [(news["title"], news["url"]) for news in found_news]


# Requisito 9
def search_by_category(category):
    found_news = search_news(
        {"category": {"$regex": category, "$options": "i"}}
    )
    return [(news["title"], news["url"]) for news in found_news]
