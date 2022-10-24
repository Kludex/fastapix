from dataclasses import dataclass

from rich.console import Console
from typer import Context as _Context


@dataclass
class Component:
    filename: str
    content: str


@dataclass
class ProjectStructure:
    settings: Component


@dataclass
class ContextObject:
    console: Console
    structure: ProjectStructure


class Context(_Context):
    obj: ContextObject
