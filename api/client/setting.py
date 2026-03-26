# coding=utf-8
from mod.client.extraClientApi import GetEngineCompFactory, GetLevelId, GetMinecraftEnum
from ..common.cacher import MethodCacher

CF = GetEngineCompFactory()


RegisterCustomKeyMapping = MethodCacher(
    lambda: CF.CreatePlayerView(GetLevelId()).RegisterCustomKeyMapping
)
RegisterCustomGamepadMapping = MethodCacher(
    lambda: CF.CreatePlayerView(GetLevelId()).RegisterCustomGamepadMapping
)
GetKeyMappings = MethodCacher(lambda: CF.CreatePlayerView(GetLevelId()).GetKeyMappings)
GetGamepadKeyMappings = MethodCacher(
    lambda: CF.CreatePlayerView(GetLevelId()).GetGamepadKeyMappings
)
GetKeyboardEnum = MethodCacher(lambda: GetMinecraftEnum().KeyBoardType)
GetGamepadKeyEnum = MethodCacher(lambda: GetMinecraftEnum().GamepadKeyType)

__all__ = [
    "RegisterCustomKeyMapping",
    "RegisterCustomGamepadMapping",
    "GetKeyMappings",
    "GetKeyboardEnum",
    "GetGamepadKeyEnum",
    "GetGamepadKeyMappings",
]
