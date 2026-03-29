from bson import ObjectId

from app.core.database import get_database


class UserRepository:
    @property
    def collection(self):
        return get_database()["users"]

    async def create(self, user: dict) -> dict:
        result = await self.collection.insert_one(user)
        created = await self.collection.find_one({"_id": result.inserted_id})
        return self._serialize(created)

    async def get_by_email(self, email: str) -> dict | None:
        user = await self.collection.find_one({"email": email})
        return self._serialize(user) if user else None

    async def get_by_id(self, user_id: str) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return self._serialize(user) if user else None

    async def exists_engineer(self, engineer_id: str) -> bool:
        if not ObjectId.is_valid(engineer_id):
            return False
        engineer = await self.collection.find_one({"_id": ObjectId(engineer_id), "role": "engineer", "is_active": True})
        return engineer is not None

    @staticmethod
    def _serialize(document: dict) -> dict:
        document["id"] = str(document["_id"])
        del document["_id"]
        return document
