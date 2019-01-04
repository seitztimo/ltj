import hmac
import hashlib
import base64
from django.utils.encoding import force_bytes
from ltj.settings import SHARED_SECRET


def signature_is_valid(date, host, groups_string, request_line, received_signature):
    signing_string = 'date: {0}\nhost: {1}\nx-forwarded-groups: {2}\n{3}'.format(
        date,
        host,
        groups_string,
        request_line
        )
    hmac_obj = hmac.HMAC(key=str.encode(SHARED_SECRET), msg=signing_string.encode('utf-8'), digestmod=hashlib.sha256)
    checksum = base64.b64encode(hmac_obj.digest())
    return hmac.compare_digest(force_bytes(checksum), force_bytes(received_signature))
