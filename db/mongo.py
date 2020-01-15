# -*- coding: utf-8 -*-
from typing import List, Tuple

from motor.motor_asyncio import AsyncIOMotorClient


class PersistentStorage(object):
    DB_NAME = "autocomplete"
    DB_COLLECTION = "en_corpus"

    def __init__(self, dsn):
        # docker run -it --rm --name mongodb -p 27017:27017 mongo
        client = AsyncIOMotorClient(dsn)
        db = client[self.DB_NAME]
        self.collection = db[self.DB_COLLECTION]

    async def get_words(self) -> List[Tuple[str, int]]:
        cursor = self.collection.find()
        return [(item["word"], item["frequency"]) async for item in cursor]

    async def add_word(self, item: Tuple[str, int]) -> None:
        word = item[0]
        frequency = item[1]
        await self.collection.find_one_and_update(
            {"word": word},
            {"$inc": {"frequency": frequency}},
            projection={"frequency": True, "_id": False},
            upsert=True,)

    async def fill(self, words: List[Tuple[str, int]]) -> None:
        if not words:
            return
        await self.collection.insert_many(
            [{"word": pair[0], "frequency": pair[1]} for pair in words]
        )