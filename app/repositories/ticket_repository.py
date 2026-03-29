from bson import ObjectId

from app.core.database import get_database


class TicketRepository:
    @property
    def collection(self):
        return get_database()["tickets"]

    async def create(self, payload: dict) -> dict:
        result = await self.collection.insert_one(payload)
        document = await self.collection.find_one({"_id": result.inserted_id})
        return self._serialize(document)

    async def list_by_user(self, user_id: str) -> list[dict]:
        if not ObjectId.is_valid(user_id):
            return []
        cursor = self.collection.find({"user_id": ObjectId(user_id)})
        return [self._serialize(doc) async for doc in cursor]

    async def list_all(self) -> list[dict]:
        cursor = self.collection.find({})
        return [self._serialize(doc) async for doc in cursor]

    async def get_by_id(self, ticket_id: str) -> dict | None:
        if not ObjectId.is_valid(ticket_id):
            return None
        ticket = await self.collection.find_one({"_id": ObjectId(ticket_id)})
        return self._serialize(ticket) if ticket else None

    async def update_status(self, ticket_id: str, status: str, resolved_at=None) -> dict | None:
        if not ObjectId.is_valid(ticket_id):
            return None
        payload = {"status": status}
        if resolved_at is not None:
            payload["resolved_at"] = resolved_at
        await self.collection.update_one({"_id": ObjectId(ticket_id)}, {"$set": payload})
        updated = await self.collection.find_one({"_id": ObjectId(ticket_id)})
        return self._serialize(updated) if updated else None

    @staticmethod
    def _serialize(document: dict) -> dict:
        document["id"] = str(document["_id"])
        document["user_id"] = str(document["user_id"])
        del document["_id"]
        return document
