from __future__ import absolute_import

from abc import abstractmethod

from requests import Session


class HttpClientBuilderInterface:

    @abstractmethod
    def get_client(self) -> Session:
        raise NotImplementedError()
