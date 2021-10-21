import unittest
from json import loads
from dnslookupapi import Response, ErrorMessage


_json_response_empty = '''{'ErrorMessage': {'msg': 'Unable to retrieve dns record for adakjhdqkjwdh.com'}}'''

_json_response_ok = r'''{
    "DNSData": {
        "domainName": "youtube.com",
        "types": [
            -1
        ],
        "dnsTypes": "_all",
        "audit": {
            "createdDate": "2021-10-19 17:08:42 UTC",
            "updatedDate": "2021-10-19 17:08:42 UTC"
        },
        "dnsRecords": [
            {
                "type": 16,
                "dnsType": "TXT",
                "name": "youtube.com.",
                "ttl": 3600,
                "rRsetType": 16,
                "rawText": "youtube.com.\t\t3600\tIN\tTXT\t\"google-site-verification=QtQWEwHWM8tHiJ4s-jJWzEQrD_fF3\"",
                "strings": [
                    "google-site-verification=QtQWEwHWM8tHiJ4s-jJWzEQrD_fF3"
                ]
            },
            {
                "type": 16,
                "dnsType": "TXT",
                "name": "youtube.com.",
                "ttl": 3600,
                "rRsetType": 16,
                "rawText": "youtube.com.\t\t3600\tIN\tTXT\t\"v=spf1 include:google.com mx -all\"",
                "strings": [
                    "v=spf1 include:google.com mx -all"
                ]
            },
            {
                "type": 1,
                "dnsType": "A",
                "name": "youtube.com.",
                "ttl": 300,
                "rRsetType": 1,
                "rawText": "youtube.com.\t\t300\tIN\tA\t142.250.68.78",
                "address": "142.250.68.78"
            },
            {
                "type": 257,
                "dnsType": "CAA",
                "name": "youtube.com.",
                "ttl": 21600,
                "rRsetType": 257,
                "rawText": "youtube.com.\t\t21600\tIN\tCAA\t0 issue \"pki.goog\"",
                "flags": 0,
                "tag": "issue",
                "value": "pki.goog"
            },
            {
                "type": 2,
                "dnsType": "NS",
                "name": "youtube.com.",
                "additionalName": "ns2.google.com.",
                "ttl": 21600,
                "rRsetType": 2,
                "rawText": "youtube.com.\t\t21600\tIN\tNS\tns2.google.com.",
                "target": "ns2.google.com."
            },
            {
                "type": 2,
                "dnsType": "NS",
                "name": "youtube.com.",
                "additionalName": "ns1.google.com.",
                "ttl": 21600,
                "rRsetType": 2,
                "rawText": "youtube.com.\t\t21600\tIN\tNS\tns1.google.com.",
                "target": "ns1.google.com."
            },
            {
                "type": 2,
                "dnsType": "NS",
                "name": "youtube.com.",
                "additionalName": "ns3.google.com.",
                "ttl": 21600,
                "rRsetType": 2,
                "rawText": "youtube.com.\t\t21600\tIN\tNS\tns3.google.com.",
                "target": "ns3.google.com."
            },
            {
                "type": 6,
                "dnsType": "SOA",
                "name": "youtube.com.",
                "ttl": 9,
                "rRsetType": 6,
                "rawText": "youtube.com.\t\t9\tIN\tSOA\tns1.google.com. dns-admin.google.com. 403904664 900 900 1800 60",
                "admin": "dns-admin.google.com.",
                "host": "ns1.google.com.",
                "expire": 1800,
                "minimum": 60,
                "refresh": 900,
                "retry": 900,
                "serial": 403904664
            },
            {
                "type": 28,
                "dnsType": "AAAA",
                "name": "youtube.com.",
                "ttl": 259,
                "rRsetType": 28,
                "rawText": "youtube.com.\t\t259\tIN\tAAAA\t2607:f8b0:4007:811:0:0:0:200e",
                "address": "2607:f8b0:4007:811:0:0:0:200e"
            },
            {
                "type": 15,
                "dnsType": "MX",
                "name": "youtube.com.",
                "additionalName": "smtp.google.com.",
                "ttl": 300,
                "rRsetType": 15,
                "rawText": "youtube.com.\t\t300\tIN\tMX\t0 smtp.google.com.",
                "priority": 11,
                "target": "smtp.google.com."
            }
        ]
    }
}
'''

_json_response_error = '''{
    "code": 403,
    "messages": "Access restricted. Check credits balance or enter the correct API key."
}'''


class TestModel(unittest.TestCase):

    def test_ok_response_parsing(self):
        response = loads(_json_response_ok)['DNSData']
        parsed = Response(response)
        self.assertEqual(parsed.domain_name, response['domainName'])
        self.assertIsInstance(parsed.dns_records, list)
        self.assertEqual(
            parsed.dns_records[2].value,
            response['dnsRecords'][2]['address'])
        self.assertEqual(
            parsed.dns_records[0].value,
            ''.join(response['dnsRecords'][0]['strings'])
        )
        self.assertEqual(
            parsed.dns_records[-1].priority,
            response['dnsRecords'][-1]['priority'])

    def test_by_type_parsing(self):
        response = loads(_json_response_ok)['DNSData']
        parsed = Response(response)
        self.assertIsInstance(parsed.records_by_type['NS'], list)
        self.assertEqual(len(parsed.records_by_type['NS']), 3)

    def test_soa_parsing(self):
        response = loads(_json_response_ok)['DNSData']
        parsed = Response(response)
        self.assertEqual(parsed.dns_records[7]['serial'],
                         response['dnsRecords'][7]['serial'])

    def test_error_parsing(self):
        error = loads(_json_response_error)
        parsed_error = ErrorMessage(error)
        self.assertEqual(parsed_error.code, error['code'])
        self.assertEqual(parsed_error.message, error['messages'])
