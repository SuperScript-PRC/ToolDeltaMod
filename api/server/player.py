# coding=utf-8
#
from mod.server.extraServerApi import (
    GetEngineCompFactory,
    GetMinecraftEnum,
    GetPlayerList,
    GetLevelId,
)
from ...define.item import Item

CF = GetEngineCompFactory()


def GetNameById(player_id):
    # type: (str) -> str
    return CF.CreateName(player_id).GetName()


def GetPlayerDimensionId(player_id):
    # type: (str) -> int
    return CF.CreateDimension(player_id).GetEntityDimensionId()


def SpawnItemToPlayerCarried(player_id, item):
    # type: (str, Item) -> bool
    return CF.CreateItem(player_id).SpawnItemToPlayerCarried(item.marshal(), player_id)


def GiveItem(player_id, item):
    # type: (str, Item) -> bool
    return CF.CreateItem(player_id).SpawnItemToPlayerInv(item.marshal(), player_id)


def GetAllPlayers():
    # type: () -> list[str]
    return GetPlayerList()


def GetPlayersInDim(dim):
    # type: (int) -> list[str]
    return [
        player_id
        for player_id in GetAllPlayers()
        if GetPlayerDimensionId(player_id) == dim
    ]


def GetPlayerMainhandItem(player_id):
    # type: (str) -> Item | None
    it = CF.CreateItem(player_id).GetPlayerItem(
        GetMinecraftEnum().ItemPosType.CARRIED, 0, True
    )
    if it is None:
        return None
    return Item.from_dict(it)


def GetSelectedSlot(player_id):
    # type: (str) -> int
    return CF.CreateItem(player_id).GetSelectSlotId()


def GetPlayerItem(player_id, pos_type, slot, get_userdata=False):
    # type: (str, int, int, bool) -> Item | None
    res = CF.CreateItem(player_id).GetPlayerItem(pos_type, slot, get_userdata)
    return Item.from_dict(res) if res is not None else None


def GetPlayerGameType(player_id):
    # type: (str) -> int
    return CF.CreateGame(GetLevelId()).GetPlayerGameType(player_id)


def GetAllInventoryItems(player_id, get_userdata=False):
    # type: (str, bool) -> dict[int, Item]
    """获取玩家背包所有物品，返回 {槽位: Item} 字典，仅包含非空槽位"""
    items = {}
    raw_items = CF.CreateItem(player_id).GetPlayerAllItems(
        GetMinecraftEnum().ItemPosType.INVENTORY, get_userdata
    )
    for slot, res in enumerate(raw_items):
        if res is not None:
            items[slot] = Item.from_dict(res)
    return items


def GetArmorSlotItems(player_id, get_userdata=True):
    # type: (str, bool) -> dict[int, Item]
    """获取玩家装备槽位物品，返回 {槽位: Item} 字典，仅包含非空槽位"""
    items = {}
    raw_items = CF.CreateItem(player_id).GetPlayerAllItems(
        GetMinecraftEnum().ItemPosType.ARMOR, get_userdata
    )
    for slot, res in enumerate(raw_items):
        if res is not None:
            items[slot] = Item.from_dict(res)
    return items


def PlayerDestroyBlock(player_id, pos, particle, send_inv_update=True):
    # type: (str, tuple[int, int, int], bool, bool) -> bool
    # 网易对此方法拼写错误
    return CF.CreateBlockInfo(player_id).PlayerDestoryBlock(
        pos, particle, send_inv_update
    )


def SetInventorySlotItemCount(player_id, slot_id, count):
    # type: (str, int, int) -> bool
    return CF.CreateItem(player_id).SetInvItemNum(slot_id, count)


def SetPlayerAllItems(player_id, items):
    # type: (str, dict[tuple[int, int], Item]) -> None
    CF.CreateItem(player_id).SetPlayerAllItems({
        k: v.marshal() for k, v in items.items()
    })


def IsOP(player_id):
    # type: (str) -> bool
    return CF.CreatePlayer(player_id).GetPlayerAbilities().get("op", False)


def IsSneaking(player_id):
    # type: (str) -> bool
    return CF.CreatePlayer(player_id).isSneaking()


def PlayerUseItemToPos(player_id, pos, pos_type, slot=0, facing=1):
    # type: (str, tuple[int, int, int], int, int, int) -> bool
    return CF.CreateBlockInfo(player_id).PlayerUseItemToPos(pos, pos_type, slot, facing)


__all__ = [
    "GetAllPlayers",
    "GetNameById",
    "GetArmorSlotItems",
    "GetPlayerDimensionId",
    "GetPlayerMainhandItem",
    "GetSelectedSlot",
    "GetPlayersInDim",
    "GetPlayerItem",
    "GetAllInventoryItems",
    "GetPlayerGameType",
    "IsOP",
    "IsSneaking",
    "PlayerUseItemToPos",
    "PlayerDestroyBlock",
    "SetInventorySlotItemCount",
    "SpawnItemToPlayerCarried",
    "SetPlayerAllItems",
]
