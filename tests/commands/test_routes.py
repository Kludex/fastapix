import textwrap
from pathlib import Path

from typer.testing import CliRunner

from fastapix.main import app


def test_routes_command(tmp_path: Path) -> None:
    content = textwrap.dedent(
        """
        from fastapi import FastAPI

        app = FastAPI()

        @app.get("/")
        def index():
            return {"message": "Hello World!"}
        """
    )
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        file = Path(td) / "main.py"
        file.write_text(content)
        result = runner.invoke(app, ["routes"])
        assert result.exit_code == 0, result.stdout
        expected = textwrap.dedent(
            """┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ name                ┃ path                  ┃ methods         ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ index               │ /                     │ ['GET']         │
│ swagger_ui_html     │ /docs                 │ ['GET', 'HEAD'] │
│ swagger_ui_redirect │ /docs/oauth2-redirect │ ['GET', 'HEAD'] │
│ openapi             │ /openapi.json         │ ['GET', 'HEAD'] │
│ redoc_html          │ /redoc                │ ['GET', 'HEAD'] │
└─────────────────────┴───────────────────────┴─────────────────┘
 """
        )
        assert expected in result.stdout
