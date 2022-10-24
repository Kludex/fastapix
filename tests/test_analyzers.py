import pytest

from fastapix.inference.analyzers import SettingsAnalyzer


@pytest.mark.parametrize(
    "content, expected",
    [
        ("class Settings(BaseSettings):", True),
        ("class Potato(Settings):", False),
    ],
)
def test_settings_analyzer(content: str, expected: bool) -> None:
    analyzer = SettingsAnalyzer()
    assert analyzer.match(content) == expected
