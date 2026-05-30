from __future__ import annotations
import random
import requests

GUARDIAN_API_KEY = "b1ec3d19-17a3-499c-822c-246cf2def0d0"
GUARDIAN_URL = "https://content.guardianapis.com/search"

LIFESTYLE_QUERIES = [
    "lifestyle",
    "wellbeing",
    "society",
    "mental society",
    "relationships",
    "love",
    "dating",
    "food",
    "recipes",
    "fashion",
    "beauty",
    "travel",
    "home",
    "fitness",
    "self improvement",
    "work life balance",
    "stress",
    "nutrition",
    "diet",
    "sleep",
]


def get_lifestyle_news(featured_count: int = 32) -> dict:
    params = {
        "api-key": GUARDIAN_API_KEY,
        "q": random.choice(LIFESTYLE_QUERIES),
        "section": "lifeandstyle",
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
        "category": "lifestyle",
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


class LifestyleController:
    def get(self, event):
        return {
            "module": "LIFESTYLE",
            "action": "GET"
        }

    def post(self, event):
        return get_lifestyle_news()


if __name__ == "__main__":
    controller = LifestyleController()
    print(controller.post({"module": "LIFESTYLE", "action": "POST"}))