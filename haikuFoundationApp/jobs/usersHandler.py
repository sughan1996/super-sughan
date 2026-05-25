"""
PK = "USER_ID"
SK values allowed: ["TYPE#COGNITO_ID", "TYPE#EMAIL", "TYPE#PROFILE_NAME",
 "TYPE#DISPLAY_NAME", "TYPE#FIRST_NAME", "TYPE#LAST_NAME", "TYPE#PHONE_NUMBER"]
attributes = ["CREATED_AT", "UPDATED_AT", "VALUE"]
Do not change PK/SK or attribute names in items."
"""
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List

import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

# ---------------- Config ----------------
DYNAMODB_RESOURCE_ARN = "arn:aws:dynamodb:us-east-1:322828741334:table/haiku-foundation-users-table"
# Actual DynamoDB key attribute names in the table schema:
DDB_PK_ATTR = os.getenv("DDB_PK_ATTR", "userId")
DDB_SK_ATTR = os.getenv("DDB_SK_ATTR", "metaData")  # default to 'metaData' per table definition
ALLOWED_TYPES = {
    "TYPE#COGNITO_ID",
    "TYPE#EMAIL",
    "TYPE#PROFILE_NAME",
    "TYPE#DISPLAY_NAME",
    "TYPE#FIRST_NAME",
    "TYPE#LAST_NAME",
    "TYPE#PHONE_NUMBER",
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


# ---------------- Core builders ----------------

def _ensure_allowed(type_value: str) -> None:
    if type_value not in ALLOWED_TYPES:
        raise ValueError(f"type must be one of {sorted(ALLOWED_TYPES)}")


def _require_value(value: Any) -> None:
    if value is None:
        raise ValueError("value is required")
    if isinstance(value, str) and value.strip() == "":
        raise ValueError("value cannot be empty")


def _key_av(userId: str, type_value: str) -> Dict[str, Any]:
    return {
        DDB_PK_ATTR: _SERIALIZER.serialize(userId),
        DDB_SK_ATTR: _SERIALIZER.serialize(type_value),
    }


# ---------------- CRUD primitives ----------------

def insert_record(userId: str, type_value: str, value: Any) -> Dict[str, Any]:
    """Insert a new SK record with VALUE, CREATED_AT, UPDATED_AT. Idempotent on conflict."""
    _ensure_allowed(type_value)
    _require_value(value)

    item = {
        DDB_PK_ATTR: userId,
        DDB_SK_ATTR: type_value,
        "VALUE": value,
        "CREATED_AT": _now_iso(),
        "UPDATED_AT": _now_iso(),
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
        # Return existing as idempotent behavior
        existing = get_record(userId, type_value)
        if existing:
            return existing
        raise


def update_record(userId: str, type_value: str, value: Any) -> Dict[str, Any]:
    """Update VALUE and UPDATED_AT on an existing SK record. Fails if missing."""
    _ensure_allowed(type_value)
    _require_value(value)

    resp = _client().update_item(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        Key=_key_av(userId, type_value),
        UpdateExpression="SET #v = :val, #u = :upd",
        ExpressionAttributeNames={"#v": "VALUE", "#u": "UPDATED_AT", "#pk": DDB_PK_ATTR, "#sk": DDB_SK_ATTR},
        ExpressionAttributeValues={":val": _SERIALIZER.serialize(value), ":upd": _SERIALIZER.serialize(_now_iso())},
        ConditionExpression="attribute_exists(#pk) AND attribute_exists(#sk)",
        ReturnValues="ALL_NEW",
    )
    attrs = resp.get("Attributes")
    return _from_av_map(attrs) if attrs else {DDB_PK_ATTR: userId, DDB_SK_ATTR: type_value, "VALUE": value}


def upsert_record(userId: str, type_value: str, value: Any) -> Dict[str, Any]:
    """Update if exists; otherwise insert. Returns final record."""
    try:
        return update_record(userId, type_value, value)
    except _client().exceptions.ConditionalCheckFailedException:
        return insert_record(userId, type_value, value)


def get_record(userId: str, type_value: str) -> Optional[Dict[str, Any]]:
    _ensure_allowed(type_value)
    resp = _client().get_item(
        TableName=_table_name_from_arn(DYNAMODB_RESOURCE_ARN),
        Key=_key_av(userId, type_value),
        ConsistentRead=False,
    )
    av_item = resp.get("Item")
    return _from_av_map(av_item) if av_item else None


def get_user_id_values(userId: str) -> List[Dict[str, Any]]:
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

def create_user(
    userId: str,
    *,
    cognito_id: str,
    email: str,
    profile_name: str,
    display_name: str,
    first_name: str,
    last_name: str,
    phone_number: str,
) -> Dict[str, Any]:
    """Create all SK records for a user. All values are required and validated."""
    # Validate required values
    for name, v in {
        "cognito_id": cognito_id,
        "email": email,
        "profile_name": profile_name,
        "display_name": display_name,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
    }.items():
        _require_value(v)

    return {
        "TYPE#COGNITO_ID": insert_record(userId, "TYPE#COGNITO_ID", cognito_id),
        "TYPE#EMAIL": insert_record(userId, "TYPE#EMAIL", email),
        "TYPE#PROFILE_NAME": insert_record(userId, "TYPE#PROFILE_NAME", profile_name),
        "TYPE#DISPLAY_NAME": insert_record(userId, "TYPE#DISPLAY_NAME", display_name),
        "TYPE#FIRST_NAME": insert_record(userId, "TYPE#FIRST_NAME", first_name),
        "TYPE#LAST_NAME": insert_record(userId, "TYPE#LAST_NAME", last_name),
        "TYPE#PHONE_NUMBER": insert_record(userId, "TYPE#PHONE_NUMBER", phone_number),
    }


# Convenience setters (upsert semantics)

def set_cognito_id(userId: str, value: str) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#COGNITO_ID", value)


def set_email(userId: str, value: str) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#EMAIL", value)


def set_profile_name(userId: str, value: str) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#PROFILE_NAME", value)


def set_display_name(userId: str, value: str) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#DISPLAY_NAME", value)


def set_first_name(userId: str, value: str) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#FIRST_NAME", value)


def set_last_name(userId: str, value: str) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#LAST_NAME", value)


def set_phone_number(userId: str, value: str) -> Dict[str, Any]:
    return upsert_record(userId, "TYPE#PHONE_NUMBER", value)


# ---------------- CLI demo (optional) ----------------
if __name__ == "__main__":
    try:
        out = create_user(
            userId="samsonbabuji",
            cognito_id="84a864d8-20d1-7064-df14-2a3afec0f125",
            email="samsonbabuji.m@gmail.com",
            profile_name="Samson Babuji",
            display_name="samsonbabuji",
            first_name="Samson",
            last_name="Babuji",
            phone_number="+919382266099",
        )
        print(out)
        print(get_record("samsonbabuji", "TYPE#EMAIL"))
        print(get_record("samsonbabuji", "TYPE#FIRST_NAME"))
        print(get_user_id_values("samsonbabuji"))
    except Exception as e:
        raise e
