import requests
import aiohttp

from eight_coupons.scrapers.base import Scraper
from eight_coupons import settings


class GiantBombScraper(Scraper):
    __STEP = 20
    __PLATFORMS_URL = 'http://www.giantbomb.com/api/platforms/?limit=100&offset=0&api_key=' + \
                      settings.GIANT_BOMB_API + '&format=json'
    __PLATFORMS = ('NES',
                   'SNES',
                   'N64')

    def __init__(self):
        self.platform_ids = []

    def get_additional_data(self):
        req = requests.get(self.__PLATFORMS_URL, headers={
            'User-Agent': settings.USER_AGENT
        })
        self.platform_ids = [x['id'] for x in req.json()['results'] if x['abbreviation'] in self.__PLATFORMS]

    async def fetch_data(self, offset):
        while True:
            url = 'http://www.giantbomb.com/api/games/?limit=' + str(self.__STEP) + \
                  '&offset=' + str(offset * self.__STEP) + '&api_key=' + settings.GIANT_BOMB_API + \
                  '&format=json&platforms=' + ',' . join(map(lambda x: str(x), self.platform_ids))

            req = await aiohttp.get(url, headers={
                'User-Agent': settings.USER_AGENT
            })
            results = await req.json()
            await req.release()

            print(len(results['results']))

            if len(results['results']) == 0:
                break

            # put data into mongo

            offset += settings.CONCURRENT
