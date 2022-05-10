from checkout_sdk.http_metadata import HttpMetadata


def map_to_http_metadata(response):
    if response is None:
        return None
    http_metadata = HttpMetadata()
    http_metadata.reason_phrase = response.reason
    http_metadata.status_code = response.status_code
    http_metadata.headers = response.headers
    return http_metadata
