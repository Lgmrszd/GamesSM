import os
import sys
import json
import importlib.util


PLUGINS_DIR = "Plugins"


class Plugin(object):
    def __init__(self, name, dirname, description=None, enabled=False):
        self.name = name
        self.dirname = dirname
        self.description = description
        self.enabled = enabled

    def __str__(self):
        return "Plugin(name=\"{}\", dirname=\"{}\", description=\"{}\", enabled={})"\
            .format(self.name, self.dirname, self.description, self.enabled)


def get_plugin_info(path):
    if not os.path.isdir(item_path):
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


def save_config(conf):
    config_path = os.path.join(PLUGINS_DIR, "plugins.json")
    with open(config_path, "w") as f:
        json.dump(conf, f, indent=2)


def read_config():
    config_path = os.path.join(PLUGINS_DIR, "plugins.json")
    if os.path.exists(os.path.join(PLUGINS_DIR, "plugins.json")):
        try:
            with open(config_path, "r") as f:
                conf = json.load(f)
        except json.JSONDecodeError:
            conf = {"plugins": {}}
            save_config(conf)
        return conf
    else:
        conf = {"plugins": {}}
        save_config(conf)
        return conf


config = read_config()

plugins_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
plugins_dir = os.path.join(plugins_dir, PLUGINS_DIR)

if not os.path.exists(plugins_dir):
    os.makedirs(plugins_dir)

plugins = []

for item in os.listdir(plugins_dir):
    item_path = os.path.join(plugins_dir, item)
    plugin_info = get_plugin_info(item_path)
    if plugin_info:
        plugin_info["dirname"] = item
        plugin = Plugin(plugin_info["name"], plugin_info["dirname"], plugin_info.get("description"))
        plugins.append(plugin)
    del plugin_info


for plugin in plugins:
    print(plugin.dirname)
    if plugin.dirname in config["plugins"].keys():
        config["plugins"][plugin.dirname]["enabled"] = config["plugins"][plugin.dirname].get("enabled", False)
        plugin.enabled = config["plugins"][plugin.dirname]["enabled"]
    else:
        config["plugins"][plugin.dirname] = {"enabled": False}

save_config(config)


# print(plugins_dirs)
# # m = importlib.import_module(os.path.join(plugins_dir, plugins_dirs[0], "main"))
# module_spec = importlib.util.spec_from_file_location("main", os.path.join(plugins_dir, plugins_dirs[0], "main.py"))
# module = importlib.util.module_from_spec(module_spec)
# module_spec.loader.exec_module(module)
# module.main()
# print(module_spec)
