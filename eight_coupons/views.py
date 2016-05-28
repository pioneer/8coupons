import json
from aiohttp import web
import snowballstemmer


class SiteHandler:

    def __init__(self, db):
        self.db = db

    async def games(self, request):
        search_params = {}
        search_str = request.GET.get('search')
        if search_str:
            stemmer = snowballstemmer.stemmer("english")
            # TODO: Add the same regex splitting and possibly HTML stripping
            words = search_str.split()
            game_ids = set()
            for word in words:
                word = word.lower()
                stem = stemmer.stemWord(word)
                index_item = await self.db.search_index.find_one({"stem": stem})
                if index_item:
                    game_ids = game_ids.union(index_item["game_ids"])
            if game_ids:
                search_params = {"id": {"$in": list(game_ids)}}
        games = []
        async for game in self.db.games.find(search_params):
            game.pop("_id")
            games.append(game)
        return web.Response(text=json.dumps({'games': games}),
                            content_type="application/json")
