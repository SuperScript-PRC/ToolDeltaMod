# coding=utf-8
from mod.client.extraClientApi import GetEngineCompFactory, GetLevelId

CF = GetEngineCompFactory()

item_tags_pool = {}  # type: dict[str, set[str]]


def GetItemHoverName(itemName):
    # type: (str) -> str
    return CF.CreateItem(GetLevelId()).GetItemHoverName(itemName)


def GetItemFormattedHoverText(itemName):
    # type: (str) -> str
    return CF.CreateItem(GetLevelId()).GetItemFormattedHoverText(itemName)


def GetItemTags(item_id, aux_value=0):
    # type: (str, int) -> set[str]
    basic_info = item_tags_pool.get(item_id)
    if basic_info is not None:
        return basic_info
    tags_list = CF.CreateItem(GetLevelId()).GetItemTags(item_id, aux_value)
    if tags_list is None:
        raise ValueError("Item id invalid: " + item_id)
    tags = set(tags_list)
    item_tags_pool[item_id] = tags
    return tags


__all__ = [
    "GetItemHoverName",
    "GetItemFormattedHoverText",
    "GetItemTags",
]
