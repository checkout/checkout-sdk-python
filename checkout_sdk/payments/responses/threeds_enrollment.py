from checkout_sdk.common import RequestDTO


class ThreeDSEnrollment(RequestDTO):
    def __init__(self,
                 downgraded, enrolled, signature_valid,
                 authentication_response, eci, cryptogram, xid):
        self.downgraded = downgraded
        self.enrolled = enrolled
        self.signature_valid = signature_valid
        self.authentication_response = authentication_response
        self.eci = eci
        self.cryptogram = cryptogram
        self.xid = xid
