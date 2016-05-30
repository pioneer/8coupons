"""
.. module:: scraper.py

Scraping and indexing GiantBomb data
"""
import logging
import time
import requests
from eight_coupons import settings
from eight_coupons.utils import split_stems
from eight_coupons.db.sync import db


logging.basicConfig(level=logging.DEBUG,
                    format=settings.LOGGING_FORMAT)


class GiantBombScraper:

    PLATFORM_IDS = []

    def __init__(self):
        # Get platform ids for given platform names taken from the config
        if not self.PLATFORM_IDS:
            response = requests.\
                get(settings.SCRAPER['platform_url_template'].
                    format(api_key=settings.SCRAPER['api_key']),
                    headers={'User-Agent': settings.SCRAPER['user_agent']})
            self.PLATFORM_IDS = [x['id'] for x in response.json()['results']
                                 if x['abbreviation']
                                 in settings.SCRAPER['platforms']]
            logging.debug("Fetched platform IDs %s for %s",
                          self.PLATFORM_IDS, settings.SCRAPER['platforms'])

    def data(self):
        """
        An iterator which fetches games from GiantBomb API, page by page,
        using an offset value from settings, and yields those pages as
        a sequence.

        TODO: Parallel fetching
        """
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
                                    headers={'User-Agent':
                                             settings.SCRAPER['user_agent']})
            results = response.json()
            if len(results['results']) == 0:
                break
            yield results
            offset += settings.SCRAPER['step']

    def run(self):
        """
        Main process: fetch data, insert/update the database, add search index
        against fetched data.
        """
        for data_page in self.data():
            results = data_page.pop('results')
            logging.info("Fetched %s", data_page)
            # TODO: bulk update
            for game in results:
                db.games.update({"id": game["id"]},
                                {"$set": game}, upsert=True)
                self.store_search_data(game)
        logging.info("Total games in database: %s", db.games.count())

    def store_stem(self, stem, ids):
        """
        Updates or inserts the part of index related to the given stem.

        :param: stem
          A stem (normalized word form) to update the data for.

        :param: ids
          Ids of games which are known to contain the given stem.
        """
        # Update the list of game ids related to given stem with given ids
        db.search_index.update({"stem": stem},
                               {"$addToSet": {"game_ids": ids}},
                               upsert=True)
        # Fetch updated search index item to show in logging
        index_item = db.search_index.find_one({"stem": stem})
        index_item.pop("_id")  # Remove _id for better displaying in log
        logging.debug("Added stem '%s' to %s", stem, index_item)

    def store_search_data(self, game):
        """
        Get stems from each configured field of given game and store
        the index for each stem.

        :param: game
          Game JSON object fetched from API.
        """
        for field in settings.SCRAPER['fields_to_index']:
            if not game[field]:
                continue
            for stem in split_stems(game[field]):
                logging.debug("Found word '%s' in field '%s' of game #%s",
                              stem,
                              field, game['id'])
                self.store_stem(stem, game['id'])

if __name__ == "__main__":
    scraper = GiantBombScraper()
    # Run scraping forever periodically, using a delay from settings
    while True:
        scraper.run()
        logging.info("Sleeping for %s seconds", settings.SCRAPER['run_every'])
        time.sleep(settings.SCRAPER['run_every'])
