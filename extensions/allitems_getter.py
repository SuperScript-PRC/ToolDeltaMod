# coding=utf-8
from ..general import (
    ServerInitCallback,
    ClientInitCallback,
    ServerUninitCallback,
    ClientUninitCallback,
)
from ..internal import InClientEnv
from ..events.basic import CustomC2SEvent, CustomS2CEvent
from ..events.client import UiInitFinishedEvent
from ..events.server import DelServerPlayerEvent

allitems = set()  # type: set[str]
_items_by_tag_cache = {False: {}, True: {}}  # type: dict[bool, dict[str, set[str]]]
client_already_get_allitems = set()  # type: set[str]
items_getted_callback = []
game_loaded = False


class GetAllItemsRequest(CustomC2SEvent):
    name = "td:GetAllItemsRequest"

    def __init__(self, player_id=""):
        self.player_id = player_id

    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, data):
        return cls(data["__id__"])


class GetAllItemsResponse(CustomS2CEvent):
    name = "td:GetAllItemsResponse"

    def __init__(self, items=[], ok=True):
        # type: (list[str], bool) -> None
        self.items = items
        self.ok = ok

    def marshal(self):
        return {"i": self.items, "ok": self.ok}

    @classmethod
    def unmarshal(cls, data):
        return cls(
            items=data["i"],
            ok=data["ok"],
        )


@ServerInitCallback()
def onServerInited():
    _items_by_tag_cache[False].clear()
    from ..srv import CF, LEVEL_ID

    @DelServerPlayerEvent.Listen()
    def onDelPlayer(event):
        # type: (DelServerPlayerEvent) -> None
        client_already_get_allitems.discard(event.id)

    @GetAllItemsRequest.Listen()
    def onGetAllItems(event):
        # type: (GetAllItemsRequest) -> None
        player_id = event.player_id
        if player_id in client_already_get_allitems:
            GetAllItemsResponse(ok=False).send(player_id)
        else:
            items = CF.CreateItem(LEVEL_ID).GetLoadItems()
            # if len(items) < 100:
            #     print("[ERROR] ITEMS COUNT TOO SMALL", items)
            GetAllItemsResponse(items).send(player_id)


@ClientInitCallback()
def onClientReallyInited():
    _items_by_tag_cache[True].clear()

    @GetAllItemsResponse.Listen()
    def onGetResponse(event):
        # type: (GetAllItemsResponse) -> None
        global allitems
        if not event.ok:
            print("[ERROR] GetAllItemsResponse: Failed to get all items")
        else:
            print(
                "[INFO] GetAllItemsResponse: Got all items from server (%d)"
                % len(event.items)
            )
            loadAllItems(event.items)
            for cb in items_getted_callback:
                cb(allitems)

    def loadAllItems(_allitems):
        # type: (list[str]) -> None
        global allitems
        allitems = set(_allitems)

    @UiInitFinishedEvent.Listen()
    def onStartGame(event):
        global game_loaded
        if game_loaded:
            return
        game_loaded = True
        GetAllItemsRequest().send()


@ServerUninitCallback()
def _clear_server_tag_cache():
    _items_by_tag_cache[False].clear()


@ClientUninitCallback()
def _clear_client_tag_cache():
    _items_by_tag_cache[True].clear()


def GetAllItems():
    # type: () -> set[str]
    """
    客户端侧函数。获取已加载的所有物品 ID 的集合。

    Returns:
        set[str]: 所有物品 ID 的集合
    """
    return allitems


def GetItemsByTag(tag):
    # type: (str) -> set[str]
    """双端函数。通过原生接口获取物品标签与方块标签下的 ID 并集。"""
    is_client = InClientEnv()
    cache = _items_by_tag_cache[is_client]
    items = cache.get(tag)
    if items is not None:
        return items

    if is_client:
        from ..cli import CF, LEVEL_ID
    else:
        from ..srv import CF, LEVEL_ID

    items = set(
        entry["itemName"]
        for entry in CF.CreateItem(LEVEL_ID).LookupItemsByItemTag(tag)
    )
    items.update(
        entry["blockName"]
        for entry in CF.CreateBlock(LEVEL_ID).LookupBlocksByBlockTag(tag)
    )
    # 初始化早期查询可能为空，后续仍需向引擎查询。
    if items:
        cache[tag] = items
    return items


def AddItemGettedCallback(callback):
    "ClientSide function"
    items_getted_callback.append(callback)
