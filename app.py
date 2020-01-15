# -*- coding: utf-8 -*-
import asyncio

from aiohttp import web

from utils import configure_app, setup_routes, setup_service


def main():
    app = web.Application()
    configure_app(app)
    setup_routes(app)
    setup_service(app)
    web.run_app(
        app, 
        host=app["config"]["host"],
        port=app["config"]["port"],
    )

if __name__ == '__main__':
    main()
