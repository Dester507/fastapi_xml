import importlib
import pkgutil


def iter_namespace(ns):
    return pkgutil.iter_modules(ns.__path__, ns.__name__ + '.')


def load_plugins(namespace):
    plugins = {}

    for finder, name, _ in iter_namespace(namespace):
        module = importlib.import_module(name)
        plugins[name] = module
    return plugins
