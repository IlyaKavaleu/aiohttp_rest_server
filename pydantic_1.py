import json
from typing import List
from pydantic import BaseModel


class Tag(BaseModel):
    id: int
    channel: str


class User(BaseModel):
    user_id: int
    name: str
    lastname: str
    age: int
    email: str
    city: str
    tags: List[Tag]


user_obj = User(
    user_id=1,
    name='Jack',
    lastname='Pupkin',
    age=26,
    email='pupkin@gmail.com',
    city='Minsk',
    tags=[
        {'id': 1, 'channel': 'RTB'},
        {'id': 2, 'channel': 'OOR'},
        {'id': 3, 'channel': '1QR'},
    ]
)
print(user_obj)
with open('file.json', 'w') as f:
    data = user_obj.model_dump()
    json.dump(data, f, indent=2, ensure_ascii=False, default=str)

