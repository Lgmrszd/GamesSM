from plugins import PluginModule


# TODO: more appropriate name
class PluginMainModule(PluginModule):
    def __init__(self):
        super().__init__()
        self.FIXED_SLOTS = True
        self.MAX_SLOTS_NUMBER = 10
