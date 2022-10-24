import platform

import typer

__version__ = "0.1.0"

app = typer.Typer(name="FastAPI X", help="Manage your FastAPI project.")


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
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    ...  # pragma: no cover
