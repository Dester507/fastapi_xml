from typing import Optional

from pydantic import BaseModel

from api import rpc_api


class Foo(BaseModel):
    name: str
    age: int
    surname: Optional[str] = None
    father: Optional[str] = None


'''
print(dir(Foo.__fields__["name"]))
print(Foo.__fields__)
print(Foo.__fields__["age"]._type_display())
'''


@rpc_api.post("/hello")
async def hello_world():
    return {"ms": "Hello world!"}


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
