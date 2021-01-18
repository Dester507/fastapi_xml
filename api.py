from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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
            xml_str = await request.body()
            response = await handle_xml(xml_str)
            print(response)
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
