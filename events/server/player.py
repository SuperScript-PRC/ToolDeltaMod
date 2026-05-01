# coding=utf-8
from ...define.item import Item
from ..basic import ServerEvent


class AddServerPlayerEvent(ServerEvent):
    name = "AddServerPlayerEvent"

    def __init__(
        self,
        id,  # type: str
        isTransfer,  # type: bool
        isReconnect,  # type: bool
        isPeUser,  # type: bool
        transferParam,  # type: str
        uid,  # type: int
        proxyId,  # type: int
    ):
        self.id = id
        """ 玩家id """
        self.isTransfer = isTransfer
        """ 是否是切服时进入服务器，仅用于Apollo。如果是True，则表示切服时加入服务器，若是False，则表示登录进入网络游戏 """
        self.isReconnect = isReconnect
        """ 是否是断线重连，仅用于Apollo。如果是True，则表示本次登录是断线重连，若是False，则表示本次是正常登录或者转服 """
        self.isPeUser = isPeUser
        """ 是否从手机端登录，仅用于Apollo。如果是True，则表示本次登录是从手机端登录，若是False，则表示本次登录是从PC端登录 """
        self.transferParam = transferParam
        """ 切服传入参数，仅用于Apollo。调用【TransferToOtherServer】或【TransferToOtherServerById】传入的切服参数 """
        self.uid = uid
        """ 仅用于Apollo，玩家的netease uid，玩家的唯一标识 """
        self.proxyId = proxyId
        """ 仅用于Apollo，当前客户端连接的proxy服务器id """

    @classmethod
    def unmarshal(cls, data):
        return cls(
            id=data["id"],
            isTransfer=data.get("isTransfer", False),
            isReconnect=data.get("isReconnect", False),
            isPeUser=data.get("isPeUser", False),
            transferParam=data.get("transferParam", ""),
            uid=data.get("uid", 0),
            proxyId=data.get("proxyId", 0),
        )

    def marshal(self):
        # type: () -> dict
        return {
            "id": self.id,
            "isTransfer": self.isTransfer,
            "isReconnect": self.isReconnect,
            "isPeUser": self.isPeUser,
            "transferParam": self.transferParam,
            "uid": self.uid,
            "proxyId": self.proxyId,
        }


class PlayerAttackEntityEvent(ServerEvent):
    name = "PlayerAttackEntityEvent"

    def __init__(
        self,
        playerId,  # type: str
        victimId,  # type: str
        damage,  # type: float
        isValid,  # type: int
        isKnockBack,  # type: bool
        isCrit,  # type: bool
        _orig,  # type: dict
    ):
        self.playerId = playerId
        """ 玩家id """
        self.victimId = victimId
        """ 受击者id """
        self.damage = damage
        """ 伤害值：引擎传过来的值是0 允许脚本层修改为其他数 """
        self.isValid = isValid
        """ 脚本是否设置伤害值：1表示是；0 表示否 """
        self.isKnockBack = isKnockBack
        """ 是否支持击退效果，默认支持，当不支持时将屏蔽武器击退附魔效果 """
        self.isCrit = isCrit
        """ 本次攻击是否产生暴击,不支持修改 """
        self._orig = _orig
        """ 原始事件数据 """

    @classmethod
    def unmarshal(cls, data):
        return cls(
            playerId=data["playerId"],
            victimId=data["victimId"],
            damage=data["damage"],
            isValid=data["isValid"],
            isKnockBack=data["isKnockBack"],
            isCrit=data["isCrit"],
            _orig=data,
        )

    def marshal(self):
        # type: () -> dict
        return {
            "playerId": self.playerId,
            "victimId": self.victimId,
            "damage": self.damage,
            "isValid": self.isValid,
            "isKnockBack": self.isKnockBack,
            "isCrit": self.isCrit,
        }

    def cancel(self):
        # type: () -> None
        "取消该次攻击"
        self._orig["cancel"] = True

    def SetDamage(self, damage):
        # type: (int) -> None
        "设置伤害"
        self.damage = self._orig["damage"] = damage

    def DisableKnockBack(self):
        # type: () -> None
        "取消击退效果"
        self.isKnockBack = self._orig["isKnockBack"] = False


class ActuallyHurtServerEvent(ServerEvent):
    name = "ActuallyHurtServerEvent"

    def __init__(
        self,
        srcId,  # type: str
        projectileId,  # type: str
        entityId,  # type: str
        damage,  # type: float
        invulnerableTime,  # type: int
        lastHurt,  # type: float
        cause,  # type: str
        customTag,  # type: str
        _orig,  # type: dict
    ):
        self.srcId = srcId
        """ 伤害源id """
        self.projectileId = projectileId
        """ 投射物id """
        self.entityId = entityId
        """ 被伤害id """
        self.damage = damage
        """ 伤害值（被伤害吸收后的值），允许修改，设置为0则此次造成的伤害为0，若设置数值和原来一样则视为没有修改 """
        self.invulnerableTime = invulnerableTime
        """ 实体受击后，剩余的无懈可击帧数，在无懈可击时间内，damage和damage_f为超过上次伤害的部分 """
        self.lastHurt = lastHurt
        """ 实体上次受到的伤害 """
        self.cause = cause
        """ 伤害来源，详见Minecraft枚举值文档的ActorDamageCause """
        self.customTag = customTag
        """ 使用Hurt接口传入的自定义伤害类型 """
        self._orig = _orig
        """ 原始事件数据 """

    @classmethod
    def unmarshal(cls, data):
        return cls(
            srcId=data["srcId"],
            projectileId=data["projectileId"],
            entityId=data["entityId"],
            damage=data["damage"],
            invulnerableTime=data["invulnerableTime"],
            lastHurt=data["lastHurt"],
            cause=data["cause"],
            customTag=data["customTag"],
            _orig=data,
        )

    def marshal(self):
        # type: () -> dict
        return {
            "srcId": self.srcId,
            "projectileId": self.projectileId,
            "entityId": self.entityId,
            "damage": self.damage,
            "invulnerableTime": self.invulnerableTime,
            "lastHurt": self.lastHurt,
            "cause": self.cause,
            "customTag": self.customTag,
        }

    def modifyDamage(self, damage):
        # type: (float) -> None
        self._orig["damage"] = damage
        self.damage = damage


class PlayerHurtEvent(ServerEvent):
    name = "PlayerHurtEvent"

    def __init__(
        self,
        id,  # type: str
        attacker,  # type: str
        customTag,  # type: str
        cause,  # type: str
    ):
        self.id = id
        """ 受击玩家id """
        self.attacker = attacker
        """ 伤害来源实体id，若没有实体攻击，例如高空坠落，id为-1 """
        self.customTag = customTag
        """ 使用Hurt接口传入的自定义伤害类型 """
        self.cause = cause
        """ 伤害来源，详见Minecraft枚举值文档的ActorDamageCause """

    @classmethod
    def unmarshal(cls, data):
        return cls(
            id=data["id"],
            attacker=data["attacker"],
            customTag=data["customTag"],
            cause=data["cause"],
        )

    def marshal(self):
        # type: () -> dict
        return {
            "id": self.id,
            "attacker": self.attacker,
            "customTag": self.customTag,
            "cause": self.cause,
        }
