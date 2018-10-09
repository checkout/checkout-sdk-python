from checkout_sdk.common import DTO


class ThreeDS(DTO):
    def __init__(self, enabled=False, attempt_n3d=False, eci=None, cryptogram=None, xid=None):
        self.enabled = enabled
        self.attempt_n3d = attempt_n3d
        self.eci = eci
        self.cryptogram = cryptogram
        self.xid = xid
