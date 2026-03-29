from bson import ObjectId

from app.core.database import get_database


class NetworkRepository:
    @property
    def collection(self):
        return get_database()["network_nodes"]

    async def create(self, payload: dict) -> dict:
        result = await self.collection.insert_one(payload)
        document = await self.collection.find_one({"_id": result.inserted_id})
        return self._serialize(document)

    async def update_status(self, network_id: str, status: str) -> dict | None:
        if not ObjectId.is_valid(network_id):
            return None
        await self.collection.update_one({"_id": ObjectId(network_id)}, {"$set": {"status": status}})
        updated = await self.collection.find_one({"_id": ObjectId(network_id)})
        return self._serialize(updated) if updated else None

    @staticmethod
    def _serialize(document: dict) -> dict:
        document["id"] = str(document["_id"])
        del document["_id"]
        return document
