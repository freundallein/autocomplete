# -*- coding: utf-8 -*-
import pytest


@pytest.mark.slow
async def test_get_words(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    resp = await client.get("/?prefix=perspective")
    assert resp.status == 200
    text = await resp.text()
    assert text == '{"words": [{"word": "perspective", "frequency": 555}, {"word": "perspectives", "frequency": 27}], "len": 2}'


@pytest.mark.slow
async def test_get_words_top(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    resp = await client.get("/?prefix=perspective&top=1")
    assert resp.status == 200
    text = await resp.text()
    assert text == '{"words": [{"word": "perspective", "frequency": 555}], "len": 1}'


@pytest.mark.slow
async def test_get_words_no_prefix(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    resp = await client.get("/")
    assert resp.status == 400
    text = await resp.text()
    assert text == '{"error": "no prefix provided"}'


@pytest.mark.slow
async def test_add_word(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    resp = await client.post("/", data='{"word":"testtesttest"}')
    assert resp.status == 200
    text = await resp.text()
    assert text == '{"error": null}'
    resp = await client.get("/?prefix=testtesttest")
    assert resp.status == 200
    text = await resp.text()
    assert text == '{"words": [{"word": "testtesttest", "frequency": 1}], "len": 1}'


@pytest.mark.slow
async def test_add_word_no_word(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    resp = await client.post("/", data='{"notword":"1"}')
    assert resp.status == 400
    text = await resp.text()
    assert text == """{"error": "body should contain 'word' key"}"""


@pytest.mark.slow
async def test_healthz(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    resp = await client.get("/healthz")
    assert resp.status == 200
    text = await resp.text()
    assert text == "READY"


@pytest.mark.slow
async def test_healthz_not_ready(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    configured_app["service"].ready = False
    resp = await client.get("/healthz")
    assert resp.status == 500
    text = await resp.text()
    assert text == "NOT READY"
