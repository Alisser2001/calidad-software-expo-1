import logging
from typing import Optional
from pymongo import MongoClient, errors
from domain.ports.infrastructure.persistence.mongo_repository import MongoDBRepository
from domain.exceptions import (
    DomainError,
    ValidationError
)
from .mongo_schema import ensure_user_roles_collection
from pymongo.collection import Collection
from domain.entities.user_entity import User
from typing import List, Dict, Any
from .mappers import (
    map_user_mongo_to_user_entity,
    map_users_mongo_to_users_entity
)
from domain.value_objects.role_permissions import RoleCode
from datetime import datetime, UTC
from infrastructure.exceptions import (
    DatabaseConnectionError,
    DatabaseOperationError,
    MappingError
)

logger = logging.getLogger("app.infrastructure.adapters.persistence.mongodb.mongo_db")

MONGO_MAPPING_ERROR = "Failed to map MongoDB response"

class MongoClientRepository(MongoDBRepository):
    def __init__(self, client: Optional[MongoClient] = None) -> None:
        self._database_url: Optional[str] = None
        self._client: Optional[MongoClient] = client
        self._db = None
        self._collection: Optional[Collection] = None

    def _classify_and_raise(self, err: Exception, context: str) -> None:
        if isinstance(err, errors.ServerSelectionTimeoutError):
            raise DatabaseConnectionError("MongoDB connection timed out", extra={"context": context}) from err
        if isinstance(err, errors.ConnectionFailure):
            raise DatabaseConnectionError("MongoDB connection failed", extra={"context": context}) from err
        if isinstance(err, errors.OperationFailure):
            raise DatabaseOperationError("MongoDB operation failed", extra={"context": context}) from err
        if isinstance(err, errors.PyMongoError):
            raise DatabaseOperationError("General MongoDB error", extra={"context": context}) from err
        raise DatabaseOperationError("Unexpected MongoDB exception", extra={"context": context}) from err

    def _ensure_client(self) -> MongoClient:
        if self._client is None:
            try:
                from config.settings import settings
                self._database_url = settings.mongodb_url
                db_name = settings.db_name
                self._client = MongoClient(self._database_url, serverSelectionTimeoutMS=5000)
                self._db = self._client[db_name]
                ensure_user_roles_collection(self._db)
                self._collection = self._db["user_roles"]
            except Exception as e:
                self._classify_and_raise(e, "initialize client")
        return self._client
    
    def _col(self) -> Collection:
        if self._collection is None:
            raise DatabaseConnectionError("MongoDB client not initialized")
        return self._collection
    
    def upsert_user(self, user: User) -> Optional[User]:
        self._ensure_client()
        try:
            self._col().update_one(
                {"email": user.email},
                {"$set": user.model_dump(exclude_none=True)},
                upsert=True
            )
            data = self._col().find_one({"email": user.email})
            return map_user_mongo_to_user_entity(data)
        except MappingError as e:
            raise ValidationError(MONGO_MAPPING_ERROR, extra={"cause": str(e)}) from e
        except DomainError:
            raise
        except Exception as e:
            self._classify_and_raise(e, "upsert_user")

    def get_user_by_email(self, email: str) -> Optional[User]:
        self._ensure_client()
        try:
            data = self._col().find_one({"email": email})
            return map_user_mongo_to_user_entity(data)
        except MappingError as e:
            raise ValidationError(MONGO_MAPPING_ERROR, extra={"cause": str(e)}) from e
        except DomainError:
            raise
        except Exception as e:
            self._classify_and_raise(e, "get_user_by_email")

    def list_users(self, role: Optional[str] = None) -> List[User]:
        self._ensure_client()
        try:
            query: Dict[str, Any] = {}
            if role:
                query["role"] = role
            cursor = self._col().find(query)
            return map_users_mongo_to_users_entity(cursor)
        except MappingError as e:
            raise ValidationError(MONGO_MAPPING_ERROR, extra={"cause": str(e)}) from e
        except DomainError:
            raise
        except Exception as e:
            self._classify_and_raise(e, "list_users")
        
    def assign_role(self, email: str, role: str) -> Optional[User]:
        self._ensure_client()
        if role not in [r.value for r in RoleCode]:
            raise MappingError(f"Invalid role '{role}' for user assignment")
        try:
            data = self._col().find_one_and_update(
                {"email": email},
                {
                    "$set": {
                        "role": role,
                        "updated_at": datetime.now(UTC),
                    }
                },
                return_document=True,
            )
            if not data:
                raise DatabaseOperationError(f"User with email '{email}' not found")
            return map_user_mongo_to_user_entity(data)
        except MappingError as e:
            raise ValidationError(MONGO_MAPPING_ERROR, extra={"cause": str(e)}) from e
        except DomainError:
            raise
        except Exception as e:
            self._classify_and_raise(e, "assign_role")
        
    def remove_role(self, email: str) -> Optional[User]:
        self._ensure_client()
        try:
            data = self._col().find_one_and_update(
                {"email": email},
                {
                    "$set": {
                        "role": None,
                        "updated_at": datetime.now(UTC),
                    }
                },
                return_document=True,
            )
            if not data:
                raise DatabaseOperationError(f"User with email '{email}' not found")
            return map_user_mongo_to_user_entity(data)
        except MappingError as e:
            raise ValidationError(MONGO_MAPPING_ERROR, extra={"cause": str(e)}) from e
        except DomainError:
            raise
        except Exception as e:
            self._classify_and_raise(e, "assign_role")

    def aclose(self) -> None:
        try:
            if self._client is not None:
                self._client.close()
                self._client = None
                self._db = None
        except Exception as e:
            raise DatabaseOperationError("Failed to close MongoDB client") from e