"""
PK = "CONTENT_ID"
SK = [TYPE#TITLE", "TYPE#TAGS", "TYPE#STATUS", "TYPE#BODY", "TYPE#AUTHOR", "TYPE#STATUS"]
attributes = ["CREATED_AT", "UPDATED_AT", "VALUE", "USER_ID"]
Do not change PK/SK or attribute names in items.
"""

import os

# ---------------- Config ----------------
DYNAMODB_RESOURCE_ARN = "arn:aws:dynamodb:us-east-1:322828741334:table/haiku-foundation-stories-table"
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

