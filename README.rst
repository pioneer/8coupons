8 coupons demo
==============

How to use
==========

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
* aiohttp
* motor
* requests
* snowballstemmer
* BeautifulSoup


TODO
====
* tests
* scaling
* spelling errors processing via Levenstein algorythm
* more flexible scraping in order to allow extending with more sources
* multi-threaded scraping and totally switching to async db access
* limit and offset parameters for splitting the results
* MongoDB index for "id" field
* bonus points
