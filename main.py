from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from lxml import etree

app = FastAPI(title="Main Default API")
rpc_api = FastAPI(title="Support RPC-XML API")


@rpc_api.middleware("http")
async def process_time_handler(request: Request, call_next):
    import methods
    try:
        route = await request.json()
        response = await getattr(methods, route['method'])(**route["attrs"])
    except NameError:
        return JSONResponse(status_code=404, content="Method does not exist")
    except TypeError:
        return JSONResponse(status_code=404, content="Error with arguments")
    except SyntaxError as ex:
        print(ex)
        return JSONResponse(status_code=404, content="Method name is void")
    try:
        if isinstance(response, dict):
            response = JSONResponse(response)
        return response
    except:
        return JSONResponse(status_code=404, content="Bad response")

app.mount("/xml", rpc_api)
