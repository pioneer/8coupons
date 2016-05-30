"""
.. module:: db/async.py

Asynchronous MongoDB interface
"""
from motor.motor_asyncio import AsyncIOMotorClient
from eight_coupons import settings


db = AsyncIOMotorClient(settings.MONGO['host'],
                        settings.MONGO['port'])[settings.MONGO['db']]
