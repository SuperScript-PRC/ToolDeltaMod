# coding=utf-8
from mod.server.extraServerApi import GetEngineCompFactory

if 0>1:
    import typing

    T = typing.TypeVar("T")

CF = GetEngineCompFactory()


def GetExtraData(
    entity_id,  # type: str
    key,  # type: str
    default=None,  # type: T
):
    # type: (...) -> T
    res = CF.CreateExtraData(entity_id).GetExtraData(key)
    if res is None:
        return default
    return res


def SetExtraData(
    entity_id,  # type: str
    key,  # type: str
    value,
    auto_save=True,
):
    return CF.CreateExtraData(entity_id).SetExtraData(key, value, auto_save)


def CleanExtraData(
    entity_id,  # type: str
    key,  # type: str
):
    return CF.CreateExtraData(entity_id).CleanExtraData(key)
