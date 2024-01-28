from aiohttp import web
from aiohttp_jinja2 import template


class HomeView(web.View):
    @template("home.html")
    async def get(self):
        return {"msg": "Hello Python!"}


class AboutView(web.View):
    @template("about.html")
    async def get(self):
        return {"data": "We are very good company!"}


class ContactView(web.View):
    @template("contact.html")
    async def get(self):
        return {"number": '5544332211', 'city': 'New-York'}
