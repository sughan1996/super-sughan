from __future__ import annotations

import random
from typing import Any, Dict

import requests

GUARDIAN_API_KEY = "b1ec3d19-17a3-499c-822c-246cf2def0d0"
GUARDIAN_URL = "https://content.guardianapis.com/search"

SOCIETY_QUERIES= [
    "society",
    "medicine",
    "public society",
    "mental society",
    "wellness",
    "disease",
]


def fetch_guardian_health_news(
    featured_count: int = 32,
    page_size: int = 50,
) -> Dict[str, Any]:
    """
    Fetch society-related news from The Guardian API.
    """

    params = {
        "api-key": GUARDIAN_API_KEY,
        "q": random.choice(SOCIETY_QUERIES),
        "section": "society",  # more relevant than "world" for society topics
        "page-size": page_size,
        "page": random.randint(1, 5),
        "show-fields": "trailText,thumbnail,byline",
        "order-by": "newest",
    }

    response = requests.get(GUARDIAN_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = data.get("response", {}).get("results", [])

    random.shuffle(results)

    return {
        "category": "society",
        "count": min(featured_count, len(results)),
        "articles": [_parse_article(a) for a in results[:featured_count]],
    }


def _parse_article(article: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Guardian article format."""
    fields = article.get("fields", {})

    return {
        "id": article.get("id"),
        "title": article.get("webTitle"),
        "url": article.get("webUrl"),
        "published": article.get("webPublicationDate"),
        "section": article.get("sectionName"),
        "description": fields.get("trailText"),
        "thumbnail": fields.get("thumbnail"),
        "author": fields.get("byline"),
    }


class SocietyController:
    def get(self, event: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "module": "HEALTH_NEWS",
            "action": "GET",
        }

    def post(self, event: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return fetch_guardian_health_news()


if __name__ == "__main__":
    controller = SocietyController()
    result = controller.post()
    print(result)