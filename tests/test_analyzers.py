import pytest

from fastapix.inference.analyzers import ApplicationAnalyzer, SettingsAnalyzer


@pytest.mark.parametrize(  # type: ignore[misc]
    "content, expected",
    [
        ("class Settings(BaseSettings):", True),
        ("class Potato(Settings):", False),
    ],
)
def test_settings_analyzer(content: str, expected: bool) -> None:
    analyzer = SettingsAnalyzer()
    assert analyzer.match(content) == expected


@pytest.mark.parametrize(  # type: ignore[misc]
    "content, expected",
    [
        ("app = FastAPI()", True),
        ("return FastAPI(", True),
        ("def potato() -> FastAPI:", False),
    ],
)
def test_application_analyzer(content: str, expected: bool) -> None:
    analyzer = ApplicationAnalyzer()
    assert analyzer.match(content) == expected
