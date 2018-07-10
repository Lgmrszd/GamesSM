import sys
import json
import importlib.util
from pathlib import Path
from db_connect import BaseModel, MemoryBaseModel
import peewee as pw

PLUGINS_DIR = "Plugins"

plugins_path = Path(sys.argv[0]).resolve()
plugins_path = plugins_path.parent.joinpath(Path(PLUGINS_DIR))
plugins_path = Path(plugins_path)

modules = {}


# Plugin class to store in database
class DbPlugin(BaseModel):
    name = pw.CharField(max_length=50, primary_key=True)
    enabled = pw.BooleanField(default=False)


# Plugin class to work while app running
class Plugin(MemoryBaseModel):
    name = pw.CharField(max_length=50, primary_key=True)
    description = pw.CharField()
    enabled = pw.BooleanField(default=False)
    broken = pw.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Save plugin preferences to local db if it's new plugin
        self.db_plugin, created = DbPlugin.get_or_create(name=self.name)
        if kwargs.get("broken", False):
            self.db_plugin.enabled = False

        if not created:
            self.enabled = self.db_plugin.enabled
            self.save()

    def get_module(self):
        return modules.get(self.name)

    def save(self, force_insert=False, only=None):
        super().save(force_insert=force_insert, only=only)
        # Save plugin preferences to local db
        self.db_plugin.enabled = self.enabled
        self.db_plugin.save()

    def set_enabled(self):
        self.enabled = True
        self.save()

    def set_disabled(self):
        self.enabled = False
        self.save()


def get_plugin_info(pl_path: Path):
    if not pl_path.is_dir():
        return None
    info_path = pl_path.joinpath("info.json")
    if not info_path.is_file():
        return None
    try:
        with info_path.open() as f:
            info = json.load(f)
            if isinstance(info, dict) and info.get("name") == pl_path.name:
                return info
            else:
                return None
    except Exception as ex:
        print("ERROR:", ex)
        return None


def get_plugins_info():
    if not plugins_path.exists():
        plugins_path.mkdir()
    plugins_info = {}
    for pl_path in plugins_path.iterdir():
        pl_info = get_plugin_info(pl_path)
        if pl_info:
            plugins_info[pl_info["name"]] = pl_info

    return plugins_info


def load_plugins():
    # Drop table if restart
    Plugin.drop_table()
    # Create plugins table
    Plugin.create_table()
    # Get list of existing plugins located in directories
    existing_plugins = get_plugins_info()
    # Add existing plugins to memory
    for ex_pl_name in existing_plugins.keys():
        ex_pl = existing_plugins[ex_pl_name]
        Plugin.create(
            name=ex_pl_name,
            description=ex_pl["description"]
        )
    # Find broken plugins
    db_pl_names = set([i.name for i in DbPlugin.select(DbPlugin.name)])
    missed_pl_names = list(db_pl_names - set(existing_plugins.keys()))
    for missed_pl_name in missed_pl_names:
        Plugin.create(
            name=missed_pl_name,
            description="",
            enabled=False,
            broken=True
        )


def import_plugins():
    for plugin in Plugin.select():
        if plugin.enabled:
            module = import_plugin_module(plugin.name)
            try:
                modules[plugin.name] = module.PluginModule()
                print(modules[plugin.name])
            except Exception as ex:
                print(ex)
                plugin.enabled = False
                plugin.save()


def import_plugin_module(name):
    module_spec = importlib.util.spec_from_file_location("main", plugins_path.joinpath(name, "main.py"))
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def get_plugins_list():
    return list(Plugin.select())


def get_enabled_plugins_list():
    return list(Plugin.select().where(Plugin.enabled == True))
