import glob
import os
from typing import Union

from rich.console import Console

from fastapix.context import Component, ProjectStructure
from fastapix.inference.analyzers import ApplicationAnalyzer, SettingsAnalyzer

# TODO: Limit the number of files. If surpass the threshold, ask for manual input.


def infer_project_structure(console: Console) -> ProjectStructure:
    python_pattern = os.getcwd() + "/**/*.py"

    settings_analyzer = SettingsAnalyzer()
    settings: Union[Component, None] = None

    app_analyzer = ApplicationAnalyzer()
    app: Union[Component, None] = None

    filenames = iter(glob.glob(python_pattern, recursive=True))
    filename = next(filenames, None)
    while filename and (app is None or settings is None):
        with open(filename, "r") as f:
            content = f.read()
            if settings_analyzer.match(content):
                settings = Component(filename=filename, content=content)
            if app_analyzer.match(content):
                app = Component(filename=filename, content=content)
        filename = next(filenames, None)

    # TODO: PR welcome to add a test for this case.
    if settings is None:  # pragma: no cover
        console.print("[bold red]Could not infer the settings file.[/bold red]")
        raise RuntimeError()

    # TODO: PR welcome to add a test for this case.
    if app is None:  # pragma: no cover
        console.print("[bold red]Could not infer the application file.[/bold red]")
        raise RuntimeError()

    return ProjectStructure(settings=settings, app=app)
