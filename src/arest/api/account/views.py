from aiohttp import web

from src.arest.api.account.models import User


class Account(web.View):
    async def get(self):
        return web.json_response({'message': 'OK'})

    async def post(self):
        data = await self.request.json()
        new_user = User(**data)
        new_user.set_password()
        await new_user.save()
        return web.json_response({'id': str(new_user.uuid)})


class Token(web.View):
    async def post(self):
        data = await self.request.json()
        user = await User.get(username=data['username'])
        if user.check_passwd(data['password']):
            # refresh =
            return web.json_response({'msg': 'OK'})
        return web.json_response({'msg': 'Not found'}, status=401)

