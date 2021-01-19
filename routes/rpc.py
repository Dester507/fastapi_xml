from pydantic import BaseModel
from fastapi import Body, APIRouter, Request
from fastapi.routing import APIRoute
from typing import Optional

from api import rpc_api

'''
class Foo(BaseModel):
    name: str
    age: int
    surname: Optional[str] = None
    father: Optional[str] = None


print(dir(Foo.__fields__["name"]))
print(Foo.__fields__["name"]._type_display())
'''


class Fo(BaseModel):
    qq: str


@rpc_api.post("/hello/{msg}")
async def hello_world(msg: str, ms: Fo):
    return {"ms": ms.qq, "msg": msg}


@rpc_api.post("/say_gg")
async def say_gg(name: Optional[str], age: Optional[int], surname: Optional[str] = None, father: Optional[str] = None):
    if surname and father:
        return {"msg": "gg", "name": name, "age": age, "surname": surname, "father": father}
    elif surname:
        return {"msg": "gg", "name": name, "age": age, "surname": surname}
    elif father:
        return {"msg": "gg", "name": name, "age": age, "father": father}
    else:
        return {"msg": "gg", "name": name, "age": age}


print(dir(rpc_api.routes[4]))
print(dir(rpc_api.routes[4].handle))
print(rpc_api.routes[4].handle())


def return_routes_for_openapi():
    return rpc_api.routes
