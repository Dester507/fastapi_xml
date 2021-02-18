from typing import Optional, Callable
from functools import wraps

from pydantic import BaseModel
from fastapi.types import DecoratedCallable

from api import rpc_api


class Foo(BaseModel):
    name: str
    age: int


def api_router(ns: str) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(func) -> Callable:
        @wraps(func)
        @rpc_api.post(path=f"/{ns}/{func.__name__}", name=f'{ns}_{func.__name__}')
        async def wrap():
            return await func()
        return wrap
    return decorator


@rpc_api.post("/test1")
async def test1():
    return {"msg": "Test1 good"}


@api_router("rpc")
async def hello_world():
    return {"ms": "Hello world! RPC"}


@rpc_api.post("/say_gg")
async def say_gg(name: str, age: int):
    return {"msg": "gg", "name": name, "age": age}


def return_routes_for_openapi():
    return rpc_api.routes
