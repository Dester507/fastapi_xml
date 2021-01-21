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
async def say_gg(user: Foo):
    if user.surname and user.father:
        return {"msg": "gg", "name": user.name, "age": user.age, "surname": user.surname, "father": user.father}
    elif user.surname:
        return {"msg": "gg", "name": user.name, "age": user.age, "surname": user.surname}
    elif user.father:
        return {"msg": "gg", "name": user.name, "age": user.age, "father": user.father}
    else:
        return {"msg": "gg", "name": user.name, "age": user.age}


print(rpc_api.url_path_for(name='say_gg'))
print(rpc_api.url_path_for(name="hello_world"))


def return_routes_for_openapi():
    return rpc_api.routes
