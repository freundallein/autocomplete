# -*- coding: utf-8 -*-
import pytest

from aiohttp import web

from utils import configure_app, setup_routes, setup_service


@pytest.fixture
def empty_app():
    app = web.Application()
    return app


@pytest.fixture
def configured_app():
    app = web.Application()
    configure_app(app)
    setup_routes(app)
    setup_service(app)
    return app


@pytest.fixture
def fake_storage():
    class DummyStorage:
        def __init__(self):
            self.store = []
        async def add_word(self, pair):
            self.store.append(pair)

        async def get_words(self):
            return self.store

        async def fill(self, pairs):
            self.store = pairs

    return DummyStorage()
