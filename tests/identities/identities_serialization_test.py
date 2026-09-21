import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.identities.entities import (
    AttemptAssetsQueryFilter, AttemptsQueryFilter, IdvAddress, PhoneNumber,
)
from checkout_sdk.identities.addressdocumentverification.addressdocumentverification import (
    AddressDocumentVerificationRequest, DeclaredData as AdvDeclaredData,
)
from checkout_sdk.identities.faceauthentication.faceauthentication import (
    ClientInformation as FavClientInformation, FaceAuthenticationAttemptRequest,
)
from checkout_sdk.identities.iddocumentverification.iddocumentverification import (
    DeclaredData as IddvDeclaredData, IdDocumentVerificationRequest,
)
from checkout_sdk.identities.identityverification.identityverification import (
    ClientInformation as IdvClientInformation, DeclaredData as IdvDeclaredData,
    IdentityVerificationAndAttemptRequest, IdentityVerificationAttemptRequest,
    IdentityVerificationRequest,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _phone_number():
    phone_number = PhoneNumber()
    phone_number.country_code = '+33'
    phone_number.number = '5555550102'
    return phone_number


def _idv_address():
    address = IdvAddress()
    address.address_line1 = '123 Main Street'
    address.city = 'London'
    address.zip = 'SW1A 1AA'
    address.country = 'GB'
    return address


def _idv_declared_data():
    declared_data = IdvDeclaredData()
    declared_data.name = 'Hannah Bret'
    declared_data.birth_date = '1994-10-15'
    declared_data.email = 'hannah.bret@example.com'
    declared_data.phone_number = _phone_number()
    declared_data.address = _idv_address()
    return declared_data


def _idv_client_information():
    client_information = IdvClientInformation()
    client_information.pre_selected_residence_country = 'FR'
    client_information.pre_selected_language = 'en-US'
    client_information.pre_selected_document_issuing_country = 'GB'
    client_information.pre_selected_document_type = 'Travel Document'
    return client_information


class TestIdentitiesSerialization:

    def test_phone_number_serializes_both_properties(self):
        assert _serialize(_phone_number()) == {
            'country_code': '+33',
            'number': '5555550102',
        }

    def test_idv_address_serializes_every_property(self):
        address = _idv_address()
        address.address_line2 = 'Apt 4B'
        address.state = 'Greater London'

        assert _serialize(address) == {
            'address_line1': '123 Main Street',
            'address_line2': 'Apt 4B',
            'city': 'London',
            'state': 'Greater London',
            'zip': 'SW1A 1AA',
            'country': 'GB',
        }

    def test_identity_declared_data_serializes_every_property(self):
        result = _serialize(_idv_declared_data())

        assert result['name'] == 'Hannah Bret'
        assert result['birth_date'] == '1994-10-15'
        assert result['email'] == 'hannah.bret@example.com'
        assert result['phone_number'] == {'country_code': '+33', 'number': '5555550102'}
        assert result['address']['address_line1'] == '123 Main Street'
        assert result['address']['country'] == 'GB'
        assert len(result) == 5

    def test_identity_declared_data_round_trip(self):
        payload = json.dumps(_idv_declared_data(), cls=JsonSerializer)

        assert json.loads(payload) == _serialize(_idv_declared_data())

    def test_identity_declared_data_omits_unset_optional_fields(self):
        declared_data = IdvDeclaredData()
        declared_data.name = 'Hannah Bret'

        assert _serialize(declared_data) == {'name': 'Hannah Bret'}

    def test_identity_declared_data_reads_an_explicit_null_email(self):
        """email is nullable in the spec, so a response may carry an explicit null."""
        payload = json.loads('{"name":"Hannah Bret","birth_date":"1994-10-15","email":null}')

        assert 'email' in payload
        assert payload['email'] is None

    def test_address_document_declared_data_carries_only_the_shared_shape(self):
        """The ADV and IDDV requests take IdvDeclaredData, which has no phone_number, email or
        address. Those three belong to IdvIdentityDeclaredData and must not leak here."""
        assert list(AdvDeclaredData.__annotations__) == ['name', 'birth_date']
        assert list(IddvDeclaredData.__annotations__) == ['name', 'birth_date']

    def test_address_document_declared_data_serializes_birth_date(self):
        declared_data = AdvDeclaredData()
        declared_data.name = 'Hannah Bret'
        declared_data.birth_date = '1994-10-15'

        assert _serialize(declared_data) == {
            'name': 'Hannah Bret',
            'birth_date': '1994-10-15',
        }

    def test_face_authentication_client_information_keeps_the_two_field_shape(self):
        """FavClientInformation declares neither document field, so sending them would be a
        request the API rejects."""
        assert list(FavClientInformation.__annotations__) == [
            'pre_selected_residence_country', 'pre_selected_language',
        ]

    def test_identity_verification_client_information_adds_the_two_idv_only_fields(self):
        result = _serialize(_idv_client_information())

        assert result == {
            'pre_selected_residence_country': 'FR',
            'pre_selected_language': 'en-US',
            'pre_selected_document_issuing_country': 'GB',
            'pre_selected_document_type': 'Travel Document',
        }

    def test_identity_verification_attempt_request_serializes_phone_number(self):
        request = IdentityVerificationAttemptRequest()
        request.redirect_url = 'https://example.com/success'
        request.phone_number = _phone_number()
        request.client_information = _idv_client_information()

        result = _serialize(request)

        assert result['redirect_url'] == 'https://example.com/success'
        assert result['phone_number'] == {'country_code': '+33', 'number': '5555550102'}
        assert result['client_information']['pre_selected_document_type'] == 'Travel Document'

    def test_face_authentication_attempt_request_serializes_phone_number(self):
        client_information = FavClientInformation()
        client_information.pre_selected_residence_country = 'FR'

        request = FaceAuthenticationAttemptRequest()
        request.redirect_url = 'https://example.com/success'
        request.phone_number = _phone_number()
        request.client_information = client_information

        result = _serialize(request)

        assert result['phone_number']['country_code'] == '+33'
        assert result['client_information'] == {'pre_selected_residence_country': 'FR'}
        assert 'pre_selected_document_type' not in result['client_information']

    def test_identity_verification_attempt_request_from_swagger_example(self):
        payload = json.loads(
            '{"redirect_url":"https://example.com/success",'
            '"phone_number":{"country_code":"+33","number":"5555550102"},'
            '"client_information":{"pre_selected_residence_country":"FR",'
            '"pre_selected_document_issuing_country":"GB",'
            '"pre_selected_document_type":"Passport",'
            '"pre_selected_language":"en-US"}}'
        )

        assert payload['phone_number']['country_code'] == '+33'
        assert payload['client_information']['pre_selected_document_type'] == 'Passport'

    def test_identity_verification_request_carries_the_identity_declared_data(self):
        request = IdentityVerificationRequest()
        request.applicant_id = 'aplt_tkoi5db4hryu5cei5vwoabr7we'
        request.user_journey_id = 'usj_tkoi5db4hryu5cei5vwoabr7we'
        request.declared_data = _idv_declared_data()

        result = _serialize(request)

        assert result['applicant_id'] == 'aplt_tkoi5db4hryu5cei5vwoabr7we'
        assert result['declared_data']['email'] == 'hannah.bret@example.com'
        assert result['declared_data']['phone_number']['country_code'] == '+33'
        assert result['declared_data']['address']['country'] == 'GB'

    def test_identity_verification_and_attempt_request_carries_the_identity_declared_data(self):
        request = IdentityVerificationAndAttemptRequest()
        request.applicant_id = 'aplt_tkoi5db4hryu5cei5vwoabr7we'
        request.redirect_url = 'https://example.com/success'
        request.declared_data = _idv_declared_data()

        result = _serialize(request)

        assert result['redirect_url'] == 'https://example.com/success'
        assert result['declared_data']['birth_date'] == '1994-10-15'
        assert result['declared_data']['address']['city'] == 'London'

    def test_address_document_verification_request_serializes_declared_data(self):
        declared_data = AdvDeclaredData()
        declared_data.name = 'Hannah Bret'

        request = AddressDocumentVerificationRequest()
        request.applicant_id = 'aplt_tkoi5db4hryu5cei5vwoabr7we'
        request.user_journey_id = 'usj_tkoi5db4hryu5cei5vwoabr7we'
        request.declared_data = declared_data

        assert _serialize(request)['declared_data'] == {'name': 'Hannah Bret'}

    def test_id_document_verification_request_serializes_declared_data(self):
        declared_data = IddvDeclaredData()
        declared_data.name = 'Hannah Bret'
        declared_data.birth_date = '1994-10-15'

        request = IdDocumentVerificationRequest()
        request.applicant_id = 'aplt_tkoi5db4hryu5cei5vwoabr7we'
        request.declared_data = declared_data

        assert _serialize(request)['declared_data']['birth_date'] == '1994-10-15'

    def test_attempts_query_filter_serializes_skip_and_limit(self):
        query = AttemptsQueryFilter()
        query.skip = 5
        query.limit = 25

        assert _serialize(query) == {'skip': 5, 'limit': 25}

    def test_attempts_query_filter_keeps_an_explicit_zero_skip(self):
        """skip=0 is a meaningful value, not an absent one."""
        query = AttemptsQueryFilter()
        query.skip = 0
        query.limit = 10

        assert _serialize(query) == {'skip': 0, 'limit': 10}

    def test_attempts_query_filter_serializes_limit_only(self):
        query = AttemptsQueryFilter()
        query.limit = 25

        assert _serialize(query) == {'limit': 25}

    def test_empty_attempts_query_filter_serializes_to_an_empty_object(self):
        assert _serialize(AttemptsQueryFilter()) == {}

    def test_attempt_assets_query_filter_serializes_skip_and_limit(self):
        query = AttemptAssetsQueryFilter()
        query.skip = 2
        query.limit = 50

        assert _serialize(query) == {'skip': 2, 'limit': 50}
