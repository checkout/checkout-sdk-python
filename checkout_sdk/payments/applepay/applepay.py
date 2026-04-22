from enum import Enum


class ProtocolVersions(str, Enum):
    EC_V1 = 'ec_v1'
    RSA_V1 = 'rsa_v1'


class UploadCertificateRequest:
    content: str


class EnrollDomainRequest:
    domain: str


class GenerateSigningRequestRequest:
    protocol_version: ProtocolVersions
