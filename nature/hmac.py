import base64
import hashlib
import hmac
import re
from datetime import datetime

import pytz
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.encoding import force_bytes
from sentry_sdk import capture_event

from hmac_auth.models import HMACGroup
from .enums import UserRole


class HMACAuth:
    """Validate a hmac request and check its authorization information."""

    ALLOWED_CLOCK_SKEW_IN_SECONDS = 300

    # Supported digest algorithms
    DIGEST_ALGORITHMS = {
        "hmac-sha1": hashlib.sha1,
        "hmac-sha256": hashlib.sha256,
        "hmac-sha384": hashlib.sha384,
        "hmac-sha512": hashlib.sha512,
    }

    def __init__(self, request):
        self.request = request

    @property
    def auth_header(self):
        return self.request.META.get(
            "HTTP_PROXY_AUTHORIZATION"
        ) or self.request.META.get("HTTP_AUTHORIZATION")

    @property
    def is_valid(self):
        """Return True if the request is valid

        The method validates two things:
        - The request is within allowed clock skew
        - The request has valid credentials

        :return: True if the request is valid
        :rtype: bool
        """
        return self.within_clock_skew and self.has_valid_credentials

    @property
    def has_admin_group(self):
        """Return true if the user has an admin group"""
        return any([group.is_admin_group for group in self.groups])

    @property
    def has_office_hki_group(self):
        """Return true if user has an office hki group"""
        return any([group.is_office_hki_group for group in self.groups])

    @property
    def has_office_group(self):
        """Return true if user has an office group"""
        return any([group.is_office_group for group in self.groups])

    @property
    def groups(self):
        group_names = self.request.META.get("HTTP_X_FORWARDED_GROUPS", "").split(";")
        return HMACGroup.objects.filter(name__in=group_names)

    @property
    def user_role(self):
        # seen as public access if no auth header provided
        if not self.auth_header:
            return UserRole.PUBLIC

        if not self.is_valid:
            event = self._get_event(
                "invalid-auth", "Authorization failed: invalid auth header provided"
            )
            capture_event(event)
            raise PermissionDenied()

        if self.has_admin_group:
            return UserRole.ADMIN
        elif self.has_office_hki_group:
            return UserRole.OFFICE_HKI
        elif self.has_office_group:
            return UserRole.OFFICE
        else:
            event = self._get_event(
                "invalid-group", "Authorization failed: invalid group provided"
            )
            capture_event(event)
            raise PermissionDenied()

    @property
    def within_clock_skew(self):
        if "HTTP_DATE" not in self.request.META:
            return False
        date = datetime.strptime(
            self.request.META["HTTP_DATE"], "%a, %d %b %Y %H:%M:%S %Z"
        )
        gmt = pytz.timezone("GMT")  # DATE header is always in GMT
        date = date.replace(tzinfo=gmt)
        now = timezone.now()
        return abs(date - now) < timezone.timedelta(
            seconds=self.ALLOWED_CLOCK_SKEW_IN_SECONDS
        )

    @property
    def has_valid_credentials(self):
        auth_type, credentials = self.auth_header.split(" ", maxsplit=1)
        if auth_type.lower() != "hmac":
            return False  # only hmac auth allowed

        p = re.compile(r'(\w+)="([^"]+)"')
        auth_info = dict(p.findall(credentials))

        required_keys = {"algorithm", "headers", "signature"}
        if not required_keys.issubset(auth_info):
            return False

        algorithm = auth_info["algorithm"]
        headers = auth_info["headers"].split(" ")
        signature = auth_info["signature"]

        meta_keys = [
            "HTTP_{0}".format(header.replace("-", "_").upper()) for header in headers
        ]
        if not set(meta_keys).issubset(self.request.META):
            return False

        signature_string = self._generate_signature_message(headers, meta_keys)
        digestmod = self.DIGEST_ALGORITHMS.get(algorithm)
        if not digestmod:
            return False
        expected_signature = self._generate_signature(digestmod, signature_string)
        return hmac.compare_digest(expected_signature, force_bytes(signature))

    def _generate_signature_message(self, headers, meta_keys):
        """Generate signature message

        See https://docs.konghq.com/hub/kong-inc/hmac-auth/#signature-string-construction
        for the specification of signature string construction
        """
        header_lines = []
        for header, meta_key in zip(headers, meta_keys):
            if header.lower() == "request-line":
                header_lines.append(self.request.META[meta_key])
            else:
                header_lines.append(
                    "{0}: {1}".format(header.lower(), self.request.META[meta_key])
                )
        return "\n".join(header_lines)

    def _generate_signature(self, digestmod, message):
        hmac_obj = hmac.HMAC(
            key=settings.SHARED_SECRET.encode("utf-8"),
            msg=message.encode("utf-8"),
            digestmod=digestmod,
        )
        return base64.b64encode(hmac_obj.digest())

    def _get_event(self, event_type, message):
        return {
            "type": event_type,
            "headers": self.request.headers,
            "path": self.request.get_full_path(),
            "ip-address": self._get_client_ip(),
            "message": message,
        }

    def _get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip
