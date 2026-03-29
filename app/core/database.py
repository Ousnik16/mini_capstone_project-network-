from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

client: AsyncIOMotorClient | None = None
database: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    global client, database
    client = AsyncIOMotorClient(settings.mongodb_uri)
    database = client[settings.mongodb_db_name]
    await database["users"].create_index("email", unique=True)
    await database["tickets"].create_index("user_id")
    await database["tickets"].create_index("status")
    await database["assignments"].create_index("ticket_id", unique=True)
    await database["assignments"].create_index("engineer_id")
    await database["network_nodes"].create_index("tower_id", unique=True)


async def close_mongo_connection() -> None:
    global client, database
    if client:
        client.close()
    client = None
    database = None


def get_database() -> AsyncIOMotorDatabase:
    if database is None:
        raise RuntimeError("Database is not initialized")
    return database
