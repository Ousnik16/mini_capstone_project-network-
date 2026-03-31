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

    async def update(self, network_id: str, update_data: dict) -> dict | None:
        """Update network node with multiple fields"""
        if not ObjectId.is_valid(network_id):
            return None
        filtered_data = {k: v for k, v in update_data.items() if v is not None}
        if not filtered_data:
            return await self.collection.find_one({"_id": ObjectId(network_id)})
        await self.collection.update_one({"_id": ObjectId(network_id)}, {"$set": filtered_data})
        updated = await self.collection.find_one({"_id": ObjectId(network_id)})
        return self._serialize(updated) if updated else None

    async def get_all(self) -> list:
        """Get all network nodes"""
        documents = await self.collection.find().to_list(None)
        return [self._serialize(doc) for doc in documents]

    async def get_by_id(self, network_id: str) -> dict | None:
        """Get network node by ID"""
        if not ObjectId.is_valid(network_id):
            return None
        document = await self.collection.find_one({"_id": ObjectId(network_id)})
        return self._serialize(document) if document else None

    @staticmethod
    def _serialize(document: dict) -> dict:
        document["id"] = str(document["_id"])
        del document["_id"]
        return document
