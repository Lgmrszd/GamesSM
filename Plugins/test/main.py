from plugins_connector import PluginModuleSample


# TODO: more appropriate name
class PluginModule(PluginModuleSample):
    def __init__(self):
        super().__init__()
        self.FIXED_SLOTS = True
        self.MAX_SLOTS_NUMBER = 10
