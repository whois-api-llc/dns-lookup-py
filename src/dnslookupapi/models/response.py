import copy
from datetime import datetime

from .base import BaseModel
import sys

if sys.version_info < (3, 9):
    import typing


def _datetime_from_int(values: dict, key: str) -> datetime or None:
    if key in values and values[key]:
        return datetime.utcfromtimestamp(values[key])
    return None


def _string_value(values: dict, key: str) -> str:
    if key in values and values[key]:
        return str(values[key])
    return ''


def _float_value(values: dict, key: str) -> float:
    if key in values and values[key]:
        return float(values[key])
    return 0.0


def _int_value(values: dict, key: str) -> int:
    if key in values and values[key]:
        return int(values[key])
    return 0


def _list_value(values: dict, key: str) -> list:
    if key in values and type(values[key]) is list:
        return copy.deepcopy(values[key])
    return []


def _list_of_objects(values: dict, key: str, classname: str) -> list:
    r = []
    if key in values and type(values[key]) is list:
        r = [globals()[classname](x) for x in values[key]]
    return r


def _object_value(values: dict, classname: str) -> object:
    if values is not None:
        return globals()[classname](values)
    return 0


def _bool_value(values: dict, key: str) -> bool:
    if key in values and values[key]:
        return bool(values[key])
    return False


values_map = {1: 'address', 2: 'target', 15: 'target', 16: 'strings', 28: 'address', 257: 'value', 6: 'host'}
classnames_map = {6: 'DnsSoaRecord', 15: 'DnsMxRecord', 257: 'DnsCaaRecord'}


class DnsRecord(BaseModel):
    type: int
    dns_type: str
    name: str
    ttl: int
    value: str
    raw_text: str

    def __init__(self, values):
        super().__init__()
        self.type = 0
        self.dns_type = ''
        self.name = ''
        self.ttl = 0
        self.value = ''
        self.raw_text = ''

        if values:
            self.type = _int_value(values, 'type')
            self.dns_type = _string_value(values, 'dnsType')
            self.name = _string_value(values, 'name')
            self.ttl = _int_value(values, 'ttl')
            if values_map[self.type]:
                self.value = _string_value(values, values_map[self.type])
            if self.type == 16:
                self.value = "".join(_list_value(values, values_map[self.type]))
            self.raw_text = _string_value(values, 'rawText')


class DnsSoaRecord(DnsRecord):
    admin: str
    host: str
    expire: int
    minimum: int
    refresh: int
    retry: int
    serial: int

    def __init__(self, values):
        super().__init__(values)
        self.admin = ''
        self.host = ''
        self.expire = 0
        self.minimum = 0
        self.refresh = 0
        self.retry = 0
        self.serial = 0

        if values:
            self.admin = _string_value(values, 'admin')
            self.host = _string_value(values, 'host')
            self.expire = _int_value(values, 'expire')
            self.minimum = _int_value(values, 'minimum')
            self.refresh = _int_value(values, 'refresh')
            self.retry = _int_value(values, 'retry')
            self.serial = _int_value(values, 'serial')


class DnsMxRecord(DnsRecord):
    priority: int
    host: str

    def __init__(self, values):
        super().__init__(values)
        self.priority = 0
        self.host = ''

        if values:
            self.priority = _int_value(values, 'priority')
            self.host = _string_value(values, 'target')


class DnsCaaRecord(DnsRecord):
    flags: int
    tag: str

    def __init__(self, values):
        super().__init__(values)
        self.flags = 0
        self.tag = ''

        if values:
            self.flags = _int_value(values, 'flags')
            self.tag = _string_value(values, 'tag')


class Response(BaseModel):
    domain_name: str
    dns_types: str
    records_by_type: dict

    if sys.version_info < (3, 9):
        types: typing.List[int]
        dns_records: typing.List[DnsRecord]
    else:
        types: [int]
        dns_records: [DnsRecord]

    def __init__(self, values):
        super().__init__()
        self.domain_name = ''
        self.types = []
        self.dns_types = ''
        self.dns_records = []
        self.records_by_type = {x['dnsType']: [] for x in values['dnsRecords']}

        if values is not None:
            self.domain_name = _string_value(values, 'domainName')
            self.types = _list_value(values, 'types')
            self.dns_types = _string_value(values, 'dnsTypes')
            for rec in values['dnsRecords']:
                classname = classnames_map[rec['type']] if rec['type'] in classnames_map.keys() else 'DnsRecord'
                self.dns_records.append(_object_value(rec, classname))
                self.records_by_type[rec['dnsType']].append(_object_value(rec, classname))


class ErrorMessage(BaseModel):
    code: int
    message: str

    def __init__(self, values):
        super().__init__()

        self.code = 0
        self.message = ''

        if values is not None:
            self.code = _int_value(values, 'code')
            self.message = _string_value(values, 'messages')
