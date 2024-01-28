import jinja2
from aiohttp_jinja2 import setup as jinja_setup
from aiohttp import web
import logging


from src.log import initial_logging
from src.arest.conf import settings
from src.arest.web.home.views import *
from aiohttp_controller.controller.__init__ import controller_setup
from tortoise.contrib.aiohttp import register_tortoise


def create_app():
    initial_logging()
    logger = logging.getLogger(settings.LOGGER)
    app = web.Application(logger=logger)
    controller_setup(app, "src.arest.web.urls", True)
    jinja_setup(
        app,
        loader=jinja2.FileSystemLoader(
            list(settings.BASE_DIR.glob("web/**/templates"))
        ),
    )

    register_tortoise(app, config=settings.DATABASE, generate_schemas=True)
    return app
