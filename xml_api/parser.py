import asyncio

from lxml import etree as et

from .xml_parser_settings import xml2py, schema


async def handle_xml(xml_text):
    try:
        from type import PathOperationFactory
        xml_request = await parser_run(xml_text)
        method_name = xml_request.xpath("//methodName[1]")[0].text
        kwargs = {}
        args = list(
            map(
                xml2py,
                xml_request.xpath("//params/param/value")
            )
        )
        if isinstance(args[-1], dict):
            kwargs = args.pop(-1)
        method_name = method_name.split('_', 1)
        method_namespace = f"routes.{method_name[0]}"
        response = await PathOperationFactory.factory(method_namespace, method_name[1], *args, **kwargs)
        if response is None:
            return send_response(await create_bad_response(""))
        return response
    except:
        await send_response(await create_bad_response(""))


async def parser_run(xml_text):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(
            None,
            parser,
            xml_text
        )
    except et.DocumentInvalid as ex:
        await send_response(create_bad_response)  # ErrorResponse


def parser(xml_text):
    parse = et.XMLParser(resolve_entities=False)
    root = et.fromstring(xml_text, parse)
    schema.assertValid(root)
    return root


async def create_good_response(json_format_response):  # Response
    pass


async def create_bad_response(json_format_response):  # Error Response XML
    pass


async def send_response(response):
    pass
