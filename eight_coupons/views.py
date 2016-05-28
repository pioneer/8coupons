import json
from aiohttp import web


class SiteHandler:

    def __init__(self, db):
        self.db = db

    async def games(self, request):
        search_params = {}
        search_str = request.GET.get('search')
        if search_str:
            search_params["name"] = search_str
        games = []
        async for game in self.db.games.find(search_params):
            game.pop("_id")
            games.append(game)
        return web.Response(text=json.dumps({'games': games}),
                            content_type="application/json")
