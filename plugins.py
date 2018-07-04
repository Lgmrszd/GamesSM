import os
import sys
import json
import importlib.util
from db_connect import BaseModel, MemoryBaseModel
import peewee as pw

PLUGINS_DIR = "Plugins"

plugins_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
plugins_dir = os.path.join(plugins_dir, PLUGINS_DIR)

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


class PluginModule(object):
    def __init__(self):
        self.FIXED_SLOTS = True
        self.MAX_SLOTS_NUMBER = 0


def get_plugin_info(path):
    if not os.path.isdir(path):
        return None
    try:
        with open(os.path.join(path, "info.json"), "r") as f:
            info = json.load(f)
            if "name" in info.keys():
                return info
            else:
                return None
    except Exception as ex:
        print("ERROR:", ex)
        return None


def get_plugins_info():
    if not os.path.exists(plugins_dir):
        os.makedirs(plugins_dir)

    plugins_info = {}

    for item in os.listdir(plugins_dir):
        item_path = os.path.join(plugins_dir, item)
        plugin_info = get_plugin_info(item_path)
        if plugin_info and plugin_info["name"] == item:
            plugins_info[item] = plugin_info

    return plugins_info


def load_plugins():
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
                modules[plugin.name] = module.PluginMainModule()
            except Exception as ex:
                print(ex)


def import_plugin_module(name):
    module_spec = importlib.util.spec_from_file_location("main", os.path.join(plugins_dir, name, "main.py"))
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def get_plugins_list():
    return list(Plugin.select())


def get_enabled_plugins_list():
    return list(Plugin.select().where(Plugin.enabled == True))

# print(plugins_dirs)
# module.main()
# print(module_spec)
