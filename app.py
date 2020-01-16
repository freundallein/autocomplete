# -*- coding: utf-8 -*-
import logging

from aiohttp import web

from utils import configure_app, setup_routes, setup_service


logging.basicConfig(
    format='%(asctime)s | [autocomplete] %(message)s', 
    datefmt="%d.%m.%Y %H:%M:%S", 
    level=logging.INFO
)


def main():
    app = web.Application()
    logging.info("[config] configuring app...")
    configure_app(app)
    setup_routes(app)
    setup_service(app)
    logging.info("[config] app configuration ready")
    web.run_app(
        app,
        host=app["config"]["host"],
        port=app["config"]["port"],
        access_log=None,
    )


if __name__ == '__main__':
    main()
