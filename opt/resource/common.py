from base64 import b64encode
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


def with_source(func):
    def wrapper(payload):
        return func(payload['source'])
    return wrapper


@with_source
def get_index_url(source):
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


@with_source
def get_auth(source):
    return b64encode(':'.join([source['username'], source['password']]).encode('ascii'))


@with_source
def get_versioning_scheme(source):
    return source.get('versioning', 'loose')


def get_version(payload):
    try:
        version = payload['version']['version']
    except TypeError:
        version = None
    return version
