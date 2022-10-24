import platform
from pathlib import Path

import typer
from appdirs import user_cache_dir
from rich.console import Console

from fastapix.commands.environment import app as env_app
from fastapix.commands.middlewares import app as middlewares_app
from fastapix.commands.routes import app as routes_app
from fastapix.context import Context, ContextObject
from fastapix.inference import infer_project_structure

__version__ = "0.1.0"


app = typer.Typer(name="FastAPI X", help="Manage your FastAPI project.")
app.add_typer(env_app)
app.add_typer(routes_app)
app.add_typer(middlewares_app)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(
            "Running FastAPI X {} with {} {} on {}.".format(
                __version__,
                platform.python_implementation(),
                platform.python_version(),
                platform.system(),
            )
        )
        raise typer.Exit(0)


@app.callback()  # type: ignore[misc]
def main(
    ctx: Context,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    console = Console()

    cache_dir = Path(user_cache_dir("fastapix"))
    cache_dir.mkdir(exist_ok=True)

    # TODO: Create an entry per project. Each entry that represents a file should have
    # a hash.

    project_structure = infer_project_structure(console)
    ctx.obj = ContextObject(console=console, structure=project_structure)
