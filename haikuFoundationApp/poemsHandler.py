"""
PK = "CONTENT_ID"
SK = [TYPE#TITLE", "TYPE#TAGS", "TYPE#BODY", "TYPE#AUTHOR", "TYPE#STATUS"]
attributes = ["CREATED_AT", "UPDATED_AT", "VALUE", "USER_ID"]
Do not change PK/SK or attribute names in items.
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List

import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

# ---------------- Config ----------------
DYNAMODB_RESOURCE_ARN = "arn:aws:dynamodb:us-east-1:322828741334:table/haiku-foundation-poems-table"
# Actual DynamoDB key attribute names in the table schema:
DDB_PK_ATTR = os.getenv("DDB_PK_ATTR", "userId")
DDB_SK_ATTR = os.getenv("DDB_SK_ATTR", "metaData")  # default to 'metaData' per table definition
ALLOWED_TYPES = {
    "TYPE#CONTENT",
    "TYPE#TITLE",
    "TYPE#BODY",
    "TYPE#AUTHOR",
    "TYPE#TAGS",
    "TYPE#STATUS"
}


# ---------------- AWS Helpers ----------------

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


# ---------------- (De)Serializers ----------------
_SERIALIZER = TypeSerializer()
_DESERIALIZER = TypeDeserializer()


def _to_av_map(item: Dict[str, Any]) -> Dict[str, Any]:
    return {k: _SERIALIZER.serialize(v) for k, v in item.items()}


def _from_av_map(av_item: Dict[str, Any]) -> Dict[str, Any]:
    return {k: _DESERIALIZER.deserialize(v) for k, v in av_item.items()}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


# ---------------- Builders ----------------

def _build_item(content_id: str, sk_type: str, value: Any, user_id: str) -> Dict[str, Any]:
    if not sk_type or not isinstance(sk_type, str):
        raise ValueError("type must be a non-empty string")
    if sk_type not in ALLOWED_TYPES:
        raise ValueError(f"type must be one of {sorted(ALLOWED_TYPES)}")
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValueError("value is required and cannot be empty")
    if not user_id:
        raise ValueError("USER_ID is required")

    return {
        DDB_PK_ATTR: content_id,
        DDB_SK_ATTR: sk_type,
        "VALUE": value,
        "USER_ID": user_id,
    }


# ---------------- Writes ----------------

def insert_record(content_id: str, sk_type: str, value: Any, user_id: str) -> Dict[str, Any]:
    """Create a new poem attribute record. Fails if PK/SK already exists."""
    item = _build_item(content_id, sk_type, value, user_id)
    now = _now_iso()
    item["CREATED_AT"] = now
    item["UPDATED_AT"] = now
    _client().put_item(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        Item=_to_av_map(item),
        ConditionExpression="attribute_not_exists(#pk) AND attribute_not_exists(#sk)",
        ExpressionAttributeNames={"#pk": DDB_PK_ATTR, "#sk": DDB_SK_ATTR},
    )
    return item


def update_record(content_id: str, sk_type: str, value: Any, user_id: Optional[str] = None) -> Dict[str, Any]:
    """Update VALUE and UPDATED_AT. Requires the record to exist."""
    if sk_type not in ALLOWED_TYPES:
        raise ValueError(f"type must be one of {sorted(ALLOWED_TYPES)}")
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValueError("value is required and cannot be empty")

    key = {
        DDB_PK_ATTR: _SERIALIZER.serialize(content_id),
        DDB_SK_ATTR: _SERIALIZER.serialize(sk_type),
    }
    expr_names = {"#v": "VALUE", "#u": "UPDATED_AT"}
    expr_vals = {":v": _SERIALIZER.serialize(value), ":u": _SERIALIZER.serialize(_now_iso())}

    # Optionally update USER_ID too if provided
    update_expr = "SET #v = :v, #u = :u"
    if user_id is not None:
        expr_names["#uid"] = "USER_ID"
        expr_vals[":uid"] = _SERIALIZER.serialize(user_id)
        update_expr += ", #uid = :uid"

    resp = _client().update_item(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        Key=key,
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_vals,
        ConditionExpression="attribute_exists(#pk) AND attribute_exists(#sk)",
        ExpressionAttributeNamesAdditional={"#pk": DDB_PK_ATTR, "#sk": DDB_SK_ATTR} if False else None,
        ReturnValues="ALL_NEW",
    )
    # NOTE: botocore doesn't accept ExpressionAttributeNamesAdditional; we used standard names above.
    return _from_av_map(resp.get("Attributes", {}))


def upsert_record(content_id: str, sk_type: str, value: Any, user_id: str) -> Dict[str, Any]:
    """Update if exists else insert."""
    existing = get_record(content_id, sk_type)
    if existing:
        return update_record(content_id, sk_type, value, user_id)
    return insert_record(content_id, sk_type, value, user_id)


# ---------------- Reads ----------------

def get_record(content_id: str, sk_type: str) -> Optional[Dict[str, Any]]:
    key = {
        DDB_PK_ATTR: _SERIALIZER.serialize(content_id),
        DDB_SK_ATTR: _SERIALIZER.serialize(sk_type),
    }
    resp = _client().get_item(TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN), Key=key, ConsistentRead=False)
    av_item = resp.get("Item")
    return _from_av_map(av_item) if av_item else None


def list_content_items(content_id: str) -> List[Dict[str, Any]]:
    resp = _client().query(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        KeyConditionExpression="#pk = :pk",
        ExpressionAttributeNames={"#pk": DDB_PK_ATTR},
        ExpressionAttributeValues={":pk": _SERIALIZER.serialize(content_id)},
        ConsistentRead=False,
    )
    return [_from_av_map(av) for av in resp.get("Items", [])]


# ---------------- Convenience helpers ----------------

def create_poem(*, content_id: str, user_id: str, title: str, body: str, author: str, tags: Any, status: str) -> Dict[str, Any]:
    """Create the standard set of items for a poem (TITLE, BODY, AUTHOR, TAGS, STATUS)."""
    return {
        "TITLE": insert_record(content_id, "TYPE#TITLE", title, user_id),
        "BODY": insert_record(content_id, "TYPE#BODY", body, user_id),
        "AUTHOR": insert_record(content_id, "TYPE#AUTHOR", author, user_id),
        "TAGS": insert_record(content_id, "TYPE#TAGS", tags, user_id),
        "STATUS": insert_record(content_id, "TYPE#STATUS", status, user_id),
    }


def set_title(content_id: str, value: str, user_id: str) -> Dict[str, Any]:
    return upsert_record(content_id, "TYPE#TITLE", value, user_id)


def set_body(content_id: str, value: str, user_id: str) -> Dict[str, Any]:
    return upsert_record(content_id, "TYPE#BODY", value, user_id)


def set_author(content_id: str, value: str, user_id: str) -> Dict[str, Any]:
    return upsert_record(content_id, "TYPE#AUTHOR", value, user_id)


def set_tags(content_id: str, value: Any, user_id: str) -> Dict[str, Any]:
    return upsert_record(content_id, "TYPE#TAGS", value, user_id)


def set_status(content_id: str, value: str, user_id: str) -> Dict[str, Any]:
    return upsert_record(content_id, "TYPE#STATUS", value, user_id)


# ---------------- CLI demo ----------------
if __name__ == "__main__":
    try:
        out = create_poem(
            content_id="test_poem",
            user_id="sughanrichardson",
            title="A quiet pond",
            body="ripples fade into dusk",
            author="",
            tags=["haiku", "nature"],
            status="DRAFT",
        )
        print("Created:", out.keys())
    except Exception as error:
        raise error
