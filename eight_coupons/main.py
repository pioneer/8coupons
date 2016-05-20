import asyncio
import logging
import pathlib

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
from eight_coupons.routes import setup_routes
from eight_coupons.utils import load_config
from eight_coupons.views import SiteHandler


PROJ_ROOT = pathlib.Path(__file__).parent.parent


async def init(loop):
    # setup application and extensions
    app = web.Application(loop=loop)

    # load config from yaml file
    conf = load_config(str(PROJ_ROOT / 'config' / 'config.yaml'))

    # create connection to the database\\
    db = AsyncIOMotorClient()[conf['mongo']['db']]

    # setup views and routes
    handler = SiteHandler(db)
    setup_routes(app, handler, PROJ_ROOT)

    host, port = conf['host'], conf['port']
    return app, host, port


def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
