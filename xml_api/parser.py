import asyncio

import requests
from fastapi.responses import JSONResponse
from lxml import etree as et

from .xml_parser_settings import xml2py, schema


XML_URL = "http://127.0.0.1:8000/xml"


async def handle_xml(xml_text):
    try:
        from type_plugin import PathOperationFactory
        from routes.rpc import rpc_api
        xml_request = await parser_run(xml_text)
        method_name = xml_request.xpath("//methodName[1]")[0].text
        kwargs = {}
        args = list(
            map(
                xml2py,
                xml_request.xpath("//params/param/value")
            )
        )
        try:
            if isinstance(args[-1], dict):
                kwargs = args.pop(-1)
        except IndexError:
            kwargs = {}
        method_name = method_name.split('_', 1)
        method_namespace = f"routes.{method_name[0]}"
        method_exit = await PathOperationFactory.factory(method_namespace, method_name[1])
        if method_exit is not None:
            method_url = rpc_api.url_path_for(method_name[1])
            arg_names = method_exit.__code__.co_varnames
            data = await request_data_create(arg_names, args)
            print(data)
            url_for_req = XML_URL + method_url
            print(url_for_req)
        else:
            return await create_bad_response("Method does not exist.")
        return url_for_req
    except TypeError as ex:
        print(ex)
        return await create_bad_response("Error with arguments")
    except Exception as ex:
        print(ex, type(ex))
        return await create_bad_response("Error with parse xml request.")


async def parser_run(xml_text):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(
            None,
            parser,
            xml_text
        )
    except et.DocumentInvalid as ex:
        return await create_bad_response("Invalid xml.")  # ErrorResponse


def parser(xml_text):
    parse = et.XMLParser(resolve_entities=False)
    root = et.fromstring(xml_text, parse)
    schema.assertValid(root)
    return root


async def request_data_create(args_name, attrs):
    # Parse kwargs in future
    request_body = {}
    try:
        if len(attrs) < len(args_name):
            for i in range(len(args_name) - len(attrs)):
                attrs.append(None)
        for idx in range(len(args_name)):
            request_body[args_name[idx]] = attrs[idx]
        return request_body
    except:
        raise TypeError


async def create_good_response(json_msg):  # Response
    return JSONResponse(status_code=200, content=json_msg)


async def create_bad_response(json_msg):  # Error Response XML
    return JSONResponse(status_code=404, content=json_msg)
