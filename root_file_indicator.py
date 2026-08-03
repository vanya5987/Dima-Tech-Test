import os

class RootPathIndicator:
    @staticmethod
    def get_root_path() -> str:
        return os.path.join(os.path.dirname(__file__))