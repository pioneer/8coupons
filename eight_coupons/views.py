import json
from aiohttp import web


class SiteHandler:

    def __init__(self, db):
        self.db = db

    async def games(self, request):
        games = []
        async for game in self.db.games.find():
            game.pop("_id")
            games.append(game)
        return web.Response(text=json.dumps({'games': games}),
                            content_type="application/json")
