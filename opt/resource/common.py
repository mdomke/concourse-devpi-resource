import json
from urllib.parse import urljoin
import sys


def get_payload():
    return json.load(sys.stdin)


def get_index_url(payload):
    source = payload['source']
    uri = source['uri']
    index = source['index']
    if not uri.endswith('/'):
        uri += '/'
    if not index.endswith('/'):
        index += '/'
    return urljoin(uri, index)


def get_package_url(payload):
    package = payload['source']['package']
    return get_index_url(payload) + package


def get_auth(payload):
    source = payload['source']
    return source['username'], source['password']


def get_version(payload):
    if 'version' in payload:
        version = payload['version']['version']
    else:
        version = None
    return version
