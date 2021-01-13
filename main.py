from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from lxml import etree as et

app = FastAPI(title="Main Default API")
rpc_api = FastAPI(title="Support RPC-XML API")


@rpc_api.middleware("http")
async def process_time_handler(request: Request, call_next):
    import methods
    try:
        xml_str = await request.body()
        route = await make_json(xml_str)
        response = await getattr(methods, route['method'])(**route["attrs"])
    except NameError:
        return JSONResponse(status_code=404, content="Method does not exist")
    except TypeError:
        return JSONResponse(status_code=404, content="Error with arguments")
    except SyntaxError as ex:
        return JSONResponse(status_code=404, content="Method name is void")
    try:
        if isinstance(response, dict):
            response = JSONResponse(response)
        return response
    except:
        return JSONResponse(status_code=404, content="Bad response")


async def make_json(xml_str):
    tree = et.XML(xml_str)
    method_name = tree.xpath("//methodName")[0].text
    params = tree.xpath("//params/param")
    attrs = {}
    for pa in params:
        pa_name = pa.get('name')
        pa_type = pa.getchildren()[0].getchildren()[0].tag
        pa_attr = pa.getchildren()[0].getchildren()[0].text
        attrs[pa_name] = await switch_type(pa_attr, pa_type)
    return {"method": method_name, "attrs": attrs}


async def switch_type(param, type_pa):
    try:
        if type_pa == "str":
            str(param)
        elif type_pa == "int":
            int(param)
        elif type_pa == 'float':
            float(param)
        elif type_pa == "bool":
            bool(param)
        return param
    except:
        # JSONResponse 'Attr type error'
        pass

app.mount("/xml", rpc_api)
