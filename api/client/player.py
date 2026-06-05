# coding=utf-8
from mod.client.extraClientApi import (
    GetEngineCompFactory,
    GetLevelId,
    GetPlayerList,
    GetLocalPlayerId,
    GetMinecraftEnum,
)
from ...define import Item

CF = GetEngineCompFactory()


def GetNameById(player_id):
    # type: (str) -> str
    return CF.CreateName(player_id).GetName()


def GetPlayerDimensionId():
    # type: () -> int
    return CF.CreateGame(GetLocalPlayerId()).GetCurrentDimension()


def GetAllPlayers():
    # type: () -> list[str]
    return GetPlayerList()


def GetPlayerMainhandItem(player_id):
    # type: (str) -> Item | None
    it = CF.CreateItem(player_id).GetPlayerItem(
        GetMinecraftEnum().ItemPosType.CARRIED, 0, True
    )
    if it is None:
        return None
    return Item.from_dict(it)


def GetLocalPlayerMainhandItem():
    # type: () -> Item | None
    it = CF.CreateItem(GetLocalPlayerId()).GetPlayerItem(
        GetMinecraftEnum().ItemPosType.CARRIED, 0, True
    )
    if it is None:
        return None
    return Item.from_dict(it)


def GetLocalPlayerHotbarAndInvItems(get_user_data=False):
    return [
        (Item.from_dict(it) if it is not None else None)
        for it in CF.CreateItem(GetLocalPlayerId()).GetPlayerAllItems(
            GetMinecraftEnum().ItemPosType.INVENTORY, get_user_data
        )
    ]


def GetLocalPlayerTotalExp():
    # type: () -> int
    return int(CF.CreateGame(GetLevelId()).GetPlayerTotalExp(GetLocalPlayerId()))


def GetLevelByTotalExp(total_exp):
    # type: (int) -> int
    if total_exp <= 0:
        return 0
    level = 0
    exp_left = int(total_exp)
    while True:
        if level <= 15:
            need = 2 * level + 7
        elif level <= 30:
            need = 5 * level - 38
        else:
            need = 9 * level - 158
        if exp_left < need:
            return level
        exp_left -= need
        level += 1


def GetLocalPlayerLevelByExp():
    # type: () -> int
    return GetLevelByTotalExp(GetLocalPlayerTotalExp())


__all__ = [
    "GetNameById",
    "GetPlayerDimensionId",
    "GetAllPlayers",
    "GetLocalPlayerId",
    "GetPlayerMainhandItem",
    "GetLocalPlayerMainhandItem",
    "GetLocalPlayerHotbarAndInvItems",
    "GetLocalPlayerTotalExp",
    "GetLevelByTotalExp",
    "GetLocalPlayerLevelByExp",
]
