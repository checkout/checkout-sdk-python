"""Shared assertions for client tests.

Use these instead of the trivial pattern:

    mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
    assert client.create_card(PhysicalCardRequest()) == 'response'

which only verifies the mock-passthrough — not the path, body, or HTTP verb.
"""


def assert_api_call(mock, path, body=None):
    """Verify a mocked ApiClient.{get,post,put,patch,delete} call.

    Args:
        mock: the MagicMock returned by mocker.patch('checkout_sdk.api_client.ApiClient.<verb>', ...)
        path: the expected URL path (e.g. 'issuing/cards/card_id'). Compared by ==.
        body: optional — the expected request body object. Compared by `is`
              (identity) so a typo or accidental object swap is caught immediately.

    The HTTP verb is verified implicitly: if the client uses the wrong verb,
    the patched mock is never invoked and `assert_called_once()` will fail.

    Positional args on ApiClient.post/put/patch are (path, authorization, body, ...);
    ApiClient.get/delete pass (path, authorization, [params]). For verbs without a
    body, omit `body=` from the call site.
    """
    mock.assert_called_once()
    args = mock.call_args.args
    assert args[0] == path, f'path expected={path!r} got={args[0]!r}'
    if body is not None:
        assert len(args) >= 3, f'no body in call: {args!r}'
        assert args[2] is body, f'body mismatch: expected={body!r} got={args[2]!r}'
