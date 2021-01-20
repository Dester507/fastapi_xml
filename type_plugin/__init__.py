from typing import Optional, Callable

from .plugin import load_plugins

import routes

PLUGINS = load_plugins(routes)


class PathOperationFactory:
    @staticmethod
    async def factory(namespace: str, method: str, *args, **kwargs) -> Optional[Callable]:
        try:
            return await getattr(PLUGINS[namespace], method)(*args, **kwargs)
        except (KeyError, AttributeError):
            return None
