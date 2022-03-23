import checkout_sdk.customers.customers


class CustomerRequest(checkout_sdk.customers.customers.CustomerRequest):
    instruments: list
