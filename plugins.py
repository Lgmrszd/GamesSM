import os
import sys
import json
import importlib.util
from models import Plugin

PLUGINS_DIR = "Plugins"
_plugins = []



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
    plugins_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    plugins_dir = os.path.join(plugins_dir, PLUGINS_DIR)

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
    # Get list of existing plugins located in directories
    existing_plugins = get_plugins_info()
    # Get iterable (peewee select) of known plugins (stored in db)
    known_plugins = Plugin.select()
    known_plugins_names = []

    for known_plugin in known_plugins:
        # Fill up list of known plugins names
        known_plugins_names.append(known_plugin.name)
        # Check if directory of known plugin exists and mark as broken if it's not
        if known_plugin.name not in existing_plugins.keys():
            known_plugin.broken = True
        # store plugin
        _plugins.append(known_plugin)

    for ex_pl_name in existing_plugins.keys():
        # Check if new plugin found and store it if it is
        if ex_pl_name not in known_plugins_names:
            new_plugin = Plugin.create(
                name=existing_plugins[ex_pl_name]["name"],
                description=existing_plugins[ex_pl_name]["description"]
            )
            # store plugin
            _plugins.append(new_plugin)


# print(plugins_dirs)
# # m = importlib.import_module(os.path.join(plugins_dir, plugins_dirs[0], "main"))
# module_spec = importlib.util.spec_from_file_location("main", os.path.join(plugins_dir, plugins_dirs[0], "main.py"))
# module = importlib.util.module_from_spec(module_spec)
# module_spec.loader.exec_module(module)
# module.main()
# print(module_spec)
