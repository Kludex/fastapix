import glob
import os
from typing import Union

from rich.console import Console

from fastapix.context import Component, ProjectStructure
from fastapix.inference.analyzers import SettingsAnalyzer

# TODO: Limit the number of files. If surpass the threshold, ask for manual input.


def infer_project_structure(console: Console) -> ProjectStructure:
    python_pattern = os.getcwd() + "/**/*.py"

    settings_analyzer = SettingsAnalyzer()
    settings: Union[Component, None] = None

    for filename in glob.glob(python_pattern, recursive=True):
        with open(filename, "r") as f:
            content = f.read()
            if settings_analyzer.match(content):
                settings = Component(filename=filename, content=content)
                break

    # TODO: PR welcome to add a test for this case.
    if settings is None:
        console.print("[bold red]Could not infer the settings file.[/bold red]")
        raise RuntimeError()

    return ProjectStructure(settings=settings)
