from inspect import getmembers
from typing import Union

import typer
from fastapi import FastAPI
from rich.table import Table

from fastapix.context import Context
from fastapix.loader import import_from_filename

app = typer.Typer(name="middlewares", help="List FastAPI middlewares.")


@app.callback(invoke_without_command=True)  # type: ignore[misc]
def middlewares(ctx: Context) -> None:
    if ctx.obj.structure.app is None:  # pragma: no cover
        ctx.obj.console.print("No app found.")
        raise typer.Exit(2)

    module = import_from_filename(ctx.obj.structure.app.filename)
    app: Union[FastAPI, None] = None
    # TODO: Support factory functions.
    for name, value in getmembers(module):
        if isinstance(value, FastAPI):
            app = value

    # TODO: PR welcome to add test.
    if app is None:  # pragma: no cover
        raise RuntimeError("Could not find FastAPI instance.")

    headers = ("middleware", "parameter", "value")
    middlewares = [
        (
            middleware.cls.__name__,
            "\n".join(str(key) for key in middleware.options.keys()),
            "\n".join(str(value) for value in middleware.options.values()),
        )
        for middleware in app.user_middleware
    ]
    for middleware in app.user_middleware:
        print(middleware.cls, middleware.options)
    table = Table(show_header=True, header_style="bold magenta")
    for column in headers:
        table.add_column(column)
    for middleware in middlewares:
        table.add_row(*middleware)
    ctx.obj.console.print(table)
