import sys
import inspect
import asyncio

from eight_coupons.scrapers import *
from eight_coupons.scrapers.base import Scraper
from eight_coupons import settings
from eight_coupons.celery import app


def get_scrapers():
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and obj != Scraper:
            yield obj


@app.task
def download():
    loop = asyncio.get_event_loop()

    for scraper in get_scrapers():
        worker = scraper()
        worker.get_additional_data()
        loop.run_until_complete(asyncio.wait([worker.fetch_data(x) for x in range(settings.CONCURRENT)]))

    loop.close()
