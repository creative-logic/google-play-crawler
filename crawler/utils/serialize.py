import base64
import hashlib
import json


def json_hash(data):
    """
    Return the hash of the input encoded to JSON
    """
    json_text = json.dumps(data, separators=(',', ':'))
    return hashlib.md5(json_text).hexdigest()


def deserialize_arg(arg):
    json_data = base64.standard_b64decode(arg)
    return json.loads(json_data)
