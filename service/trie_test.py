# -*- coding: utf-8 -*-

from service import Word
from service.trie import Trie, Node


def test_trie_construction():
    observed = Trie()
    assert isinstance(observed.store, Node)
    assert observed.size == 0

def test_add_word():
    observed = Trie()
    expected_word = Word("abcd", 1)
    observed.add_word(expected_word)
    assert observed.size == 1
    observed_words = observed.get_words("a")
    assert len(observed_words) == 1
    observed_word = observed_words[0]
    assert observed_word.word == expected_word.word
    assert observed_word.frequency == expected_word.frequency

def test_add_word_twice():
    observed = Trie()
    expected_word = Word("abcd", 1)
    observed.add_word(expected_word)
    observed.add_word(expected_word)
    assert observed.size == 1
    observed_words = observed.get_words("a")
    assert len(observed_words) == 1
    observed_word = observed_words[0]
    assert observed_word.word == expected_word.word
    assert observed_word.frequency == 2

def test_get_words():
    observed = Trie()
    expected_word_one = Word("abcd", 1)
    expected_word_two = Word("abb", 3)
    observed.add_word(expected_word_one)
    observed.add_word(expected_word_two)
    assert observed.size == 2
    observed_words = observed.get_words("ab")
    assert observed_words == [expected_word_two, expected_word_one]

def test_get_words_empty():
    observed = Trie()
    observed_words = observed.get_words("a")
    assert observed_words == []
