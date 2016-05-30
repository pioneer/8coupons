"""
.. module:: db/sync.py

Synchronous MongoDB interface
"""
import pymongo
from eight_coupons import settings


db = pymongo.MongoClient(settings.MONGO['host'],
                         settings.MONGO['port'])[settings.MONGO['db']]
