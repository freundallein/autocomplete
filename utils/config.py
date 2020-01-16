# -*- coding: utf-8 -*-
import os
import asyncio

from handlers import add_word, get_word, healthz
from db.mongo import PersistentStorage
from service import Service, Trie

__all__ = (
    "configure_app",
    "setup_routes",
    "setup_service",
)


def configure_app(app) -> None:
    app["config"] = {}
    app["config"]["host"] = get_config_value("HOST", "0.0.0.0")
    app["config"]["port"] = get_config_value("PORT", "8000")
    app["config"]["top"] = get_config_value("TOP", 5)
    app["config"]["use_persistence"] = get_config_value("USE_PERSISTENCE", False)
    app["config"]["db_host"] = get_config_value("DB_HOST", "0.0.0.0")
    app["config"]["db_port"] = get_config_value("DB_PORT", "27017")
    app["config"]["db_user"] = get_config_value("DB_USER", "autocomplete")
    app["config"]["db_password"] = get_config_value("DB_PASSWORD", "autocomplete")


def get_config_value(key, fallback: str) -> str:
    return os.getenv(key, fallback)


def setup_routes(app) -> None:
    app.router.add_get('/healthz', healthz)
    app.router.add_get('/', get_word)
    app.router.add_post('/', add_word)


def setup_service(app) -> None:
    storage = None
    if app["config"]["use_persistence"]:
        host = app["config"]["db_host"]
        port = app["config"]["db_port"]
        username = app["config"]["db_user"]
        password = app["config"]["db_password"]
        dsn = f"mongodb://{username}:{password}@{host}:{port}"
        storage = PersistentStorage(dsn)
    serv = Service(Trie, storage)
    app["service"] = serv
    app.on_startup.append(start_background_tasks)


async def restore_service(app) -> None:
    await app["service"].restore()


async def start_background_tasks(app) -> None:
    asyncio.create_task(restore_service(app))
