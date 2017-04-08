from .cookies import jar_to_har, har_to_jar


DEFAULT_COOKIEJAR_NAME = "_default"


def hars_to_cookiejars(hars, jars):
    for k, har in hars.items():
        jar_key = None if k == DEFAULT_COOKIEJAR_NAME else k
        har_to_jar(jars[jar_key], har)


def cookiejars_to_hars(cookiejars):
    return {
        (k if k else DEFAULT_COOKIEJAR_NAME): jar_to_har(jar)
        for k, jar in cookiejars.items()
    }


def find_cookie(name, cookiejars, key=None):
    key = None if key == DEFAULT_COOKIEJAR_NAME else key
    for jar_key, jar in cookiejars.items():
        if key and key != jar_key:
            continue
        for c in jar_to_har(jar):
            if c['name'] == name:
                return c
