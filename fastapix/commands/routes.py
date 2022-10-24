from inspect import getmembers
from typing import Union

from fastapi import FastAPI
from rich.table import Table
from typer import Typer

from fastapix.context import Context
from fastapix.loader import import_from_filename

app = Typer(name="routes", help="List FastAPI routes.")


@app.callback(invoke_without_command=True)  # type: ignore[misc]
def routes(ctx: Context) -> None:
    module = import_from_filename(ctx.obj.structure.settings.filename)
    app: Union[FastAPI, None] = None
    for name, value in getmembers(module):
        if isinstance(value, FastAPI):
            app = value

    # TODO: PR welcome to add test.
    if app is None:  # pragma: no cover
        raise RuntimeError("Could not find FastAPI instance.")

    headers = ("name", "path", "methods")
    routes: list[tuple[str, str, str]] = []
    for route in app.routes:
        name = str(getattr(route, "name"))
        path = str(getattr(route, "path", None))
        methods = sorted(getattr(route, "methods", None) or {})
        routes.append((name, path, str(methods)))
    routes.sort(key=lambda x: x[1])
    table = Table(show_header=True, header_style="bold magenta")
    for column in headers:
        table.add_column(column)
    for route in routes:
        table.add_row(*route)
    ctx.obj.console.print(table)
