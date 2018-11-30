from checkout_sdk.payments.responses import Payment, Customer, ThreeDSEnrollment


class PaymentPending(Payment):
    def __init__(self, api_response):
        super().__init__(api_response, is_pending=True)

        customer = api_response.body.get('customer')
        if customer is not None:
            self._customer = Customer(
                id=customer.get('id'),
                email=customer.get('email'),
                name=customer.get('name')
            )

        threeds = api_response.body.get('3ds')
        if threeds is not None:
            self._threeds = ThreeDSEnrollment(
                downgraded=threeds.get('downgraded'),
                enrolled=threeds.get('enrolled'),
                signature_valid=threeds.get('signature_valid'),
                authentication_response=threeds.get('authentication_response'),
                eci=threeds.get('eci'),
                cryptogram=threeds.get('cavv'),
                xid=threeds.get('xid')
            )

    @property
    def customer(self):
        return self._customer

    @property
    def threeds(self):
        return self._threeds

    @property
    def requires_redirect(self):
        return self.has_link('redirect')

    @property
    def redirect_link(self):
        return self.get_link('redirect')
