# -*- coding: utf-8 -*-
from aiohttp.web import json_response, Response

from utils.serialization import dumps


__all__ = (
    "get_words",
    "add_word",
    "healthz",
)


async def get_words(request):
    # GET http://0.0.0.0:8000/?prefix=Example&top=100
    prefix = request.rel_url.query.get("prefix")
    if not prefix:
        return json_response({"error": "no prefix provided"}, status=400)
    try:
        top = int(request.rel_url.query.get("top", request.app["config"]["top"]))
    except ValueError:
        top = request.app["config"]["top"]
    service = request.app["service"]
    words = await service.get_words(prefix)
    words = words[:top]
    return json_response({"words": words, "len": len(words)}, dumps=dumps)


async def add_word(request):
    # curl -X POST -d '{"word":"Example"}' -H "Content-Type: application/json"  0.0.0.0:8000
    body = await request.json()
    new_word = body.get("word")
    if not new_word:
        return json_response({"error": "body should contain 'word' key"}, status=400)
    service = request.app["service"]
    await service.add_word(new_word)
    return json_response({"error": None})


async def healthz(request):
    service = request.app["service"]
    response = {
        True: ("READY", 200),
        False: ("NOT READY", 500),
    }[service.ready]
    return Response(text=response[0], status=response[1])
