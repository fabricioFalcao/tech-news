from tech_news.database import get_collection


# Requisito 10
def top_5_categories():
    collection = get_collection()
    pipeline = [
        {"$unwind": "$category"},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1, "_id": 1}},
        {"$limit": 5},
    ]
    categories = list(collection.aggregate(pipeline))
    top_5_categories = [category["_id"] for category in categories]
    return top_5_categories
