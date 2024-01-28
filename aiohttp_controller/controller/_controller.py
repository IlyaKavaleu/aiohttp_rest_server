import traceback
from importlib import import_module
from collections import namedtuple
from typing import TypeVar, Union, Iterator

View = TypeVar("View")
Route = namedtuple("Route", "method, path, handler, name")

__all__ = ("Controller", "ControllerError")


class ControllerError(Exception):
    """Controller extension."""


class Controller:
    __slots__ = ()

    _urlpatterns = set()
    _sub_path = ""

    @classmethod
    def add(
        cls, path: str, handler: View, *, name: str, method: str | tuple[str] = "GET"
    ) -> None:
        """Add a new relative route.

        :param path: relative resource path.
        :param handler: aiohttp view.
        :param name: the route name.
        :param method: ["GET", "POST", ...] or *
        """
        mtd = method if isinstance(method, (str, tuple)) else tuple(method)
        url = Route(mtd, "".join([cls._sub_path, path]), handler, name)
        cls._urlpatterns.add(url)

    @classmethod
    def include(cls, path: str, module: str) -> None:
        """Include a new file with urls.

        :param path: relative resource path.
        :param module: the module string value for import.
        :raises ControllerError: if any exception.
        """
        old_subpath = cls._sub_path
        cls._sub_path += path
        try:
            import_module(module)
        except ImportError as err:
            raise ControllerError(
                "Import {!r} from {!r}:\n".format(path, module)
            ) from err
        cls._sub_path = old_subpath

    @classmethod
    def get(cls, name: str) -> namedtuple:
        """Get a route by name.

        :param name: the route name.
        :return: route or None.
        :rtype: namedtuple | None
        """
        for route in list(cls._urlpatterns):
            if route.name == name:
                return route

    @classmethod
    def entry_point(cls, module: str) -> None:
        """Set the root module with urls.

        :param module: the module string value for import.
        :type module: str
        :raises ControllerError: if any exception.
        """
        try:
            import_module(module)
        except ImportError as err:
            raise ControllerError("Import {!r}:\n".format(module)) from err

    @classmethod
    def urls(cls) -> Iterator:
        """Routs iterator.

        :yield: routers iterator.
        :rtype: Iterator
        """
        for route in list(cls._urlpatterns):
            yield route