"""
PK = "USER_ID"
SK = ["TYPE#CREATE", "TYPE#UPDATE", "TYPE#REACT", "TYPE#SAVED"]
attributes = ["CREATED_AT", "UPDATED_AT", "CONTENT_ID"]
"""
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import requests

import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

from haikuFoundationApp.jobs.usersHandler import get_record as cid

GUARDIAN_API_KEY = "b1ec3d19-17a3-499c-822c-246cf2def0d0"
GUARDIAN_URL = "https://content.guardianapis.com/search"
GUARDIAN_CONTENT_URL = "https://content.guardianapis.com"

# ---------------- Config ----------------
# NOTE: keep the attribute names in DynamoDB items exactly as declared in the docstring.
# This ARN can be overridden via env var for different deployments.
DYNAMODB_RESOURCE_ARN = os.getenv(
    "USERS_ACTIVITY_DDB_ARN",
    "arn:aws:dynamodb:us-east-1:322828741334:table/haiku-foundation-users-activity-table",
)

# Actual DynamoDB key attribute names in the table schema
DDB_PK_ATTR = os.getenv("DDB_PK_ATTR", "userId")
DDB_SK_ATTR = os.getenv("DDB_SK_ATTR", "metaData")

ALLOWED_TYPES = {
    "TYPE#CREATE",
    "TYPE#UPDATE",
    "TYPE#REACT",
    "TYPE#SAVED",
}

# ---------------- AWS helpers ----------------

def _aws_region() -> str:
    return (
        os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or boto3.session.Session().region_name
        or "us-east-1"
    )


def _client():
    return boto3.client("dynamodb", region_name=_aws_region())


def _table_name_from_arn(arn: str) -> str:
    return arn.split("/", 1)[1] if "/" in arn else arn


# ---------------- (De)serialization ----------------

_SERIALIZER = TypeSerializer()
_DESERIALIZER = TypeDeserializer()


def _to_av_map(item: Dict[str, Any]) -> Dict[str, Any]:
    return {k: _SERIALIZER.serialize(v) for k, v in item.items()}


def _from_av_map(av_item: Dict[str, Any]) -> Dict[str, Any]:
    return {k: _DESERIALIZER.deserialize(v) for k, v in av_item.items()}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


# ---------------- Validators / builders ----------------

def _ensure_allowed(type_value: str) -> None:
    if type_value not in ALLOWED_TYPES:
        raise ValueError(f"type must be one of {sorted(ALLOWED_TYPES)}")


def _require_content_id(content_id: Any) -> None:
    if content_id is None:
        raise ValueError("content_id is required")
    if isinstance(content_id, str) and content_id.strip() == "":
        raise ValueError("content_id cannot be empty")


def _key_av(userId: str, type_value: str) -> Dict[str, Any]:
    return {
        DDB_PK_ATTR: _SERIALIZER.serialize(userId),
        DDB_SK_ATTR: _SERIALIZER.serialize(type_value),
    }


# ---------------- CRUD primitives ----------------

def insert_record(userId: str, type_value: str, content_id: Any) -> Dict[str, Any]:
    """Insert a new activity record (idempotent on PK/SK conflict).

    Item attributes (do not rename): CREATED_AT, UPDATED_AT, CONTENT_ID
    """
    _ensure_allowed(type_value)
    _require_content_id(content_id)

    now = _now_iso()
    item = {
        DDB_PK_ATTR: userId,
        DDB_SK_ATTR: type_value,
        "CONTENT_ID": content_id,
        "CREATED_AT": now,
        "UPDATED_AT": now,
    }

    client = _client()
    try:
        client.put_item(
            TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
            Item=_to_av_map(item),
            ConditionExpression="attribute_not_exists(#pk) AND attribute_not_exists(#sk)",
            ExpressionAttributeNames={"#pk": DDB_PK_ATTR, "#sk": DDB_SK_ATTR},
        )
        return item
    except client.exceptions.ConditionalCheckFailedException:
        existing = get_record(userId, type_value)
        if existing:
            return existing
        raise


def update_record(userId: str, type_value: str, content_id: Any) -> Dict[str, Any]:
    """Update CONTENT_ID and UPDATED_AT on an existing record. Fails if missing."""
    _ensure_allowed(type_value)
    _require_content_id(content_id)

    resp = _client().update_item(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        Key=_key_av(userId, type_value),
        UpdateExpression="SET #cid = :cid, #u = :upd",
        ExpressionAttributeNames={
            "#cid": "CONTENT_ID",
            "#u": "UPDATED_AT",
            "#pk": DDB_PK_ATTR,
            "#sk": DDB_SK_ATTR,
        },
        ExpressionAttributeValues={
            ":cid": _SERIALIZER.serialize(content_id),
            ":upd": _SERIALIZER.serialize(_now_iso()),
        },
        ConditionExpression="attribute_exists(#pk) AND attribute_exists(#sk)",
        ReturnValues="ALL_NEW",
    )
    attrs = resp.get("Attributes")
    return _from_av_map(attrs) if attrs else {DDB_PK_ATTR: userId, DDB_SK_ATTR: type_value, "CONTENT_ID": content_id}


def upsert_record(userId: str, type_value: str, content_id: Any) -> Dict[str, Any]:
    """Update if exists; otherwise insert."""
    try:
        return update_record(userId, type_value, content_id)
    except _client().exceptions.ConditionalCheckFailedException:
        return insert_record(userId, type_value, content_id)


def get_record(userId: str, type_value: str) -> Optional[Dict[str, Any]]:
    _ensure_allowed(type_value)
    resp = _client().get_item(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        Key=_key_av(userId, type_value),
        ConsistentRead=False,
    )
    av_item = resp.get("Item")
    return _from_av_map(av_item) if av_item else None


def get_user_activity_values(userId: str) -> List[Dict[str, Any]]:
    """Get all activity records for a user (all SKs under the PK)."""
    resp = _client().query(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        KeyConditionExpression="#pk = :pk",
        ExpressionAttributeNames={"#pk": DDB_PK_ATTR},
        ExpressionAttributeValues={":pk": _SERIALIZER.serialize(userId)},
        ConsistentRead=False,
    )
    items = resp.get("Items", [])
    return [_from_av_map(av) for av in items]


# ---------------- Domain helpers ----------------

def record_create(userId: str, content_id: Any) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#CREATE", content_id)


def record_update(userId: str, content_id: Any) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#UPDATE", content_id)


def record_react(userId: str, content_id: Any) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#REACT", content_id)


def record_saved(userId: str, article_id: str):
    now = _now_iso()

    item = {
        DDB_PK_ATTR: userId,
        DDB_SK_ATTR: f"TYPE#SAVED#{article_id}",
        "CONTENT_ID": article_id,
        "CREATED_AT": now,
        "UPDATED_AT": now,
    }

    _client().put_item(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        Item=_to_av_map(item),
    )

    return item


def save_user_records(userId: str):
    cid_record = cid(userId, "TYPE#COGNITO_ID")
    uid = cid_record['VALUE']
    return record_saved(uid)


def get_users_saved_records(userId: str):
    cid_record = cid(userId, "TYPE#COGNITO_ID")
    uid = cid_record['VALUE']
    return get_user_activity_values(uid)

def get_users_saved_articles(userId: str):
    records =  get_users_saved_records(userId)
    users_articles = []
    saved_article_ids = []
    for record in records:
        saved_article_ids.append(record)
    for article_record in saved_article_ids:
        content_id = article_record["CONTENT_ID"]
        users_articles.append(get_article_by_id(content_id))
    article_count = len(users_articles)
    if article_count > 0:
        resp = {'category': 'saved', 'count': article_count, 'articles': users_articles}
    else:
        resp = "you do not have any saved articles..."
    return resp


def get_article_by_id(article_id: str) -> dict:
    parse_url = GUARDIAN_CONTENT_URL + "/" + article_id
    response = requests.get(
        parse_url,
        params={
            "api-key": GUARDIAN_API_KEY,
            "show-fields": (
                "headline,trailText,body,bodyText,"
                "thumbnail,byline,main"
            ),
            "show-tags": "contributor",
        },
        timeout=10,
    )
    response.raise_for_status()
    article = response.json()
    article = article["response"]["content"]

    return {
        "id": article["id"],
        "title": article["webTitle"],
        "url": article["webUrl"],
        "published": article["webPublicationDate"],
        "section": article["sectionName"],
        "description": article.get("fields", {}).get("trailText"),
        "body": article.get("fields", {}).get("body"),
        "bodyText": article.get("fields", {}).get("bodyText"),
        "thumbnail": article.get("fields", {}).get("thumbnail"),
        "author": article.get("fields", {}).get("byline"),
    }




# ---------------- CLI demo (optional) ----------------
if __name__ == "__main__":
    article_0 = 'sport/2025/jul/17/gillis-draws-boos-and-laughs-amid-jabs-at-caitlin-clark-and-donald-trump-at-espys-ceremony'
    article_1 = 'sport/2026/feb/07/one-battle-after-another-sam-darnolds-stubborn-route-to-the-super-bowl'
    article_2 = 'sport/2026/mar/15/kimi-antonelli-wins-chinese-gp-lewis-hamilton-takes-first-podium-for-ferrari'
    article_3 = 'sport/2026/mar/06/weekend-guide-cricket-six-nations-fa-cup-formula-one-follow-with-us'
    article_4 = 'sport/2026/mar/06/aston-martin-fear-may-not-be-able-to-compete-in-australian-gp-practice-f1'
    print(record_saved('94f86428-9081-70a5-44f1-7a030f617f5a', article_0))
    print(record_saved('94f86428-9081-70a5-44f1-7a030f617f5a', article_1))
    print(record_saved('94f86428-9081-70a5-44f1-7a030f617f5a', article_2))
    print(record_saved('94f86428-9081-70a5-44f1-7a030f617f5a', article_3))
    print(record_saved('94f86428-9081-70a5-44f1-7a030f617f5a', article_4))
    print(get_users_saved_articles('sughanrichardson'))

