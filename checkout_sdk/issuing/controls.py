from enum import Enum


class ControlType(str, Enum):
    VELOCITY_LIMIT = 'velocity_limit'
    MCC_LIMIT = 'mcc_limit'
    MID_LIMIT = 'mid_limit'


class VelocityWindowType(str, Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    ALL_TIME = 'all_time'


class MccLimitType(str, Enum):
    ALLOW = 'allow'
    BLOCK = 'block'


class MidLimitType(str, Enum):
    ALLOW = 'allow'
    BLOCK = 'block'


class FailIfType(str, Enum):
    ALL_FAIL = 'all_fail'
    ANY_FAIL = 'any_fail'


class VelocityWindow:
    type: VelocityWindowType


class VelocityLimit:
    amount_limit: int
    velocity_window: VelocityWindow
    mcc_list: list  # str
    mid_list: list  # str


class MccLimit:
    type: MccLimitType
    mcc_list: list  # str


class MidLimit:
    type: MidLimitType
    mid_list: list  # str


class CardControlRequest:
    description: str
    control_type: ControlType
    target_id: str

    def __init__(self, control_type: ControlType):
        self.control_type = control_type


class VelocityControlRequest(CardControlRequest):
    velocity_limit: VelocityLimit

    def __init__(self):
        super().__init__(ControlType.VELOCITY_LIMIT)


class MccControlRequest(CardControlRequest):
    mcc_limit: MccLimit

    def __init__(self):
        super().__init__(ControlType.MCC_LIMIT)


class CardControlsQuery:
    target_id: str


class UpdateCardControlRequest:
    description: str
    velocity_limit: VelocityLimit
    mcc_limit: MccLimit


class ControlGroupControl:
    control_type: ControlType
    description: str

    def __init__(self, control_type: ControlType):
        self.control_type = control_type


class MccControlGroupControl(ControlGroupControl):
    mcc_limit: MccLimit

    def __init__(self):
        super().__init__(ControlType.MCC_LIMIT)


class MidControlGroupControl(ControlGroupControl):
    mid_limit: MidLimit

    def __init__(self):
        super().__init__(ControlType.MID_LIMIT)


class VelocityControlGroupControl(ControlGroupControl):
    velocity_limit: VelocityLimit

    def __init__(self):
        super().__init__(ControlType.VELOCITY_LIMIT)


class CreateControlGroupRequest:
    target_id: str
    fail_if: FailIfType
    controls: list  # ControlGroupControl
    description: str


class ControlGroupQueryTarget:
    target_id: str


class ControlProfileRequest:
    name: str
