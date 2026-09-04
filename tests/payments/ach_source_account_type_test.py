from checkout_sdk.common.common import AccountHolder
from checkout_sdk.common.enums import (AccountType, AchInstrumentAccountType,
                                       AchSourceAccountType, AccountHolderType,
                                       PaymentSourceType)
from checkout_sdk.instruments.instruments import AchAccountHolder
from checkout_sdk.payments.payment_apm import (AchSourceAccountHolder,
                                               RequestAchSource)


# PaymentRequestAchSource is the only schema declaring savings / checking / cash.
# RequestAchSource previously used AccountType, which declares 'current' instead of
# 'checking', so a valid account type could not be sent and an invalid one was offered.
def test_ach_source_account_type_declares_the_three_values():
    assert AchSourceAccountType.SAVINGS.value == 'savings'
    assert AchSourceAccountType.CHECKING.value == 'checking'
    assert AchSourceAccountType.CASH.value == 'cash'
    assert len(list(AchSourceAccountType)) == 3


def test_ach_source_account_type_differs_from_the_shared_account_type():
    shared = [m.value for m in AccountType]
    # The shared enum offers 'current', which this position rejects, and cannot express
    # 'checking'. If these are ever unified, this fails.
    assert 'current' in shared
    assert 'checking' not in shared
    assert 'current' not in [m.value for m in AchSourceAccountType]


def test_ach_source_account_type_differs_from_the_instrument_account_type():
    instrument = [m.value for m in AchInstrumentAccountType]
    source = [m.value for m in AchSourceAccountType]
    # AchInstrumentAccountType serves the five stored ACH instrument positions, which declare
    # savings / checking only. It cannot express the source's 'cash'.
    assert instrument == ['savings', 'checking']
    assert 'cash' not in instrument
    assert 'cash' in source
    assert set(instrument) < set(source)


def test_the_instrument_ach_data_still_uses_the_instrument_enum():
    from checkout_sdk.instruments.instruments import AchInstrumentData
    # The instrument position must keep AchInstrumentAccountType, not the source enum.
    assert AchInstrumentData.__annotations__['account_type'] is AchInstrumentAccountType


def test_request_ach_source_is_typed_with_the_dedicated_enum():
    assert RequestAchSource.__annotations__['account_type'] is AchSourceAccountType
    assert RequestAchSource.__annotations__['account_holder'] is AchSourceAccountHolder


def test_request_ach_source_carries_the_ach_source_type():
    source = RequestAchSource()
    assert source.type == PaymentSourceType.ACH


def test_ach_source_account_holder_declares_the_seven_schema_properties():
    fields = list(AchSourceAccountHolder.__annotations__)
    assert fields == ['type', 'first_name', 'last_name', 'company_name',
                      'billing_address', 'date_of_birth', 'identification']


def test_ach_source_account_holder_is_narrower_than_the_shared_one():
    shared = set(AccountHolder.__annotations__)
    dedicated = set(AchSourceAccountHolder.__annotations__)
    # AccountHolder is a 16-property superset carrying a phone, a tax ID and more that
    # AccountHolderAch does not declare.
    assert len(shared) == 16
    assert dedicated < shared
    for absent in ('phone', 'tax_id', 'gender'):
        assert absent not in dedicated


def test_ach_source_account_holder_differs_from_the_instrument_one():
    instrument = set(AchAccountHolder.__annotations__)
    dedicated = set(AchSourceAccountHolder.__annotations__)
    # The instrument schema declares four properties and no billing address,
    # date of birth or identification.
    assert instrument == {'first_name', 'last_name', 'company_name', 'type'}
    assert 'billing_address' in dedicated
    assert 'billing_address' not in instrument


def test_ach_source_account_holder_type_accepts_government():
    holder = AchSourceAccountHolder()
    holder.type = AccountHolderType.GOVERNMENT
    # AccountHolderAch.type declares individual, corporate and government.
    assert holder.type.value == 'government'


def test_no_enum_name_is_defined_twice_with_different_values():
    """Guard against the name collision this rename fixed.

    common.enums and payments.setups.setups both used to define AchAccountType and
    SepaMandateType with different wire values. Each was correct for its own position,
    but importing the wrong one type-checked, ran, and sent a value the target schema
    rejects with no error until the API responded.
    """
    from enum import Enum
    import checkout_sdk.common.enums as common_enums
    import checkout_sdk.payments.setups.setups as setups

    def enums_of(mod):
        return {
            name: tuple(m.value for m in obj)
            for name, obj in vars(mod).items()
            if isinstance(obj, type) and issubclass(obj, Enum) and obj.__module__ == mod.__name__
        }

    a, b = enums_of(common_enums), enums_of(setups)
    clashing = {n for n in set(a) & set(b) if a[n] != b[n]}

    assert clashing == set(), f'enum names defined twice with different values: {clashing}'


def test_the_three_ach_account_type_positions_are_named_apart():
    from checkout_sdk.common.enums import AchInstrumentAccountType, AchSourceAccountType
    from checkout_sdk.payments.setups.setups import AchAccountType as SetupsAchAccountType

    # Mirrors the java naming: AchInstrumentAccountType / AchSourceAccountType /
    # setups AchAccountType. Three positions, three value sets, three names.
    assert [m.value for m in AchInstrumentAccountType] == ['savings', 'checking']
    assert [m.value for m in AchSourceAccountType] == ['savings', 'checking', 'cash']
    assert [m.value for m in SetupsAchAccountType] == ['savings', 'current', 'cash']

    names = {AchInstrumentAccountType.__name__, AchSourceAccountType.__name__,
             SetupsAchAccountType.__name__}
    assert len(names) == 3


def test_the_two_sepa_mandate_positions_are_named_apart():
    from checkout_sdk.common.enums import SepaMandateType
    from checkout_sdk.payments.setups.setups import SetupsSepaMandateType

    # The specification declares this field capitalized on the payment source and the
    # instrument, and lowercase on the Payment Setup. Both casings are real.
    assert [m.value for m in SepaMandateType] == ['Core', 'B2B']
    assert [m.value for m in SetupsSepaMandateType] == ['core', 'b2b']
    assert SepaMandateType.__name__ != SetupsSepaMandateType.__name__
