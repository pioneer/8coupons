import logging
import time
import re
import requests
import pymongo
import snowballstemmer
from bs4 import BeautifulSoup
from eight_coupons import settings


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

splitter = re.compile(r"[\s\.-]")


class GiantBombScraper:

    PLATFORM_IDS = []

    def __init__(self):
        if not self.PLATFORM_IDS:
            response = requests.get(settings.SCRAPER['platform_url_template'].\
                                        format(api_key=settings.SCRAPER['api_key']),
                                    headers={'User-Agent': settings.SCRAPER['user_agent']})
            self.PLATFORM_IDS = [x['id'] for x in response.json()['results']
                                 if x['abbreviation'] in settings.SCRAPER['platforms']]
            logging.debug("Fetched platform IDs %s for %s", self.PLATFORM_IDS, settings.SCRAPER['platforms'])
        self.db = pymongo.MongoClient(settings.MONGO['host'], settings.MONGO['port'])[settings.MONGO['db']]

    def data(self):
        offset = 0
        platforms = ",".join([str(platform_id)
                              for platform_id in self.PLATFORM_IDS])
        while True:
            url = settings.SCRAPER['url_template']\
                .format(api_key=settings.SCRAPER['api_key'],
                        limit=settings.SCRAPER['step'],
                        offset=offset,
                        platforms=platforms)
            response = requests.get(url,
                                    headers={'User-Agent': settings.SCRAPER['user_agent']})
            results = response.json()
            if len(results['results']) == 0:
                break
            yield results
            offset += settings.SCRAPER['step']

    def run(self):
        for data_page in self.data():
            results = data_page.pop('results')
            logging.info("Fetched %s", data_page)
            # TODO: bulk update
            for game in results:
                self.db.games.update({"id": game["id"]}, {"$set": game}, upsert=True)
                self.store_search_data(game)
        logging.info("Total games in database: %s", self.db.games.count())

    def store_stem(self, stem, id):
        self.db.search_index.update({"stem": stem},
                                   {"$addToSet": {"game_ids": id}},
                                   upsert=True)
        index_item = self.db.search_index.find_one({"stem": stem})
        index_item.pop("_id")
        logging.debug("Added stem '%s' to %s", stem, index_item)

    def store_search_data(self, game):
        stemmer = snowballstemmer.stemmer("english")
        for field in settings.SCRAPER['fields_to_index']:
            if not game[field]:
                continue
            # TODO: Check for incorrect HTML
            content = ''.join(BeautifulSoup(game[field]).findAll(text=True))
            for word in splitter.split(content):
                if not word:
                    continue
                word = word.lower()
                stem = stemmer.stemWord(word)
                logging.debug("Found word '%s' in field '%s' of game #%s", stem, field, game['id'])
                self.store_stem(stem, game['id'])

if __name__ == "__main__":
    scraper = GiantBombScraper()
    while True:
        scraper.run()
        logging.info("Sleeping for %s seconds", settings.SCRAPER['run_every'])
        time.sleep(settings.SCRAPER['run_every'])