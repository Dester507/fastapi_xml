from typing import Optional

from .plugin import load_plugins

import routes

PLUGINS = load_plugins(routes)


class PathOperationFactory:
    @staticmethod
    async def factory(namespace: str, method: str) -> Optional[bool]:
        try:
            return getattr(PLUGINS[namespace], method)
        except (KeyError, AttributeError):
            return None
