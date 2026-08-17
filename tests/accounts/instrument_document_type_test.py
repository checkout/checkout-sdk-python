from checkout_sdk.common.enums import DocumentType, InstrumentDocumentType


def test_should_expose_bank_statement_for_instrument_documents():
    assert InstrumentDocumentType.BANK_STATEMENT == 'bank_statement'
    assert InstrumentDocumentType.BANK_STATEMENT.value == 'bank_statement'


def test_should_be_the_only_accepted_instrument_document_type():
    # The spec declares a single-value enum here, so anything else is a caller error rather
    # than a value we forgot to add.
    assert [d.value for d in InstrumentDocumentType] == ['bank_statement']


def test_should_keep_bank_statement_out_of_the_identity_document_type():
    # bank_statement belongs to the instrument document enum, not the identity one. The API
    # keeps them separate, and this is what stops the two being merged the next time someone
    # reports the value as missing from DocumentType.
    assert 'bank_statement' not in [d.value for d in DocumentType]
