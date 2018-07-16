import platform
from pathlib import Path
from db_connect import BaseModel, db
from plugins import DbPlugin
import peewee as pw


class ConfigEntry(BaseModel):
    key = pw.CharField(max_length=20, primary_key=True)
    value = pw.CharField(max_length=100)


def find_steamapps_paths():
    paths = []
    system = platform.system()
    if system == "Windows":
        steam_path = Path("C:\Program Files (x86)\Steam\steamapps")
        if steam_path.exists() and steam_path.is_dir():
            paths.append(steam_path)
    elif system == "Linux":
        home = Path.home()
        steam_path = home.joinpath(Path(".local/share/Steam/steamapps")).resolve()
        if steam_path.exists() and steam_path.is_dir():
            paths.append(steam_path)
    return paths


def create_config():
    pass


def init_db():
    db.create_tables(ConfigEntry, DbPlugin)
