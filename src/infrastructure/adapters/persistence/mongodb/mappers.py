from typing import Optional, Dict, Any, List
from domain.entities.user_entity import User
from infrastructure.exceptions import MappingError

def map_user_mongo_to_user_entity(data: Optional[Dict[str, Any]]) -> Optional[User]:
    try:    
        if not data:
            return None
        data.pop("_id", None)
        return User(**data)
    except MappingError:
        raise
    except Exception as e:
        raise MappingError("Failed to map Mongo document to User entity", extra={"error": str(e)}) from e

def map_users_mongo_to_users_entity(cursor) -> List[User]:
    try:
        return [map_user_mongo_to_user_entity(doc) for doc in cursor]
    except MappingError:
        raise
    except Exception as e:
        raise MappingError("Failed to map list of Mongo documents to User entities", extra={"error": str(e)}) from e