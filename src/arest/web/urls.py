from aiohttp_controller.controller import Controller
from src.arest.web.home.views import HomeView

Controller.include("/src/api", "src.arest.api.urls")
Controller.add("/", HomeView, name="home_page", method=["GET"])

