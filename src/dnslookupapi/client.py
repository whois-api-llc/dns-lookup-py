import datetime
from json import loads, JSONDecodeError
import re

from .net.http import ApiRequester
from .models.response import Response
from .exceptions.error import ParameterError, EmptyApiKeyError, \
    UnparsableApiResponseError, ResponseError, ApiAuthError


class Client:
    __default_url = "https://www.whoisxmlapi.com/whoisserver/DNSService"
    _api_requester: ApiRequester or None
    _api_key: str
    _last_result: Response or None

    _re_api_key = re.compile(r'^at_[a-z0-9]{29}$', re.IGNORECASE)
    _re_domain_name = re.compile(
        r'^(?:[0-9a-z_](?:[0-9a-z-_]{0,62}(?<=[0-9a-z-_])[0-9a-z_])?\.)+'
        + r'[0-9a-z][0-9a-z-]{0,62}[a-z0-9]$', re.IGNORECASE)

    _SUPPORTED_FORMATS = ['json', 'xml']
    _PARSABLE_FORMAT = 'json'

    JSON_FORMAT = 'json'
    XML_FORMAT = 'xml'

    __DATETIME_OR_NONE_MSG = 'Value should be None or an instance of ' \
                             'datetime.date'
    _SUPPORTED_TYPES = {}

    def __init__(self, api_key: str, **kwargs):
        """
        :param api_key: str: Your API key.
        :key base_url: str: (optional) API endpoint URL.
        :key timeout: float: (optional) API call timeout in seconds
        """

        self._api_key = ''

        self.api_key = api_key

        if 'base_url' not in kwargs:
            kwargs['base_url'] = Client.__default_url

        self.api_requester = ApiRequester(**kwargs)

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = Client._validate_api_key(value)

    @property
    def api_requester(self) -> ApiRequester or None:
        return self._api_requester

    @api_requester.setter
    def api_requester(self, value: ApiRequester):
        self._api_requester = value

    @property
    def base_url(self) -> str:
        return self._api_requester.base_url

    @base_url.setter
    def base_url(self, value: str or None):
        if value is None:
            self._api_requester.base_url = Client.__default_url
        else:
            self._api_requester.base_url = value

    @property
    def last_result(self) -> Response or None:
        return self._last_result

    @last_result.setter
    def last_result(self, value: Response or None):
        if value is None:
            self._last_result = value
        elif isinstance(value, Response):
            self._last_result = value
        else:
            raise ValueError(
                "Values should be an instance of dnslookupapi.Response or None")

    @property
    def timeout(self) -> float:
        return self._api_requester.timeout

    @timeout.setter
    def timeout(self, value: float):
        self._api_requester.timeout = value

    def get(self, domain: str, rr_types: str = '_all') -> Response:
        """
        Get parsed API response as a `Response` instance.

        :key domain: Required. The website's domain name.
        :key rr_types: Optional. String.
            A, NS, SOA, MX, etc. You can specify multiple comma-separated values,
            e.g., 'A,SOA,TXT';
            _all (Default) for getting all record types.
        :return: `Response` instance
        :raises ConnectionError:
        :raises DnsLookupApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        response = self.get_raw(domain, rr_types, Client._PARSABLE_FORMAT)
        try:
            parsed = loads(str(response))

            if 'DNSData' not in parsed:
                if 'ErrorMessage' in parsed and 'errorCode' in parsed['ErrorMessage']:
                    if parsed['ErrorMessage']['errorCode'] == 'API_KEY_05':
                        raise ApiAuthError('Access restricted. Check credits balance or enter the correct API key.')
                raise ResponseError(parsed['ErrorMessage']['msg']
                                    if 'ErrorMessage' in parsed and 'msg' in parsed['ErrorMessage']
                                    else 'Could not find the correct root element.')

            if 'domainName' in parsed['DNSData']:
                self.last_result = Response(parsed['DNSData'])
                return self.last_result
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)
        except JSONDecodeError as error:
            raise UnparsableApiResponseError("Could not parse API response", error)

    def get_raw(self, domain: str, rr_types: str = '_all', output_format: str = _PARSABLE_FORMAT) -> str:
        """
        Get raw API response.

        :key domain: Required. The website's domain name.
        :key rr_types: Optional. String.
            A, NS, SOA, MX, etc. You can specify multiple comma-separated values,
            e.g., 'A,SOA,TXT';
            _all (Default) for getting all record types.
        :key output_format: Optional.
        Use Client.JSON_FORMAT and Client.XML_FORMAT
            constants
        :return: str
        :raises ConnectionError:
        :raises DnsLookupApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        if self.api_key == '':
            raise EmptyApiKeyError('')

        _domain = Client._validate_domain_name(domain)
        _rr_types = Client._validate_rr_types(rr_types)
        _output_format = Client._validate_output_format(output_format)

        return self._api_requester.get(self._build_payload(
            self.api_key,
            _domain,
            _rr_types,
            _output_format,
        ))

    @staticmethod
    def _validate_api_key(api_key) -> str:
        if Client._re_api_key.search(str(api_key)):
            return str(api_key)
        else:
            raise ParameterError("Invalid API key format.")

    @staticmethod
    def _validate_domain_name(value) -> str:
        if Client._re_domain_name.search(str(value)):
            return str(value)

        raise ParameterError("Invalid domain name")

    @staticmethod
    def _validate_output_format(value: str):
        if value.lower() in [Client.JSON_FORMAT, Client.XML_FORMAT]:
            return value.lower()

        raise ParameterError(
            f"Response format must be {Client.JSON_FORMAT} "
            f"or {Client.XML_FORMAT}")

    @staticmethod
    def _validate_rr_types(rr_types: str):
        return rr_types

    @staticmethod
    def _validate_date(value: datetime.date or None):
        if value is None or isinstance(value, datetime.date):
            return str(value)

        raise ParameterError(Client.__DATETIME_OR_NONE_MSG)

    @staticmethod
    def _build_payload(
            api_key,
            domain,
            rr_types,
            output_format
    ) -> dict:
        tmp = {
            'apiKey': api_key,
            'domainName': domain,
            'type': rr_types,
            'outputFormat': output_format
        }

        return {k: v for (k, v) in tmp.items() if v is not None}
