from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from xml_api.parser import handle_xml


app = FastAPI(title="Main API", description="Default api for simple requests")


@app.get('/hello')
def hello_main():
    return {"msg": "Hello World!"}


rpc_api = FastAPI(title="Support RPC-XML API", description="Mounted app for rpc-xml requests", version="0.3.1")


@rpc_api.middleware("http")
async def process_time_handler(request: Request, call_next):
    if request.url == "http://127.0.0.1:8000/xml/":
        try:
            print(await request.body())
            xml_str = await request.body()
            response = await handle_xml(xml_str)
        except NameError:
            return JSONResponse(status_code=404, content="Method does not exist")
        except TypeError:
            return JSONResponse(status_code=404, content="Error with arguments")
        except SyntaxError:
            return JSONResponse(status_code=404, content="Method name is void")
        try:
            if isinstance(response, dict):
                response = JSONResponse(response)
            return response
        except:
            return JSONResponse(status_code=404, content="Bad response")
    else:
        response = await call_next(request)
        return response


app.mount("/xml", rpc_api)


def get_routes_rpc_api():
    from routes import rpc
    return rpc.return_routes_for_openapi()


openapi_schema_rpc_api = get_openapi(
    title="Rpc docs",
    version="2.5.0",
    description="Open Api custom",
    routes=get_routes_rpc_api()
)

'''
class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


async def custom_route_handler(request: Request) -> Response:
    orig = rpc_api.routes[4].get_route_handler()
    request = GzipRequest(request.scope, request.receive)
    return await orig(request)
'''

rpc_api.openapi_schema = openapi_schema_rpc_api
