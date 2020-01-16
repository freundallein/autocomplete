# -*- coding: utf-8 -*-
from typing import List, Dict
from dataclasses import dataclass

from service.service import Word

__all__ = (
    "Trie",
)


@dataclass
class Node(object):
    char: str
    is_word: bool
    frequency: int
    children: Dict[str, "Node"]


class Trie(object):
    def __init__(self):
        self.store = Node("#", False, 0, {})
        self.size = 0

    def add_word(self, item: Word) -> None:
        curr = self.store
        for index in range(len(item.word)):
            char = item.word[index]
            if curr.children.get(char) is None:
                curr.children[char] = Node(char, False, 0, {})
            curr = curr.children[char]
        if not curr.is_word:
            self.size += 1
        curr.is_word = True
        curr.frequency += item.frequency

    def get_words(self, prefix: str) -> List[Word]:
        curr = self.store
        for char in prefix:
            if curr is None:
                return []
            curr = curr.children.get(char)
        return [
            Word(prefix + postfix, frequency)
            for postfix, frequency in self._compose_words(curr)
        ]

    def _compose_words(self, node: Node) -> List[str]:
        result = []
        if node is None:
            return result
        if node.is_word:
            result.append(("", node.frequency))
        stack = [(child, "") for child in node.children.values()]
        while stack:
            item = stack.pop()
            node = item[0]
            path = item[1]
            postfix = path + node.char
            if node.is_word:
                result.append((postfix, node.frequency))
            for child in node.children.values():
                stack.append((child, postfix))
        return sorted(result, key=lambda pair: pair[1], reverse=True)
