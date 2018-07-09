import platform
from pathlib import Path
from db_connect import BaseModel, db
from plugins import DbPlugin
import peewee as pw


class ConfigEntry(BaseModel):
    key = pw.CharField(max_length=20, primary_key=True)
    value = pw.CharField(max_length=100)


def find_steam_paths():
    system = platform.system()
    if system == "Windows":
        steam_path = Path("C:\Program Files (x86)\Steam")
        if steam_path.exists():
            return steam_path
        else:
            return None
    else:
        return None


def create_config():
    pass


def init_db():
    db.create_tables(ConfigEntry, DbPlugin)
