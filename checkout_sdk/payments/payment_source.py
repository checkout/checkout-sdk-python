from checkout_sdk.common import RequestDTO


class PaymentSource(RequestDTO):
    def __init__(self, type):
        self.type = type

    # this function allows to export class-type attributes into dictionaries
    def _get_dict_extended(self, attr_list):
        # Python 3.4 compatible
        attrib_copy = self.__dict__.copy()
        attr_dict = {}
        # add each item to dictionary
        for attr in attr_list:
            attr_value = getattr(self, attr)
            # the value is the dictionary value
            attr_dict[attr] = attr_value.get_dict() if isinstance(
                attr_value, RequestDTO) else attr_value

        attrib_copy.update(attr_dict)
        return attrib_copy
