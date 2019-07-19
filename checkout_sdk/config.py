import re
import os

from checkout_sdk import constants, logger

SECRET_KEY_REGEX = re.compile(
    r'^sk_(test_)?(\w{8})-(\w{4})-(\w{4})-(\w{4})-(\w{12})$', re.IGNORECASE)
HTTP_PROTOCOL_REGEX = re.compile(r'^http(s)?', re.IGNORECASE)

API_BASE_URLS = {
    'sandbox': 'https://api.sandbox.checkout.com/',
    'production': 'https://api.checkout.com/'
}

# using lambda functions here so that
# env variables are read at the time of access
ENV_SETTINGS = {
    'secret_key':
        lambda: os.environ.get('CKO_SECRET_KEY'),
    'sandbox':
        lambda: os.environ.get('CKO_SANDBOX', 'true').lower() in ['true', '1']
}


class Config:
    def __init__(self, secret_key=None, sandbox=None,
                 timeout=constants.DEFAULT_TIMEOUT, api_base_url=None):
        self.secret_key = \
            secret_key if secret_key else ENV_SETTINGS['secret_key']()
        self.timeout = timeout
        # use custom api_base_url if local dev, integration testing, etc
        # else `sandbox` determines the URL
        if api_base_url:
            self.api_base_url = api_base_url
        else:
            sandbox = \
                sandbox if sandbox is not None else ENV_SETTINGS['sandbox']()
            self.api_base_url = API_BASE_URLS['sandbox'] if sandbox is True \
                else API_BASE_URLS['production']

        logger.info('%s - sk%s%s', self.api_base_url, '*' * 6,
                    self.secret_key[-6:])

    @property
    def secret_key(self):
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        if SECRET_KEY_REGEX.match(value or ''):
            self._secret_key = value
        else:
            raise ValueError('Invalid secret key.')

    @property
    def api_base_url(self):
        return self._api_base_url

    @api_base_url.setter
    def api_base_url(self, value):
        self._api_base_url = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        try:
            self._timeout = int(value)
        except ValueError:
            raise ValueError(
                'Invalid timeout. Default is {} milliseconds'
                .format(constants.DEFAULT_TIMEOUT))
