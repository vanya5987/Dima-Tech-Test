from typing import Any, Dict
import json

class JsonAPI:
    @staticmethod
    def read_json_file(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (OSError, json.JSONDecodeError) as ex:
            raise RuntimeError(f"Read file error {file_path}: {ex}") from ex