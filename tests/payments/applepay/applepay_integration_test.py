from __future__ import absolute_import

import pytest

from checkout_sdk.payments.applepay.applepay import UploadCertificateRequest, EnrollDomainRequest, \
    GenerateSigningRequestRequest, ProtocolVersions
from tests.checkout_test_utils import assert_response


# tests

@pytest.mark.skip(reason='Requires valid payment processing certificate')
def test_should_upload_payment_processing_certificate(default_api):
    request = create_upload_certificate_request()
    response = default_api.apple_pay.upload_payment_processing_certificate(request)
    assert_upload_certificate_response(response)


@pytest.mark.skip(reason='Requires OAuth credentials and valid domain verification')
def test_should_enroll_domain(default_api):
    request = create_enroll_domain_request()
    response = default_api.apple_pay.enroll_domain(request)
    assert response is not None


def test_should_generate_certificate_signing_request(default_api):
    request = create_generate_signing_request(ProtocolVersions.EC_V1)
    response = default_api.apple_pay.generate_certificate_signing_request(request)
    assert_generate_signing_request_response(response)


def test_should_generate_certificate_signing_request_with_rsa_protocol(default_api):
    request = create_generate_signing_request(ProtocolVersions.RSA_V1)
    response = default_api.apple_pay.generate_certificate_signing_request(request)
    assert_generate_signing_request_response(response)


# common methods

def create_upload_certificate_request() -> UploadCertificateRequest:
    request = UploadCertificateRequest()
    request.content = ('MIIEfTCCBCOgAwIBAgIID/asezaWNycwCgYIKoZIzj0EAwIwgYAxNDAyBgNVBAMMK0FwcGxlIFdvcmxkd2lkZSBEZXZlbG9w'
                       'ZXIgUmVsYXRpb25zIENBIC0gRzIxJjAkBgNVBAsMHUFwcGxlIENlcnRpZmljYXRpb24gQXV0aG9yaXR5MRMwEQYDVQQK'
                       'DApBcHBsZSBJbmMuMQswCQYDVQQGEwJVUzAeFw0yMTA2MTExMzQ0MjVaFw0yMzA3MTExMzQ0MjRaMIGuMS0wKwYKCZIm'
                       'iZPyLGQBAQwdbWVyY2hhbnQuY29tLmNoZWNrb3V0LnNhbmRib3gxQzBBBgNVBAMMOkFwcGxlIFBheSBQYXltZW50IFBy'
                       'b2Nlc3Npbmc6bWVyY2hhbnQuY29tLmNoZWNrb3V0LnNhbmRib3gxEzARBgNVBAsMCkUzMlhCUUs0UTUxFjAUBgNVBAoM'
                       'DUNoZWNrb3V0IEx0ZC4xCzAJBgNVBAYTAkdCMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEsvyUM9D1cssldH+VPpt'
                       'En4VAw/Q6ovJuHVlyBSRaPGLHFce04lCiT/xnXOWRkUxyCzQWKhfG2zo19u4s+evx7aOCAlUwggJRMAwGA1UdEwEB/w'
                       'QCMAAwHwYDVR0jBBgwFoAUhLaEzDqGYnIWWZToGqO9SN863wswRwYIKwYBBQUHAQEEOzA5MDcGCCsGAQUFBzABhitod'
                       'HRwOi8vb2NzcC5hcHBsZS5jb20vb2NzcDA0LWFwcGxld3dkcmNhMjAxMIIBHQYDVR0gBIIBFDCCARAwggEMBgkqhkiG'
                       '92NkBQEwgf4wgcMGCCsGAQUFBwICMIG2DIGzUmVsaWFuY2Ugb24gdGhpcyBjZXJ0aWZpY2F0ZSBieSBhbnkgcGFydCBh'
                       'c3N1bWVzIGFjY2VwdGFuY2Ugb2YgdGhlIHRoZW4gYXBwbGljYWJsZSBzdGFuZGFyZCB0ZXJtcyBhbmQgY29uZGl0aW'
                       'ducyBvZiB1c2UsIGNlcnRpZmljYXRlIHBvbGljeSBhbmQgY2VydGlmaWNhdGlvbiBwcmFjdGljZSBzdGF0ZW1lbnRzLj'
                       'A2BggrBgEFBQcCAQYqaHR0cDovL3d3dy5hcHBsZS5jb20vY2VydGlmaWNhdGVhdXRob3JpdHkvMDYGA1UdHwQvMC0wK6'
                       'ApoCeGJWh0dHA6Ly9jcmwuYXBwbGUuY29tL2FwcGxld3dkcmNhMi5jcmwwHQYDVR0OBBYEFE2G+vfc0O4zhDEFl3Xpr'
                       '4AJsegTMA4GA1UdDwEB/wQEAwIHIDBPBgoZhkiG92NkBgAEBEIMQDdGRjg0REI5MDE5NkVGN0I5RTc4NDZEMjg4NzZCNk'
                       'JGRDU2RjM4MDlCNzUyNjAzRDM4QzcxNUJFMTY2M0JENEMwCgYIKoZIzj0EAwIDSAAwRQIgTjywMwOrLX3TwDUrPn7yDG'
                       'L/dhc+VNudv0uGBOWRyXACIQClFQFvgx+hfTwVdHt8klrswpgtZtbYjs74p9GYuc8Puw==')
    return request


def create_enroll_domain_request() -> EnrollDomainRequest:
    request = EnrollDomainRequest()
    request.domain = 'checkout-test-domain.com'
    return request


def create_generate_signing_request(protocol_version: ProtocolVersions) -> GenerateSigningRequestRequest:
    request = GenerateSigningRequestRequest()
    request.protocol_version = protocol_version
    return request


def assert_upload_certificate_response(response):
    assert_response(response, 'http_metadata', 'id', 'public_key_hash', 'valid_from', 'valid_until')
    assert response.valid_until > response.valid_from


def assert_generate_signing_request_response(response):
    assert_response(response, 'http_metadata', 'content')
    assert 'BEGIN CERTIFICATE REQUEST' in response.content
    assert 'END CERTIFICATE REQUEST' in response.content
