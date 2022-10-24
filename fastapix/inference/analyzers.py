import re


class Analyzer:
    def match(self, content: str) -> bool:
        raise NotImplementedError


class SettingsAnalyzer(Analyzer):
    def match(self, content: str) -> bool:
        if re.search(r"class .+\(BaseSettings\):", content):
            return True
        return False
