import textwrap
from pathlib import Path

from typer.testing import CliRunner

from fastapix.main import app


def test_env_command(tmp_path: Path) -> None:
    content = textwrap.dedent(
        """
        from pydantic import BaseSettings

        class Settings(BaseSettings):
            foo: str = "bar"
            bar: int
        """
    )
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        file = Path(td) / "settings.py"
        file.write_text(content)
        output = Path(td) / "output.md"
        result = runner.invoke(app, ["env", "--output", str(output)])
        assert result.exit_code == 0, result.stdout
        with output.open("r") as f:
            content = f.read()
            expected = (
                "| Name | Description |  Type   | Default | Required |",
                "| ---- | ----------- | :-----: | :-----: | :------: |",
                "| foo  | -           | string  |   bar   |    ❌    |",
                "| bar  | -           | integer |    -    |    ✅    |",
            )
            assert all(line in content for line in expected)
