import json
import logging
from aiohttp import web
from eight_coupons.utils import split_stems
from eight_coupons.db.async import db


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class SiteHandler:

    async def games(self, request):
        search_params = {}
        search_str = request.GET.get('search')
        if search_str:
            game_ids = set()
            for stem in split_stems(search_str):
                index_item = await db.search_index.find_one({"stem": stem})
                if index_item:
                    game_ids = game_ids.union(index_item["game_ids"])
            if game_ids:
                search_params = {"id": {"$in": list(game_ids)}}
        games = []
        async for game in db.games.find(search_params):
            game.pop("_id")
            games.append(game)
        return web.Response(text=json.dumps({'games': games}),
                            content_type="application/json")
