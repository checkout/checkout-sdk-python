from enum import Enum


class WorkflowConditionType(str, Enum):
    EVENT = 'event'
    ENTITY = 'entity'
    PROCESSING_CHANNEL = 'processing_channel'


class WorkflowActionType(str, Enum):
    WEBHOOK = 'webhook'


class WorkflowConditionRequest:
    type: WorkflowConditionType

    def __init__(self, type_p: WorkflowConditionType):
        self.type = type_p


class EventWorkflowConditionRequest(WorkflowConditionRequest):
    events: dict

    def __init__(self):
        super().__init__(WorkflowConditionType.EVENT)


class EntityWorkflowConditionRequest(WorkflowConditionRequest):
    entities: list

    def __init__(self):
        super().__init__(WorkflowConditionType.ENTITY)


class ProcessingChannelWorkflowConditionRequest(WorkflowConditionRequest):
    processing_channels: list

    def __init__(self):
        super().__init__(WorkflowConditionType.PROCESSING_CHANNEL)


class WorkflowActionRequest:
    type: WorkflowActionType

    def __init__(self, type_p: WorkflowActionType):
        self.type = type_p


class WebhookSignature:
    method: str
    key: str


class WebhookWorkflowActionRequest(WorkflowActionRequest):
    url: str
    headers: dict
    signature: WebhookSignature

    def __init__(self):
        super().__init__(WorkflowActionType.WEBHOOK)


class CreateWorkflowRequest:
    name: str
    active: bool
    conditions: list  # WorkflowConditionRequest
    actions: list  # WorkflowActionRequest


class UpdateWorkflowRequest:
    name: str
    active: bool


class ReflowRequest:
    workflows: list


class ReflowByEventsRequest(ReflowRequest):
    events: list


class ReflowBySubjectsRequest(ReflowRequest):
    subjects: list
