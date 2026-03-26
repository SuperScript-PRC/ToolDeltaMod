# coding=utf-8
from ...tooldelta.api.client import (
    RegisterGeneralKeyMapping as _reg,
    GetControlMode,
    GetControlModeEnum,
    GetKeyMappings,
    GetGamepadKeyMappings,
    GetKeyboardEnum,
    GetGamepadKeyEnum,
)


class Control:
    def __init__(self, category, name, default_key, default_gamepad):
        # type: (str, str, int, int) -> None
        _reg(category, name, default_key, default_gamepad)
        self.category = category
        self.name = name
        self._key_id = None
        self._gamepad_id = None
        self._ctrl_mode = None

    @property
    def key_id(self):
        if self._key_id is None:
            self._key_id = GetKeyMappings(self.name)
        return self._key_id

    @property
    def gamepad_id(self):
        if self._gamepad_id is None:
            self._gamepad_id = GetGamepadKeyMappings(self.name)
        return self._gamepad_id

    @property
    def key_str(self):
        from .ctrl_zhcn import KEYBOARD_STR_MAPPING

        return KEYBOARD_STR_MAPPING.get(self.key_id, "?")

    @property
    def gamepad_str(self):
        from .ctrl_zhcn import GAMEPAD_STR_MAPPING

        return GAMEPAD_STR_MAPPING.get(self.gamepad_id, "?")

    def get_general_str(self, with_prefix=False):
        CTRL = GetControlModeEnum()
        mode = GetControlMode()
        if mode == CTRL.Mouse:
            if with_prefix:
                return "键盘 " + self.key_str
            else:
                return self.key_str
        elif mode == CTRL.GamePad:
            if with_prefix:
                return "手柄 " + self.gamepad_str
            else:
                return self.gamepad_str
        else:
            return "未知按键"

    @staticmethod
    def KEY():
        return GetKeyboardEnum()

    @staticmethod
    def GAMEPAD():
        return GetGamepadKeyEnum()
