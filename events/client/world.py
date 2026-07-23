# coding=utf-8

from ..basic import ClientEvent


class OnScriptTickClient(ClientEvent):
    name = "OnScriptTickClient"

    def __init__(self):
        pass

    @classmethod
    def unmarshal(cls, data=None):
        return cls()

    def marshal(self):
        return {}


class GameRenderTickEvent(ClientEvent):
    name = "GameRenderTickEvent"

    def __init__(self):
        pass

    @classmethod
    def unmarshal(cls, data=None):
        return cls()

    def marshal(self):
        return {}

class LoadClientAddonScriptsAfter(ClientEvent):
    name = "LoadClientAddonScriptsAfter"

    def __init__(self):
        pass

    @classmethod
    def unmarshal(cls, _):
        return cls()

    def marshal(self):
        return {}
