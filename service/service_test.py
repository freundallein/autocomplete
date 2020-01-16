# -*- coding: utf-8 -*-
from unittest.mock import patch, mock_open
from pytest import raises, mark

from .trie import Trie
from .service import Service, Word


def test_service_construction():
    srv = Service(Trie)
    assert isinstance(srv.datastore, Trie)
    assert srv.persistent_storage is None
    assert not srv.ready


def test_service_init_assertion():
    with raises(AssertionError):
        Service("DUMMY")


def test_service_init_with_persistenet_storage():
    class DummyStorage:
        async def add_word(self):
            pass
        async def get_words(self):
            pass
        async def fill(self):
            pass
    srv = Service(Trie, DummyStorage())
    assert isinstance(srv.persistent_storage, DummyStorage)


def test_service_init_with_persistenet_storage_assertion():
    class DummyStorage:
        pass
    with raises(AssertionError):
        Service(Trie, DummyStorage())


def test_fill_datastore():
    srv = Service(Trie)
    expected = [("a", 1), ("b", 2)]
    srv.fill_datastore(expected)
    assert srv.datastore.size == 2


def test_fill_datastore_with_nothing():
    srv = Service(Trie)
    expected = []
    srv.fill_datastore(expected)
    assert srv.datastore.size == 0

def test_load_corpus():
    srv = Service(Trie)
    with patch("builtins.open", mock_open(read_data="a:1\nb:2\n")):
        observed = srv.load_corpus()
        assert observed == [("a", 1), ("b", 2)]

@mark.asyncio
async def test_add_word(event_loop):
    srv = Service(Trie)
    assert srv.datastore.size == 0
    await srv.add_word("a", 1)
    assert srv.datastore.size == 1
    await srv.add_word("b", 1)
    await srv.add_word("b", 1)
    assert srv.datastore.size == 2

@mark.asyncio
async def test_add_word_with_storage(event_loop, fake_storage):
    srv = Service(Trie, fake_storage)
    assert srv.persistent_storage.store == []
    await srv.add_word("a", 1)
    await srv.add_word("b", 2)
    assert srv.persistent_storage.store == [("a", 1), ("b", 2)]

@mark.asyncio
async def test_get_words(event_loop):
    srv = Service(Trie)
    await srv.add_word("a", 1)
    await srv.add_word("ab", 1)
    await srv.add_word("ab", 1)
    observed = await srv.get_words("a")
    assert observed == [Word(word="ab", frequency=2), Word(word="a", frequency=1)]

@mark.asyncio
async def test_get_words_empty(event_loop):
    srv = Service(Trie)
    observed = await srv.get_words("a")
    assert observed == []

@mark.asyncio
async def test_restore(event_loop):
    srv = Service(Trie)
    with patch("builtins.open", mock_open(read_data="a:1\nb:2\n")):
        await srv.restore()
    assert srv.ready
    assert srv.datastore.size == 2

@mark.asyncio
async def test_restore_with_storage_empty(event_loop, fake_storage):
    srv = Service(Trie, fake_storage)
    with patch("builtins.open", mock_open(read_data="a:1\nb:2\n")):
        await srv.restore()
    assert srv.ready
    observed = await srv.persistent_storage.get_words()
    assert observed == [("a", 1), ("b", 2)]

@mark.asyncio
async def test_restore_with_storage_filled(event_loop, fake_storage):
    srv = Service(Trie, fake_storage)
    fake_storage.store = [("a", 1), ("b", 2), ("c", 2)]
    await srv.restore()
    assert srv.ready
    observed = await srv.get_words("")
    assert observed == [Word("c", 2), Word("b", 2), Word("a", 1)]
