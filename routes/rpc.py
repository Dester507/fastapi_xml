from fastapi import Body
from typing import Optional

from api import rpc_api


@rpc_api.post("/hello")
async def hello_world():
    return {"msg": "Hello world!"}


@rpc_api.post("/say_gg")
async def say_gg(name: str = Body(...), age: int = Body(...), surname: Optional[str] = None, father: Optional[str] = None):
    if surname and father:
        return {"msg": "gg", "name": name, "age": age,  "surname": surname, "father": father}
    elif surname:
        return {"msg": "gg", "name": name, "age": age, "surname": surname}
    elif father:
        return {"msg": "gg", "name": name, "age": age, "father": father}
    else:
        return {"msg": "gg", "name": name, "age": age}
