from bson import ObjectId

from app.core.database import get_database


class AssignmentRepository:
    @property
    def collection(self):
        return get_database()["assignments"]

    async def create(self, payload: dict) -> dict:
        result = await self.collection.insert_one(payload)
        document = await self.collection.find_one({"_id": result.inserted_id})
        return self._serialize(document)

    async def get_by_ticket_id(self, ticket_id: str) -> dict | None:
        if not ObjectId.is_valid(ticket_id):
            return None
        assignment = await self.collection.find_one({"ticket_id": ObjectId(ticket_id)})
        return self._serialize(assignment) if assignment else None

    async def list_by_engineer(self, engineer_id: str) -> list[dict]:
        if not ObjectId.is_valid(engineer_id):
            return []
        cursor = self.collection.find({"engineer_id": ObjectId(engineer_id)})
        return [self._serialize(doc) async for doc in cursor]

    async def update_status_by_ticket(self, ticket_id: str, status: str) -> dict | None:
        if not ObjectId.is_valid(ticket_id):
            return None
        await self.collection.update_one({"ticket_id": ObjectId(ticket_id)}, {"$set": {"status": status}})
        updated = await self.collection.find_one({"ticket_id": ObjectId(ticket_id)})
        return self._serialize(updated) if updated else None

    async def aggregate_resolution_avg_seconds(self) -> float:
        pipeline = [
            {
                "$lookup": {
                    "from": "tickets",
                    "localField": "ticket_id",
                    "foreignField": "_id",
                    "as": "ticket",
                }
            },
            {"$unwind": "$ticket"},
            {"$match": {"ticket.resolved_at": {"$ne": None}}},
            {
                "$project": {
                    "seconds": {
                        "$dateDiff": {
                            "startDate": "$ticket.created_at",
                            "endDate": "$ticket.resolved_at",
                            "unit": "second",
                        }
                    }
                }
            },
            {"$group": {"_id": None, "avg_seconds": {"$avg": "$seconds"}}},
        ]
        results = [doc async for doc in self.collection.aggregate(pipeline)]
        if not results:
            return 0.0
        return float(results[0].get("avg_seconds", 0.0))

    @staticmethod
    def _serialize(document: dict) -> dict:
        document["id"] = str(document["_id"])
        document["ticket_id"] = str(document["ticket_id"])
        document["engineer_id"] = str(document["engineer_id"])
        del document["_id"]
        return document
