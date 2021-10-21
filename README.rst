.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: website-contacts-py license
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/dns-lookup-api.svg
    :alt: dns-lookup-py release
    :target: https://pypi.org/project/dns-lookup-api

.. image:: https://github.com/whois-api-llc/dns-lookup-py/workflows/Build/badge.svg
    :alt: dns-lookup-py build
    :target: https://github.com/whois-api-llc/dns-lookup-py/actions

========
Overview
========

The client library for
`DNS Lookup API <https://dns-lookup.whoisxmlapi.com/api>`_
in Python language.

The minimum Python version is 3.6.

Installation
============

.. code-block:: shell

    pip install dns-lookup-api

Examples
========

Full API documentation available `here <https://dns-lookup.whoisxmlapi.com/api/documentation/making-requests>`_

Create a new client
-------------------

.. code-block:: python

    from dnslookupapi import *

    client = Client('Your API key')

Make basic requests
-------------------

.. code-block:: python

    # Get DNS records for a domain name.
    response = client.get('youtube.com')
    print(response)
    print(response.records_by_type['MX'])

    # Get raw API response in XML format
    raw_result = client.get_raw('bbc.com',
        output_format=Client.XML_FORMAT)

Advanced usage
-------------------

Extra request parameters

.. code-block:: python

    result = client.get(
        'samsung.com',
        'A,MX,NS')

Response model overview
-----------------------

.. code-block:: python

    Response:
        - domain_name: [str]
        - dns_types: str
        - types: [int]
        - dns_records: [DnsRecord]
            - name: str
            - type: int
            - dns_type: str
            - ttl: int
            - value: str
            - raw_text: str
        - meta_description: str
        - meta_title: str
        - records_by_type: { 'dns_type' -> [DnsRecord] }


Sample response
---------------

.. code-block:: python

  {
  'domain_name': 'youtube.com',
  'types': '[-1]',
  'dns_types': '_all',
  'dns_records': [
        {'type': '16', 'dns_type': 'TXT', 'name': 'youtube.com.', 'ttl': '3600',
         'value': 'v=spf1 include:google.com mx -all',
         'raw_text': 'youtube.com.\t\t3600\tIN\tTXT\t"v=spf1 include:google.com mx -all"'},
        {'type': '16', 'dns_type': 'TXT', 'name': 'youtube.com.', 'ttl': '3600',
         'value': 'google-site-verification=QtQWEwHWM8tHiJ4s-jJWzEQrD_fF3luPnpzNDH-Nw-w',
         'raw_text': 'youtube.com.\t\t3600\tIN\tTXT\t"google-site-verification=QtQWEwHWM8tHiJ4s-jJWzEQrD_fF3luPnpzNDH-Nw-w"'},
        {'type': '1', 'dns_type': 'A', 'name': 'youtube.com.', 'ttl': '300',
         'value': '142.250.68.78',
         'raw_text': 'youtube.com.\t\t300\tIN\tA\t142.250.68.78'},
        {'type': '257', 'dns_type': 'CAA', 'name': 'youtube.com.', 'ttl': '21600',
         'value': 'pki.goog',
         'raw_text': 'youtube.com.\t\t21600\tIN\tCAA\t0 issue "pki.goog"',
         'flags': '0', 'tag': 'issue'},
        {'type': '2', 'dns_type': 'NS', 'name': 'youtube.com.', 'ttl': '21600',
         'value': 'ns2.google.com.',
         'raw_text': 'youtube.com.\t\t21600\tIN\tNS\tns2.google.com.'},
        {'type': '2', 'dns_type': 'NS', 'name': 'youtube.com.', 'ttl': '21600',
         'value': 'ns1.google.com.',
         'raw_text': 'youtube.com.\t\t21600\tIN\tNS\tns1.google.com.'},
        {'type': '6', 'dns_type': 'SOA', 'name': 'youtube.com.', 'ttl': '60',
         'value': 'ns1.google.com.',
         'raw_text': 'youtube.com.\t\t60\tIN\tSOA\tns1.google.com. dns-admin.google.com. 404480356 900 900 1800 60',
         'admin': 'dns-admin.google.com.', 'host': 'ns1.google.com.',
         'expire': '1800', 'minimum': '60', 'refresh': '900', 'retry': '900',
         'serial': '404480356'},
        {'type': '28', 'dns_type': 'AAAA', 'name': 'youtube.com.', 'ttl': '300',
         'value': '2607:f8b0:4007:811:0:0:0:200e',
         'raw_text': 'youtube.com.\t\t300\tIN\tAAAA\t2607:f8b0:4007:811:0:0:0:200e'},
        {'type': '15', 'dns_type': 'MX', 'name': 'youtube.com.', 'ttl': '254',
         'value': 'smtp.google.com.',
         'raw_text': 'youtube.com.\t\t254\tIN\tMX\t0 smtp.google.com.',
         'priority': '0', 'host': 'smtp.google.com.'}
                  ]

  'records_by_type':
    {'TXT': [
            {'type': '16', 'dns_type': 'TXT', 'name': 'youtube.com.', 'ttl': '3600',
             'value': 'v=spf1 include:google.com mx -all',
             'raw_text': 'youtube.com.\t\t3600\tIN\tTXT\t"v=spf1 include:google.com mx -all"'},
            {'type': '16', 'dns_type': 'TXT', 'name': 'youtube.com.', 'ttl': '3600',
             'value': 'google-site-verification=QtQWEwHWM8tHiJ4s-jJWzEQrD_fF3luPnpzNDH-Nw-w',
             'raw_text': 'youtube.com.\t\t3600\tIN\tTXT\t"google-site-verification=QtQWEwHWM8tHiJ4s-jJWzEQrD_fF3luPnpzNDH-Nw-w"'}
            ],
     'A':   [
            {'type': '1', 'dns_type': 'A', 'name': 'youtube.com.', 'ttl': '300',
             'value': '142.250.68.78',
             'raw_text': 'youtube.com.\t\t300\tIN\tA\t142.250.68.78'}
            ],
     'CAA': [
            {'type': '257', 'dns_type': 'CAA', 'name': 'youtube.com.', 'ttl': '21600',
             'value': 'pki.goog',
             'raw_text': 'youtube.com.\t\t21600\tIN\tCAA\t0 issue "pki.goog"',
             'flags': '0', 'tag': 'issue'}
            ],
     'NS':  [
            {'type': '2', 'dns_type': 'NS', 'name': 'youtube.com.', 'ttl': '21600',
             'value': 'ns2.google.com.',
             'raw_text': 'youtube.com.\t\t21600\tIN\tNS\tns2.google.com.'},
            {'type': '2', 'dns_type': 'NS', 'name': 'youtube.com.', 'ttl': '21600',
             'value': 'ns1.google.com.',
             'raw_text': 'youtube.com.\t\t21600\tIN\tNS\tns1.google.com.'}
            ],
     'SOA': [
            {'type': '6', 'dns_type': 'SOA', 'name': 'youtube.com.', 'ttl': '60',
             'value': 'ns1.google.com.',
             'raw_text': 'youtube.com.\t\t60\tIN\tSOA\tns1.google.com. dns-admin.google.com. 404480356 900 900 1800 60',
             'admin': 'dns-admin.google.com.', 'host': 'ns1.google.com.',
             'expire': '1800', 'minimum': '60', 'refresh': '900',
             'retry': '900', 'serial': '404480356'}
            ],
     'AAAA': [
            {'type': '28', 'dns_type': 'AAAA', 'name': 'youtube.com.', 'ttl': '300',
             'value': '2607:f8b0:4007:811:0:0:0:200e',
             'raw_text': 'youtube.com.\t\t300\tIN\tAAAA\t2607:f8b0:4007:811:0:0:0:200e'}
             ],
     'MX':  [
            {'type': '15', 'dns_type': 'MX', 'name': 'youtube.com.', 'ttl': '254',
             'value': 'smtp.google.com.',
             'raw_text': 'youtube.com.\t\t254\tIN\tMX\t0 smtp.google.com.',
             'priority': '0',
             'host': 'smtp.google.com.'}
            ]
    }
  }
