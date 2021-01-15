import asyncio
import os
from datetime import datetime
from types import GeneratorType

from functools import singledispatch, wraps

from lxml import etree as et

schema = et.RelaxNG(file=os.path.join(os.path.abspath(os.path.dirname(__file__)), "xmlrpc.rng"))
XML2PY_TYPES = {}

@singledispatch
def py2xml(value):
    raise TypeError(("Can`t serialise type: {0}."
                     " Add type {0} via decorator "
                     "@py2xml.register({0}) ").format(type(value)))


@py2xml.register(bytes)
def _(value):
    value = value.decode()
    el = et.Element("string")
    el.text = str(value)
    return el


@py2xml.register(str)
def _(value):
    el = et.Element("string")
    el.text = str(value)
    return el


@py2xml.register(float)
def _(value):
    el = et.Element("double")
    el.text = str(value)


@py2xml.register(datetime)
def _(value):
    el = et.Element("dateTime.iso8601")
    el.text = value.strftime("%Y%m%dT%H:%M:%S")
    return el


@py2xml.register(int)
def _(value):
    if -2147483648 < value < 2147483648:
        el = et.Element("i4")
    else:
        el = et.Element("double")
    el.text = str(value)
    return el


@py2xml.register(bool)
def _(value):
    el = et.Element("boolean")
    el.text = "1" if value else "0"
    return el


@py2xml.register(type(None))
def _(value):
    return et.Element("nil")


@py2xml.register(list)
@py2xml.register(tuple)
@py2xml.register(set)
@py2xml.register(frozenset)
@py2xml.register(GeneratorType)
def _(x):
    array = et.Element("array")
    data = et.Element("data")
    array.append(data)

    for i in x:
        el = et.Element("value")
        el.append(py2xml(i))
        data.append(el)

    return array


@py2xml.register(dict)
def _(x):
    struct = et.Element("struct")

    for key, value in x.items():
        member = et.Element("member")
        struct.append(member)

        key_el = et.Element("name")
        key_el.text = str(key)
        member.append(key_el)

        value_el = et.Element("value")
        value_el.append(py2xml(value))
        member.append(value_el)

    return struct


def str_to_time(x):
    for form in ["%Y%m%dT%H:%M:%S", "%Y%m%dT%H%M%S"]:
        try:
            return datetime.strptime(x.text, form)
        except ValueError:
            pass

    raise ValueError(f"It`s impossible to parse datetime with formats {['%Y%m%dT%H:%M:%S', '%Y%m%dT%H%M%S']}")


def xml2py(value):
    def xml2struct(p):
        return dict(
            map(
                lambda x: (x[0].text, x[1]),
                zip(
                    p.xpath("./member/name"),
                    map(xml2py, p.xpath("./member/value"))
                )
            )
        )

    def xml2array(p):
        return list(map(xml2py, p.xpath("./data/value")))

    def unwrap_value(p):
        try:
            value = next(p.iterchildren())
        except StopIteration:
            value = p.text or ''
        return xml2py(value)

    XML2PY_TYPES.update({
        "string": lambda x: str(x.text).strip(),
        "struct": xml2struct,
        "array": xml2array,
        "boolean": lambda x: bool(int(x.text)),
        "dateTime.iso8601": lambda x: str_to_time(x),
        "double": lambda x: float(x.text),
        "integer": lambda x: int(x.text),
        "int": lambda x: int(x.text),
        "i4": lambda x: int(x.text),
        "nil": lambda x: None,
        "value": unwrap_value,
    })

    if isinstance(value, str):
        return value.strip()

    return XML2PY_TYPES.get(value.tag)(value)


def awaitable(func):
    if asyncio.iscoroutinefunction(func):
        return func

    async def awaiter(obj):
        return obj

    @wraps(func)
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)

        if hasattr(result, "__await__"):
            return result
        if asyncio.iscoroutine(result) or asyncio.isfuture(result):
            return result

        return awaiter(result)

    return wrap


__all__ = ("py2xml", "xml2py", "schema", "awaitable")
