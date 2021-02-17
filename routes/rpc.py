from typing import Optional

from pydantic import BaseModel

from api import rpc_api


class Foo(BaseModel):
    name: str
    age: int
    surname: Optional[str] = None
    father: Optional[str] = None


@rpc_api.post("/test1")
async def test1():
    return {"msg": "Test1 good"}


@rpc_api.post("/hello")
async def hello_world():
    return {"ms": "Hello world! RPC"}


@rpc_api.post("/say_gg")
async def say_gg(name: str, age: int, surname: Optional[str] = None, father: Optional[str] = None):
    if surname and father:
        return {"msg": "gg", "name": name, "age": age, "surname": surname, "father": father}
    elif surname:
        return {"msg": "gg", "name": name, "age": age, "surname": surname}
    elif father:
        return {"msg": "gg", "name": name, "age": age, "father": father}
    else:
        return {"msg": "gg", "name": name, "age": age}


def return_routes_for_openapi():
    return rpc_api.routes
