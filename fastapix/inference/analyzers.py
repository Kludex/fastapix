import re


class Analyzer:
    def match(self, content: str) -> bool:
        raise NotImplementedError  # pragma: no cover


class SettingsAnalyzer(Analyzer):
    def match(self, content: str) -> bool:
        if re.search(r"class .+\(BaseSettings\):", content):
            return True
        return False


class ApplicationAnalyzer(Analyzer):
    def match(self, content: str) -> bool:
        """Check if the content contains a FastAPI instance.

        This is a very naive implementation, and it's expected to fail.
        """
        regex = "|".join([r"=\s*FastAPI\(\)", r"return FastAPI\("])
        if re.search(regex, content):
            return True
        return False
