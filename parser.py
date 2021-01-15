import asyncio

from lxml import etree as et

from xml_parser_settings import py2xml, xml2py, awaitable, schema


async def handle_xml(xml_text):
    try:
        xml_request = await parser_run(xml_text)
        method_name = xml_request.xpath("//methodName[1]")[0].text
        method = await check_method(method_name)
        if method:
            import methods
            kwargs = {}
            args = list(
                map(
                    xml2py,
                    xml_request.xpath("//params/param/value")
                )
            )
            print(args)
            if isinstance(args[-1], dict):
                kwargs = args.pop(-1)
            response = await getattr(methods, method_name)(*args, **kwargs)
            return response
        else:
            pass  # ErrorResponse Method doesnt exist
    except:
        pass  # Error


async def parser_run(xml_text):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(
            None,
            parser,
            xml_text
        )
    except et.DocumentInvalid as ex:
        pass  # ErrorResponse


def parser(xml_text):
    parse = et.XMLParser(resolve_entities=False)
    root = et.fromstring(xml_text, parse)
    schema.assertValid(root)
    return root


async def create_good_response(json_format_response):  # Response
    pass


async def create_bad_response(json_format_response):  # Error Response XML
    pass


async def check_method(m_name):
    import methods
    status = hasattr(methods, m_name)
    return status
