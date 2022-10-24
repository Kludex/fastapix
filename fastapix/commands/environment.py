"""
Command that prints out the environment variables that are used.
"""
import io
import json
from inspect import getmembers, isclass
from pathlib import Path
from typing import Type

import libcst as cst
import libcst.matchers as m
import typer
from pydantic import BaseSettings
from pytablewriter.style import Style
from pytablewriter.writer import MarkdownTableWriter

from fastapix.context import Context
from fastapix.loader import import_from_filename

app = typer.Typer(name="env", help="Print out the environment variables used.")


# TODO: Add template option.
# TODO: Use rich if output is stdout.
@app.callback(invoke_without_command=True)  # type: ignore[misc]
def main(
    ctx: Context,
    output: Path = typer.Option(Path("/dev/stdout"), help="Output filename."),
) -> None:
    """Print out the environment variables used."""
    if ctx.obj.structure.settings is None:  # pragma: no cover
        ctx.obj.console.print("No settings found.")
        raise typer.Exit(2)

    module = import_from_filename(ctx.obj.structure.settings.filename)

    for name, value in getmembers(module):
        if isclass(value) and issubclass(value, BaseSettings) and value != BaseSettings:
            show_environment(settings_class=value, output=output)


def show_environment(settings_class: Type[BaseSettings], output: Path) -> None:
    table = []

    schema_json = json.loads(settings_class.schema_json())
    properties = schema_json["properties"]
    required = schema_json.get("required", [])

    for key, value in properties.items():
        required_column = "✅" if key in required else "❌"
        table.append(
            [
                key,
                value.get("description", "-"),
                value["type"],
                str(value.get("default", "-")),
                required_column,
            ]
        )

    writer = MarkdownTableWriter(
        headers=["Name", "Description", "Type", "Default", "Required"],
        value_matrix=table,
        margin=1,
    )
    writer.set_style(2, Style(align="center"))
    writer.set_style(3, Style(align="center"))
    writer.set_style(4, Style(align="center"))
    writer.stream = io.StringIO()
    writer.write_table()

    with output.open("w") as fp:
        fp.write(writer.stream.getvalue())


# TODO: Use CST instead of loading the module.
class BaseSettingsVisitor(cst.CSTVisitor):  # type: ignore[misc]  # pragma: no cover
    def __init__(self) -> None:
        self.inside_settings = False

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        for base in node.bases:
            if m.matches(base, m.Arg(value=m.Name("BaseSettings"))):
                self.inside_settings = True

    def leave_ClassDef(self, original_node: cst.ClassDef) -> None:
        self.inside_settings = False
