from pymongo import errors

USER_ROLES_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "email", "name", "created_at", "updated_at"
        ],
        "properties": {
            "email": {"bsonType": "string"},
            "name": {"bsonType": "string"},
            "role": {"bsonType": ["string", "null"], "enum": ["READER", "OPERATOR", "AUDITOR", "ADMINISTRATOR", None]},
            "created_at": {"bsonType": ["date", "null"]},
            "updated_at": {"bsonType": ["date", "null"]}
        }
    }
}

def ensure_user_roles_collection(db):
    try:
        if "user_roles" not in db.list_collection_names():
            db.create_collection("user_roles")
        col = db["user_roles"]
        col.create_index("email", unique=True)
        col.create_index("role")
    except errors.CollectionInvalid:
        pass  
    except Exception as e:
        raise RuntimeError(f"Error ensuring user_roles collection: {e}")