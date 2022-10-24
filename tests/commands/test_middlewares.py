import textwrap
from pathlib import Path

from typer.testing import CliRunner

from fastapix.main import app


def test_middlewares_command(tmp_path: Path) -> None:
    content = textwrap.dedent(
        """
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        """
    )
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        file = Path(td) / "main.py"
        file.write_text(content)
        result = runner.invoke(app, ["middlewares"])
        assert result.exit_code == 0, result.stdout
        expected = textwrap.dedent(
            """
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ middleware     ┃ parameter         ┃ value ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ CORSMiddleware │ allow_origins     │ ['*'] │
│                │ allow_credentials │ True  │
│                │ allow_methods     │ ['*'] │
│                │ allow_headers     │ ['*'] │
└────────────────┴───────────────────┴───────┘
 """
        )
        assert expected in result.stdout, result.stdout
