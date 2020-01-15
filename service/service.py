# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple
from dataclasses import dataclass

__all__ = (
    "Word",
    "Service",
)


@dataclass
class Word:
    word: str
    frequency: int


class Service(object):
    def __init__(self, strategy_class, persistent_storage=None):
        strategy_methods = dir(strategy_class)
        assert "add_word" in strategy_methods, "Expected add_word method in strategy_class"
        assert "get_words" in strategy_methods, "Expected get_words method in strategy_class"
        if persistent_storage is not None:
            persistent_storage_methods = dir(persistent_storage)
            assert "add_word" in persistent_storage_methods, "Expected add_word method in persistent_storage"
            assert "get_words" in persistent_storage_methods, "Expected get_words method in persistent_storage"
            assert "fill" in persistent_storage_methods, "Expected fill method in persistent_storage"
        self.datastore = strategy_class()
        self.persistent_storage = persistent_storage
        self.ready = False

    async def add_word(self, word: str, frequency: int = 1) -> None:
        if word == "abb":
            print(word, frequency)
        self.datastore.add_word(Word(word, frequency))
        if self.persistent_storage:
            await self.persistent_storage.add_word((word, frequency))

    async def get_words(self, prefix: str) -> List[Word]:
        return self.datastore.get_words(prefix)

    def fill_datastore(self, words: List[Tuple[str, int]]) -> None:
        if not words:
            return
        for pair in words:
            self.datastore.add_word(Word(pair[0], pair[1]))

    async def restore(self) -> None:
        pairs = []
        if self.persistent_storage:
            pairs = await self.persistent_storage.get_words()
        if not pairs:
            pairs = self.load_corpus()
            await self.persistent_storage.fill(pairs)
        self.fill_datastore(pairs)
        self.ready = True

    def load_corpus(self) -> List[Tuple[str, int]]:
        pairs = []
        with open("data/corpus.txt", "r") as f:
            line = f.readline()
            while line:
                line = line.strip("\n").split(":")
                pairs.append((line[0], int(line[1])))
                line = f.readline()
        return pairs
        