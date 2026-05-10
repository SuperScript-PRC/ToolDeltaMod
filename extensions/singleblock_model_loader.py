# coding=utf-8
from mod_log import logger
from ..api.client import (
    CombineBlockPaletteToGeometry,
    NewSingleBlockPalette,
    CreateClientEntity,
    DestroyClientEntity,
    SetActorBlockGeometryScale,
    AddActorBlockGeometry,
    DeleteActorBlockGeometry,
    SetEntityShadowShow,
    SetPosForClientEntity,
)
from ..api.common import ExecLater

if 0:
    import typing


class GeometryModel(object):
    def __init__(self, entity_id, x, y, z):
        # type: (str, float, float, float) -> None
        self.entity_id = entity_id
        self.geo_id = None
        self._last_block_id = None
        self._last_block_aux = None
        self._last_scale = None
        self.x = x
        self.y = y
        self.z = z

    def SetBlockPaletteModel(self, block_palette, geo_id, scale=None):
        # type: (typing.Any, str, tuple[float, float, float] | None) -> bool
        if self.geo_id is not None:
            res = self.RemoveGeometry()
            if not res:
                logger.warning("last geometry remove failed")
        self.geo_id = CombineBlockPaletteToGeometry(block_palette, geo_id)
        if self.geo_id is None:
            raise Exception("Failed to create geometry: " + self.geo_id)
        final_res = AddActorBlockGeometry(self.entity_id, self.geo_id)
        if scale is not None:
            res = SetActorBlockGeometryScale(self.entity_id, self.geo_id, scale)
            if not res:
                logger.warning("set geometry scale failed")
                return False
        return final_res

    def SetBlockModel(self, block_name, aux, scale=None, offset=None):
        # type: (str, int, tuple[float, float, float] | None, tuple[float, float, float] | None) -> bool
        ok = True
        if offset is not None:
            offset_x, offset_y, offset_z = offset
            ok = ok and SetPosForClientEntity(
                self.entity_id,
                (self.x + offset_x, self.y + offset_y, self.z + offset_z),
            )
        if (
            block_name != self._last_block_id
            or aux != self._last_block_aux
            or scale != self._last_scale
        ):
            if self.geo_id is not None:
                res = self.RemoveGeometry()
                if not res:
                    logger.warning("[SkyblueTech] last geometry remove failed")
            pal = NewSingleBlockPalette(block_name, aux)
            self.geo_id = block_name + ":" + str(aux)
            self.geo_id = CombineBlockPaletteToGeometry(pal, self.geo_id)
            if self.geo_id is None:
                raise Exception("Failed to create geometry: " + self.geo_id)
            final_res = AddActorBlockGeometry(self.entity_id, self.geo_id)
            if final_res:
                self._last_block_id = block_name
                self._last_block_aux = aux
            ok = ok and final_res
        if scale is not None and scale != self._last_scale and self.geo_id is not None:
            res = SetActorBlockGeometryScale(self.entity_id, self.geo_id, scale)
            if not res:
                logger.warning("[SkyblueTech] Set geometry scale failed")
                return False
            else:
                self._last_scale = scale
            ok = ok and res
        return ok

    def RemoveGeometry(self):
        if self.geo_id is not None:
            geo_id = self.geo_id
            self.geo_id = None
            return DeleteActorBlockGeometry(self.entity_id, geo_id)
        else:
            logger.warning("[SkyblueTech] No geometry to remove")
            return False

    def Destroy(self):
        DestroyClientEntity(self.entity_id)


def CreateSingleBlockModelEntity(
    pos, block_name, aux=0, entity_name="skybluetech:model_entity"
):
    # type: (tuple[float, float, float], str, int, str) -> tuple[GeometryModel, bool]
    entity_id = CreateClientEntity(entity_name, pos, (0, 0))
    if entity_id is None:
        raise Exception("Failed to create entity: " + entity_name)
    SetEntityShadowShow(entity_id, False)
    model = GeometryModel(entity_id, *pos)
    return model, model.SetBlockModel(block_name, aux)


def CreateBlankModel(pos, entity_name="skybluetech:model_entity"):
    # type: (tuple[float, float, float], str) -> GeometryModel
    x, y, z = pos
    entity_id = CreateClientEntity(entity_name, (x + 0.5, y, z + 0.5), (0, 180))
    if entity_id is None:
        raise Exception("Failed to create entity: " + entity_name)
    SetEntityShadowShow(entity_id, False)
    model = GeometryModel(entity_id, x + 0.5, y, z + 0.5)
    return model


def CreateTempSingleBlockModelEntity(
    pos, block_name, aux=0, entity_name="skybluetech:model_entity", delay=8
):
    # type: (tuple[float, float, float], str, int, str, int) -> None
    x, y, z = pos
    model, _ = CreateSingleBlockModelEntity(
        (x + 0.5, y, z + 0.5), block_name, aux, entity_name
    )
    ExecLater(delay, lambda: model.Destroy())


def CreateTempBlockGeometryModelEntity(
    pos,
    block_palette,
    temp_id="temp_block_geometry",
    entity_name="skybluetech:model_entity",
    delay=8,
):
    # type: (tuple[float, float, float], typing.Any, str, str, int) -> None
    x, y, z = pos
    model = CreateBlankModel((x + 0.5, y, z + 0.5), entity_name)
    model.SetBlockPaletteModel(block_palette, temp_id)
    ExecLater(delay, lambda: model.Destroy())
