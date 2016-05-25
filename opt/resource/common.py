import json
import tempfile
from urllib.parse import urljoin
import sys


def get_payload():
    payload = json.load(sys.stdin)
    _, fname = tempfile.mkstemp()
    print("Logging payload to {}".format(fname), file=sys.stderr)
    with open(fname, 'w') as fp:
        fp.write(json.dumps(payload))
    return payload


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
    try:
        version = payload['version']['version']
    except TypeError:
        version = None
    return version
