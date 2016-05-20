
def setup_routes(app, handler, project_root):
    add_route = app.router.add_route
    add_route('GET', '/games', handler.games)
