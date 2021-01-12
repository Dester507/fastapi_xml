from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from lxml import etree

app = FastAPI(title="XML API")


@app.middleware("http")
async def process_time_handler(request: Request, call_next):
    if request.url == "http://127.0.0.1:8000/xml":
        response = ''
        try:
            route = await request.json()
            if route["method"] not in allowed_methods:
                return JSONResponse(status_code=404, content="Method does not exist")
            req = await create_req(route)
            print(req)
            response = await(eval(req))
        except (NameError, TypeError, SyntaxError) as ex:
            if isinstance(ex, NameError):
                return JSONResponse(status_code=404, content="Method does not exist")
            elif isinstance(ex, TypeError):
                return JSONResponse(status_code=404, content="Error with arguments")
            elif isinstance(ex, SyntaxError):
                return JSONResponse(status_code=404, content="Method name is void")
        if isinstance(response, dict):
            response = JSONResponse(response)
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


allowed_methods = ["say_gg", "hello_world"]

