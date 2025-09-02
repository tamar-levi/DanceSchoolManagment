import os
from pathlib import Path

class ManageJSON:
    @staticmethod
    def get_appdata_path():
        base = Path(os.getenv("LOCALAPPDATA"))
        app_folder = base / "DanceSchool"
        app_folder.mkdir(parents=True, exist_ok=True)
        return app_folder