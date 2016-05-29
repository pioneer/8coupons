import asyncio
import logging
import pathlib

from aiohttp import web
from eight_coupons.routes import setup_routes
from eight_coupons import settings
from eight_coupons.views import SiteHandler


PROJ_ROOT = pathlib.Path(__file__).parent.parent


async def init(loop):
    # setup application and extensions
    app = web.Application(loop=loop)

    # setup views and routes
    setup_routes(app, SiteHandler(), PROJ_ROOT)

    host, port = settings.HOST, settings.PORT
    return app, host, port


def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
