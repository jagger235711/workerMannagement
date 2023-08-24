import hashlib

from django.conf import settings


def md5(data_string):
    """
    Returns the md5 hexdigest of a string.
    """
    m = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    m.update(data_string.encode('utf-8'))
    return m.hexdigest()
