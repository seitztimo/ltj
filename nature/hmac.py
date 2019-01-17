import base64
import hashlib
import hmac
import re
from datetime import datetime

import pytz
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_bytes


class HMACAuth:
    """Validate a hmac request and check its authorization information."""

    # Allowed HMAC user groups
    ADMIN_GROUPS = ('ltj_admin', r'HELS000627\Paikkatietovipunen_ltj_admin')
    OFFICE_HKI_GROUPS = ('ltj_virka_hki', r'HELS000627\Paikkatietovipunen_ltj_virka')
    OFFICE_GROUPS = ('ltj_virka',)

    ALLOWED_CLOCK_SKEW_IN_SECONDS = 300

    # Supported digest algorithms
    DIGEST_ALGORITHMS = {
        'hmac-sha1': hashlib.sha1,
        'hmac-sha256': hashlib.sha256,
        'hmac-sha384': hashlib.sha384,
        'hmac-sha512': hashlib.sha512,
    }

    def __init__(self, request):
        self.request = request
        self._is_valid = None

    @property
    def is_valid(self):
        """Return True if the request is valid

        The method validates two things:
        - The request is within allowed clock skew
        - The request has valid credentials

        :return: True if the request is valid
        :rtype: bool
        """
        if self._is_valid is None:
            self._is_valid = (
                self.within_clock_skew
                and self.has_valid_credentials
            )
        return self._is_valid

    @property
    def has_admin_group(self):
        """Return true if the user has an admin group"""
        return self.is_valid and bool(set(self.ADMIN_GROUPS).intersection(self.groups))

    @property
    def has_office_hki_group(self):
        """Return true if user has an office hki group"""
        return self.is_valid and bool(set(self.OFFICE_HKI_GROUPS).intersection(self.groups))

    @property
    def has_office_group(self):
        """Return true if user has an office group"""
        return self.is_valid and bool(set(self.OFFICE_GROUPS).intersection(self.groups))

    @property
    def groups(self):
        return self.request.META.get('HTTP_X_FORWARDED_GROUPS', '').split(';')

    @property
    def within_clock_skew(self):
        if 'HTTP_DATE' not in self.request.META:
            return False
        date = datetime.strptime(self.request.META['HTTP_DATE'], '%a, %d %b %Y %H:%M:%S %Z')
        gmt = pytz.timezone('GMT')  # DATE header is always in GMT
        date = date.replace(tzinfo=gmt)
        now = timezone.now()
        return abs(date - now) < timezone.timedelta(seconds=self.ALLOWED_CLOCK_SKEW_IN_SECONDS)

    @property
    def has_valid_credentials(self):
        auth_header = (
            self.request.META.get('HTTP_PROXY_AUTHORIZATION')
            or self.request.META.get('HTTP_AUTHORIZATION')
        )
        if not auth_header:
            return False

        auth_type, credentials = auth_header.split(' ', maxsplit=1)
        if auth_type.lower() != 'hmac':
            return False  # only hmac auth allowed

        p = re.compile(r'(\w+)="([^"]+)"')
        auth_info = dict(p.findall(credentials))

        required_keys = {'algorithm', 'headers', 'signature'}
        if not required_keys.issubset(auth_info):
            return False

        algorithm = auth_info['algorithm']
        headers = auth_info['headers'].split(' ')
        signature = auth_info['signature']

        meta_keys = ['HTTP_{0}'.format(header.replace('-', '_').upper()) for header in headers]
        if not set(meta_keys).issubset(self.request.META):
            return False

        signature_string = self._generate_signature_message(headers, meta_keys)
        expected_signature = self._generate_signature(algorithm, signature_string)
        return hmac.compare_digest(expected_signature, force_bytes(signature))

    def _generate_signature_message(self, headers, meta_keys):
        """Generate signature message

        See https://docs.konghq.com/hub/kong-inc/hmac-auth/#signature-string-construction
        for the specification of signature string construction
        """
        header_lines = []
        for header, meta_key in zip(headers, meta_keys):
            if header.lower() == 'request-line':
                header_lines.append(self.request.META[meta_key])
            else:
                header_lines.append('{0}: {1}'.format(header.lower(), self.request.META[meta_key]))
        return '\n'.join(header_lines)

    def _generate_signature(self, algorithm, message):
        digestmod = self.DIGEST_ALGORITHMS.get(algorithm)
        hmac_obj = hmac.HMAC(
            key=settings.SHARED_SECRET.encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=digestmod,
        )
        return base64.b64encode(hmac_obj.digest())
