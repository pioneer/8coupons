"""
.. module:: routes.py

Routes setup for HTTP API
"""


def setup_routes(app, handler, project_root):
    """
    Setting up routes for HTTP API

    :param: app
      Aiohttp app object to add routes to

    :param: handler
      A class instance which contains actual views to route to

    :param: project_root
      NOT USED: A directory containing project root, for static files
      if needed
    """
    add_route = app.router.add_route
    add_route('GET', '/games', handler.games)
