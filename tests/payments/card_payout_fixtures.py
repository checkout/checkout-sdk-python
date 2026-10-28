from checkout_sdk.common.common import AccountHolder, AccountHolderIdentification, Address, Phone
from checkout_sdk.common.enums import AccountHolderIdentificationType, AccountHolderType, Country

# Rich destination account holder shared by the card payout and unreferenced refund destination
# tests: the card and network_token positions of both requests accept these keys.
ACCOUNT_HOLDER_FIXTURE = {
    'type': 'individual',
    'first_name': 'John',
    'middle_name': 'Paul',
    'last_name': 'Smith',
    'billing_address': {
        'address_line1': '123 High St.',
        'address_line2': 'Flat 456',
        'city': 'London',
        'state': 'GB',
        'zip': 'SW1A 1AA',
        'country': 'GB'
    },
    'phone': {'country_code': '+44', 'number': '4155552671'},
    'identification': {
        'type': 'passport',
        'number': 'E12345678',
        'issuing_country': 'GB',
        'date_of_expiry': '2030-01-01'
    },
    'email': 'john.smith@example.com',
    'date_of_birth': '1985-05-15',
    'country_of_birth': 'GB'
}


def rich_account_holder():
    billing_address = Address()
    billing_address.address_line1 = '123 High St.'
    billing_address.address_line2 = 'Flat 456'
    billing_address.city = 'London'
    billing_address.state = 'GB'
    billing_address.zip = 'SW1A 1AA'
    billing_address.country = Country.GB

    phone = Phone()
    phone.country_code = '+44'
    phone.number = '4155552671'

    identification = AccountHolderIdentification()
    identification.type = AccountHolderIdentificationType.PASSPORT
    identification.number = 'E12345678'
    identification.issuing_country = Country.GB
    identification.date_of_expiry = '2030-01-01'

    account_holder = AccountHolder()
    account_holder.type = AccountHolderType.INDIVIDUAL
    account_holder.first_name = 'John'
    account_holder.middle_name = 'Paul'
    account_holder.last_name = 'Smith'
    account_holder.billing_address = billing_address
    account_holder.phone = phone
    account_holder.identification = identification
    account_holder.email = 'john.smith@example.com'
    account_holder.date_of_birth = '1985-05-15'
    account_holder.country_of_birth = Country.GB
    return account_holder
