from abc import ABCMeta, abstractmethod


class Scraper(object):
    """
    This is base class for scraping data
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_additional_data(self):
        pass

    @abstractmethod
    async def fetch_data(self):
        pass
