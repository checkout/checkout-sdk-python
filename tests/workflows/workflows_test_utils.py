from __future__ import absolute_import

from checkout_sdk.four.checkout_api import CheckoutApi
from checkout_sdk.workflows.workflows import CreateWorkflowRequest, WebhookWorkflowActionRequest, WebhookSignature, \
    EntityWorkflowConditionRequest, EventWorkflowConditionRequest, ProcessingChannelWorkflowConditionRequest
from tests.checkout_test_utils import assert_response, retriable

__WORKFLOW_ENTITY_ID = 'ent_kidtcgc3ge5unf4a5i6enhnr5m'
__PROCESSING_CHANNEL_ID = 'pc_5jp2az55l3cuths25t5p3xhwru'
__WORKFLOW_NAME = 'testing'
__WORKFLOWS: list = []


def create_workflow(four_api):
    signature = WebhookSignature()
    signature.key = '8V8x0dLK%AyD*DNS8JJr'
    signature.method = 'HMACSHA256'

    action_request = WebhookWorkflowActionRequest()
    action_request.url = "https://google.com/fail"
    action_request.headers = {}
    action_request.signature = signature

    entity_condition_request = EntityWorkflowConditionRequest()
    entity_condition_request.entities = [__WORKFLOW_ENTITY_ID]

    event_condition_request = EventWorkflowConditionRequest()
    event_condition_request.events = {'gateway': ["payment_approved",
                                                  "payment_declined",
                                                  "card_verification_declined",
                                                  "card_verified",
                                                  "payment_authorization_incremented",
                                                  "payment_authorization_increment_declined",
                                                  "payment_capture_declined",
                                                  "payment_captured",
                                                  "payment_refund_declined",
                                                  "payment_refunded",
                                                  "payment_void_declined",
                                                  "payment_voided"],
                                      'dispute': ["dispute_canceled",
                                                  "dispute_evidence_required",
                                                  "dispute_expired",
                                                  "dispute_lost",
                                                  "dispute_resolved",
                                                  "dispute_won"]}

    processing_channel_condition_request = ProcessingChannelWorkflowConditionRequest()
    processing_channel_condition_request.processing_channels = [__PROCESSING_CHANNEL_ID]

    workflow_request = CreateWorkflowRequest()
    workflow_request.actions = [action_request]
    workflow_request.conditions = [entity_condition_request, event_condition_request,
                                   processing_channel_condition_request]
    workflow_request.name = __WORKFLOW_NAME
    workflow_request.active = True

    response = retriable(callback=four_api.workflows.create_workflow,
                         create_workflow_request=workflow_request)

    assert_response(response, 'id')

    __WORKFLOWS.append(response['id'])

    return response


def clean_workflows(four_api: CheckoutApi):
    for prop in __WORKFLOWS:
        four_api.workflows.remove_workflow(prop)
