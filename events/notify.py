# coding=utf-8
from ..internal import GetClient, GetServer
from .basic import BaseEvent, CustomC2SEvent, CustomS2CEvent

if 0 > 1:  # noqa: PLR0133
    import typing

    ET = typing.TypeVar("ET", bound="BaseEvent")


def NotifyToServer(event):
    # type: (CustomC2SEvent) -> None
    GetClient().NotifyToServer(event.name, event.marshal())


def NotifyToClient(targetId, event):
    # type: (str, CustomS2CEvent) -> None
    GetServer().NotifyToClient(targetId, event.name, event.marshal())


def NotifyToClients(targetIds, event):
    # type: (list[str], CustomS2CEvent) -> None
    GetServer().NotifyToMultiClients(targetIds, event.name, event.marshal())


def NotifyToAll(event):
    # type: (CustomS2CEvent) -> None
    GetServer().BroadcastToAllClient(event.name, event.marshal())


def ServerBroadcast(event):
    # type: (ET) -> ET
    event_dct = event.marshal()
    GetServer().BroadcastEvent(event.name, event_dct)
    return event.unmarshal(event_dct)


def ClientBroadcast(event):
    # type: (ET) -> ET
    event_dct = event.marshal()
    GetClient().BroadcastEvent(event.name, event_dct)
    return event.unmarshal(event_dct)
