from __future__ import annotations
import random
import requests

GUARDIAN_API_KEY = "b1ec3d19-17a3-499c-822c-246cf2def0d0"
GUARDIAN_URL = "https://content.guardianapis.com/search"
GUARDIAN_CONTENT_URL = "https://content.guardianapis.com"
SPORTS_QUERIES = [
    "sports",
    "football",
    "soccer",
    "basketball",
    "baseball",
    "tennis",
    "golf",
    "cricket",
    "rugby",
    "formula one",
    "motorsport",
    "olympics",
    "athletics",
    "nfl",
    "nba",
    "mlb",
    "nhl",
    "premier league",
    "champions league",
    "world cup",
]


def get_sports_news(featured_count: int = 10) -> dict:
    params = {
        "api-key": GUARDIAN_API_KEY,
        "q": random.choice(SPORTS_QUERIES),
        "section": "sport",
        "page-size": 50,
        "page": random.randint(1, 5),
        "show-fields": "trailText,thumbnail,byline",
        "order-by": "newest",
    }

    response = requests.get(
        GUARDIAN_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    articles = data["response"]["results"]
    random.shuffle(articles)

    return {
        "category": "sports",
        "count": min(featured_count, len(articles)),
        "articles": [
            {
                "id": article["id"],
                "title": article["webTitle"],
                "url": article["webUrl"],
                "published": article["webPublicationDate"],
                "section": article["sectionName"],
                "description": article.get("fields", {}).get("trailText"),
                "thumbnail": article.get("fields", {}).get("thumbnail"),
                "author": article.get("fields", {}).get("byline"),
            }
            for article in articles[:featured_count]
        ],
    }





class SportsController:
    def get(self, event):
        return {
            "module": "SPORTS",
            "action": "GET"
        }

    def post(self, event):
        return get_sports_news()


if __name__ == "__main__":
    controller = SportsController()
    print(controller.post({"module": "SPORTS", "action": "POST"}))
