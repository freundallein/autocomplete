# -*- coding: utf-8 -*-
import pytest

from aiohttp import web



# async def get_word(request):
#     # GET http://0.0.0.0:8000/?prefix=Example&top=100
#     prefix = request.rel_url.query.get("prefix")
#     if not prefix:
#         return json_response({"error": "no prefix provided"})
#     try:
#         top = int(request.rel_url.query.get("top", request.app["config"]["top"]))
#     except ValueError:
#         top = request.app["config"]["top"]
#     service = request.app["service"]
#     words = await service.get_words(prefix)
#     words = words[:top]
#     return json_response({"words": words, "len": len(words)}, dumps=dumps)


# async def add_word(request):
#     # curl -X POST -d '{"word":"Example"}' -H "Content-Type: application/json"  0.0.0.0:8000
#     body = await request.json()
#     new_word = body.get("word")
#     if not new_word:
#         return json_response({"error": "body should contain 'word' key"})
#     service = request.app["service"]
#     await service.add_word(new_word)
#     return json_response({"error": None})

# async def test_hello(aiohttp_client, loop):
#     app = web.Application()
#     app.router.add_get('/', hello)
#     client = await aiohttp_client(app)
#     resp = await client.get('/')
#     assert resp.status == 200
#     text = await resp.text()
#     assert 'Hello, world' in text
@pytest.mark.slow
async def test_healthz(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    resp = await client.get('/healthz')
    assert resp.status == 200
    text = await resp.text()
    assert text == "READY"

@pytest.mark.slow
async def test_healthz_not_ready(aiohttp_client, configured_app):
    client = await aiohttp_client(configured_app)
    configured_app["service"].ready = False
    resp = await client.get('/healthz')
    assert resp.status == 500
    text = await resp.text()
    assert text == "NOT READY"
