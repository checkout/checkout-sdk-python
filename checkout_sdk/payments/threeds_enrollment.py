from checkout_sdk.common import DTO


class ThreeDSEnrollment(DTO):
    def __init__(self,
                 downgraded, enrolled, signature_valid,
                 authentication_response, eci, cavv, xid):
        self.downgraded = downgraded
        self.enrolled = enrolled
        self.signature_valid = signature_valid
        self.authentication_response = authentication_response
        self.eci = eci
        self.cavv = cavv
        self.xid = xid
