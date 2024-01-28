from aiohttp_controller.controller import Controller

Controller.include('/user', 'src.arest.api.account.urls')
