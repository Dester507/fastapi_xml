import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()


@app.middleware("http")
async def process_time_handler(request: Request, call_next):
    if request.url == "http://127.0.0.1:8000/xml":
        start_point = time.time()
        response = ''
        try:
            route = await request.json()
            req = await create_req(route)
            response = await(eval(req))
        except (NameError, TypeError, SyntaxError) as ex:
            if isinstance(ex, NameError):
                return JSONResponse(status_code=404, content="Method does not exist")
            elif isinstance(ex, TypeError):
                return JSONResponse(status_code=404, content="Error with arguments")
            elif isinstance(ex, SyntaxError):
                return JSONResponse(status_code=404, content="Method name is void")
        end_point = time.time() - start_point
        if isinstance(response, dict):
            response = JSONResponse(response)
        response.headers["X-Process-Time"] = str(end_point)
        return response
    else:
        response = await call_next(request)
        return response


@app.get("/xml/hello")
async def hello_world():
    return {"msg": "Hello world!"}


@app.get("/xml/say_gg")
async def say_gg(name: str, age: int):
    return {"msg": "gg", "name": name, "age": age}


# Create method path
async def create_req(route: dict):
    req = ''
    req += route['method'] + '('
    for attr in route['attrs']:
        if isinstance(route['attrs'][attr], str):
            req += attr + '=' + f'"{route["attrs"][attr]}"' + ', '
        else:
            req += attr + '=' + f'{route["attrs"][attr]}' + ', '
    req += ')'
    return req

'''
Second Variant:
Example in middleware:

route = await request.json()
response = await routes[route['method']]['method']()


routes = {
    'say_gg': {
      "method": say_gg,
      "attrs": [name]
    },
    'hello_world': {
      "method": hello_world,
      "attrs": []
    }
}
'''