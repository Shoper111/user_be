import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from user_be.conf import Settings
from user_be.schemas import beanie_models

logger = logging.getLogger(__name__)


async def init_mongodb(settings: Settings):
    logger.info({'message': f'AWS MONGO client has been configured.'})
    client = AsyncIOMotorClient(settings.mongodb_database_uri)
    await init_beanie(
        database=client.db_name,
        document_models=beanie_models,
    )
