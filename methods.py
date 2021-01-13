#from pydantic import BaseModel
from fastapi import Body

from main import rpc_api


@rpc_api.post("/hello")
async def hello_world():
    return {"msg": "Hello world!"}


@rpc_api.post("/say_gg")
async def say_gg(name: str = Body(...), age: int = Body(...)):
    return {"msg": "gg", "name": name, "age": age}
