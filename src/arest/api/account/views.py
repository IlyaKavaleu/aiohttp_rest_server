import uuid
from aiohttp import web
import asyncio
from src.arest.api.account.models import User
import jwt
from datetime import datetime, timedelta
from src.arest.conf import settings

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
            tid = str(uuid.uuid4())
            refresh = jwt.encode(
                {
                    'uuid': str(user.uuid),
                    'tid': tid,
                    'exp': datetime.utcnow() + timedelta(days=7),
                    'iss': 'refresh',
                },
                settings.SECRET_KEY,
                algorithm='HS256'
            )
            access = jwt.encode(
                {
                    'uuid': str(user.uuid),
                    'tid': tid,
                    'exp': datetime.utcnow() + timedelta(seconds=settings.EXP_TIME),
                    'iss': 'access',
                    'aud': ['C', 'R', 'U', 'D']
                }
            )
            user.refresh = refresh
            await user.save()
            return web.json_response({'refresh': refresh, 'access': access})
        await asyncio.sleep(3)
        return web.json_response({'msg': 'Not found'}, status=401)

