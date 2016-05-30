"""
.. module:: views.py

HTTP API server views
"""
import json
from aiohttp import web
from eight_coupons.utils import split_stems
from eight_coupons.db.async import db


class EightCouponsHandler:

    async def games(self, request):
        """
        API endpoint to search against games

        :param: search
          A "search" parameter taken from GET query string. Should contain
          a search string, which may consist of multiple words to search
          against the database. Words are searched separately, i.e. a search
          against "android ios" would return the same results as two separate
          searches against "android" and "ios" (excluding duplicates). Use
          spaces, commas or any other punctuation symbols to separate multiple
          words, i.e. "android ios" is the same as "android,ios".

        TODO: Add limit and offset parameters
        """
        search_params = {}
        search_str = request.GET.get('search')
        # If there's something to search, create a search criteria,
        # otherwise just return all games
        if search_str:
            game_ids = set()
            for stem in split_stems(search_str):
                # Get game ids found for each stem
                index_item = await db.search_index.find_one({"stem": stem})
                if index_item:
                    game_ids = game_ids.union(index_item["game_ids"])
            # Add any found ids into search criteria
            if game_ids:
                search_params = {"id": {"$in": list(game_ids)}}
        games = []
        # Search for ids found or just return all games
        async for game in db.games.find(search_params):
            # Drop MongoDB id for readability
            game.pop("_id")
            games.append(game)
        return web.Response(text=json.dumps({'games': games}),
                            content_type="application/json")
