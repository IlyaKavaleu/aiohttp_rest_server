from ._controller import Controller, ControllerError

__version__ = "0.6.1"


def controller_setup(app, root_urls: str, cors: bool = False):
    """Initial routers.
    Example:
    ┌ app.py
    └ web ┐
          ├ root ┐
          │      ├ urls.py
          │      └ views.py
          └ home ┐
                 ├ urls.py
                 └ views.py
    ═══════════════════════════════════════
    app.py
    ───────────────────────────────────────
    from controller import controller_setup


    controller_setup(app, "web.root.urls")
    ═══════════════════════════════════════
    web/root/urls.py
    ───────────────────────────────────────
    from controller import Controller
    from web.root import views


    Controller.include("/home", "web.home.urls")
    Controller.add("", views.RootView, name="root_view")
    ═══════════════════════════════════════
    web/home/urls.py
    ───────────────────────────────────────
    from controller import Controller
    from web.home import views


    Controller.add("/about", views.AboutView, name="about_view")
    Controller.add("", views.HomeView, name="home_view")
    ═══════════════════════════════════════
    """
    Controller.entry_point(root_urls)
    if cors:
        import aiohttp_cors

        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                    max_age=3600,
                )
            },
        )
        for route in Controller.urls():
            resource = cors.add(app.router.add_resource(route.path, name=route.name))
            methods = tuple(route.method) if isinstance(route.method, str) else route.method
            for method in methods:
                cors.add(resource.add_route(method, route.handler))
        return
    for route in Controller.urls():
        methods = tuple(route.method) if isinstance(route.method, str) else route.method
        for method in methods:
            app.router.add_route(method, route.path, route.handler, name=route.name)