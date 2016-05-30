8 coupons demo
==============

How to use
==========
Install MongoDB::

Install requirements::

    $ pip install -r requirements.txt

Run HTTP API server::

    $ make runserver

Run scraper in a separate console::

    $ make runscraper

API endpoint::

    http://localhost:8080/games?search=<search string>


Requirements
============
Python 3.5+, MongoDB and the libraries below:
* aiohttp
* motor
* requests
* snowballstemmer
* BeautifulSoup


Main components
===============
* HTTP API server
* MongoDB storage
* Scraping and indexing background worker


Configuring
===========
Most of the values worth to configure are extracted into `settings.py`. Feel
free to set them up according to your project environment.


How it works
============
The scraper runs periodically in background and grabs the fresh games data
from GiantBomb API. The games added since last run are added to the database,
along with updating the search index for each newly appeared game.

The index is built using Snowball stemmer, by extracting stems from each
field which is configured in settings to be under indexing. The index is a set
of records like `{<stem>: [a list of game ids containing this stem]}`.
Searching against the index is searching for given stems, extracting game ids
linked to each stem and returning those games.

Example: we have configured in `settings.py` that the fields of interest are
"name" and "description". Then, two new games come:

    {"id": 1,
     "name": "Arkanoid: New Horizons",
     "description": "The reincarnation of well-known Arkanoid game.",
     "image": "http://static.giantbomb.com/images/1.jpg",
     "date_added": "2016-05-30 15:16:51",
     "tags": "arcade,arkanoid,breakout,old,platformer,new"}

    {"id": 2,
     "name": "Pacman 3D",
     "description": "Our old friend Pacman appears in 3D with brand " +
                    "new graphics, monsters and labyrinths.",
     "image": "http://static.giantbomb.com/images/2.jpg",
     "date_added": "2016-05-30 15:25:13",
     "tags": "arcade,pacman,3d,old,platformer,new"}

The indexer parses "name" and "description" of both games, omitting all
other fields. So, the words like "platformer" and "arcade" from tags will not
come into the index.

First game gives "arkanoid", "new", "horizon" stems extracted from name,
and "the", "reincarn", "of", "well", "known", "arkanoid", "game" stems
extracted from description.

Second game produces "pacman", "3d" and "our", "old", "friend", "pacman",
"appear", "in", "3d", "with", "brand", "new", "graphics", "monster", "and",
"labyrinth" respectively. Notice the "new" stem appears in both games.

After updating the index, assuming it was initially empty, the index will look
like below:

    {"stem": "arkanoid", "game_ids": [1]}
    {"stem": "new", "game_ids": [1, 2]}
    {"stem": "horizon", "game_ids": [1]}
    {"stem": "the", "game_ids": [1]}
    {"stem": "reincarn", "game_ids": [1]}
    {"stem": "of", "game_ids": [1]}
    {"stem": "well", "game_ids": [1]}
    {"stem": "known", "game_ids": [1]}
    {"stem": "game", "game_ids": [1]}
    {"stem": "pacman", "game_ids": [2]}
    {"stem": "3d", "game_ids": [2]}
    {"stem": "our", "game_ids": [2]}
    {"stem": "old", "game_ids": [2]}
    {"stem": "friend", "game_ids": [2]}
    {"stem": "appear", "game_ids": [2]}
    {"stem": "in", "game_ids": [2]}
    {"stem": "with", "game_ids": [2]}
    {"stem": "brand", "game_ids": [2]}
    {"stem": "graphics", "game_ids": [2]}
    {"stem": "monster", "game_ids": [2]}
    {"stem": "and", "game_ids": [2]}
    {"stem": "labyrinth", "game_ids": [2]}

Then, if a search appears by using search string "new game",

    http://localhost:8080/games?search=new+game

the HTTP API server will look for "new" and "game" stems in the index,
which contains [1, 2] for "new" and [1] for "game", so thus resulting in
both games in output:

    {"games":
        {"id": 1,
         "name": "Arkanoid: New Horizons",
         "description": "The reincarnation of well-known Arkanoid game.",
         "image": "http://static.giantbomb.com/images/1.jpg",
         "date_added": "2016-05-30 15:16:51",
         "tags": "arcade,arkanoid,breakout,old,platformer,new"}

        {"id": 2,
         "name": "Pacman 3D",
         "description": "Our old friend Pacman appears in 3D with brand " +
                        "new graphics, monsters and labyrinths.",
         "image": "http://static.giantbomb.com/images/2.jpg",
         "date_added": "2016-05-30 15:25:13",
         "tags": "arcade,pacman,3d,old,platformer,new"}}

The search against, for example, "monster" will return just the second game,
and the search against "horizon" will return only the first one.


TODO
====
* tests
* scaling
* spelling errors processing via Levenstein algorythm
* remove words like "the", "of" from using in index
* more flexible scraping in order to allow extending with more sources
* multi-threaded scraping and totally switching to async db access
* limit and offset parameters for splitting the results
* MongoDB index for "id" field
* bonus points
