"""
.. module:: main.py

Initialization for HTTP API server
"""
import asyncio
import logging
import pathlib

from aiohttp import web
from eight_coupons.routes import setup_routes
from eight_coupons import settings
from eight_coupons.views import EightCouponsHandler


PROJ_ROOT = pathlib.Path(__file__).parent.parent


async def init(loop):
    """
    Sets up aiohttp-based web application, views and routes

    :param: loop
      Asyncio's event loop to pass into aiohttp web application
    """
    # Setup application and extensions
    app = web.Application(loop=loop)

    # Setup views and routes
    setup_routes(app, EightCouponsHandler(), PROJ_ROOT)

    return app, settings.HOST, settings.PORT


def main():
    """
    Main HTTP API runner
    """
    # Init logging
    logging.basicConfig(level=logging.DEBUG,
                        format=settings.LOGGING_FORMAT)

    # Start event loop and web server
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
