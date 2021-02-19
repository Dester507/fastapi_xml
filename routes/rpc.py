from typing import Optional, Callable
from functools import wraps

from pydantic import BaseModel
from fastapi.types import DecoratedCallable
from fastapi import APIRouter


router = APIRouter(prefix="/rpc")


class Foo(BaseModel):
    name: str
    age: int


def api_router(router: APIRouter, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(func) -> Callable:
        @router.post(path=f"/{func.__name__}", name=f'{router.prefix}_{func.__name__}', **kwargs)
        @wraps(func)
        async def wrap(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrap
    return decorator


# @rpc_api.post("/test1")
# async def test1():
#     return {"msg": "Test1 good"}


@api_router(router)
async def hello_world(name: str):
    return {"ms": "Hello world! RPC", "name": name}


# @rpc_api.post("/say_gg")
# async def say_gg(name: str, age: int):
#     return {"msg": "gg", "name": name, "age": age}


# def return_routes_for_openapi():
#     return rpc_api.routes
