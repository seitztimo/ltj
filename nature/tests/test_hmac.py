from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory, override_settings
from freezegun import freeze_time

from hmac_auth.models import HMACGroup
from hmac_auth.tests.factories import HMACGroupFactory
from nature.enums import UserRole
from nature.hmac import HMACAuth


@override_settings(SHARED_SECRET="secret")
class TestHMACAuth(TestCase):
    """Test case for HMACAuth

    The tests in this test case use sample requests from
    https://docs.konghq.com/hub/kong-inc/hmac-auth/#hmac-example
    """

    def setUp(self):
        self.factory = RequestFactory()
        HMACGroupFactory(name="ltj_admin", permission_level=HMACGroup.ADMIN)
        HMACGroupFactory(name="ltj_virka_hki", permission_level=HMACGroup.OFFICE_HKI)
        HMACGroupFactory(name="ltj_virka", permission_level=HMACGroup.OFFICE)

    @freeze_time("2017-06-22 17:16:00")
    def test_is_valid_return_true_for_valid_request(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
            HTTP_PROXY_AUTHORIZATION=(
                "hmac "
                'username="alice123", '
                'algorithm="hmac-sha256", '
                'headers="date request-line", '
                'signature="ujWCGHeec9Xd6UD2zlyxiNMCiXnDOWeVFMu5VeRUxtw="'
            ),
        )
        hmac_auth = HMACAuth(request)
        self.assertTrue(hmac_auth.is_valid)

    @freeze_time("2017-06-22 20:00:00")
    def test_user_role_raise_permission_denied_if_out_of_clock_skew(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
            HTTP_PROXY_AUTHORIZATION=(
                "hmac "
                'username="alice123", '
                'algorithm="hmac-sha256", '
                'headers="date request-line", '
                'signature="ujWCGHeec9Xd6UD2zlyxiNMCiXnDOWeVFMu5VeRUxtw="'
            ),
        )
        hmac_auth = HMACAuth(request)
        with self.assertRaises(PermissionDenied):
            hmac_auth.user_role

    @freeze_time("2017-06-22 17:16:00")
    def test_user_role_raise_permission_denied_for_non_hmac_auth(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
            HTTP_PROXY_AUTHORIZATION=(
                "basic "
                'username="alice123", '
                'algorithm="hmac-sha256", '
                'headers="date request-line", '
                'signature="ujWCGHeec9Xd6UD2zlyxiNMCiXnDOWeVFMu5VeRUxtw="'
            ),
        )
        hmac_auth = HMACAuth(request)
        with self.assertRaises(PermissionDenied):
            hmac_auth.user_role

    @freeze_time("2017-06-22 17:16:00")
    def test_user_role_raise_permission_denied_if_using_wrong_headers(
        self,
    ):
        request = self.factory.get(
            "/test-url/",
            HTTP_HOST="hmac.com",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_PROXY_AUTHORIZATION=(
                "hmac "
                'username="alice123", '
                'algorithm="hmac-sha256", '
                'headers="date request-line", '
                'signature="ujWCGHeec9Xd6UD2zlyxiNMCiXnDOWeVFMu5VeRUxtw="'
            ),
        )
        hmac_auth = HMACAuth(request)
        with self.assertRaises(PermissionDenied):
            hmac_auth.user_role

    @freeze_time("2017-06-22 17:16:00")
    def test_user_role_raise_permission_denied_if_missing_required_credential_key(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
            HTTP_PROXY_AUTHORIZATION=(
                "hmac "
                'username="alice123", '
                'headers="date request-line", '
                'signature="ujWCGHeec9Xd6UD2zlyxiNMCiXnDOWeVFMu5VeRUxtw="'
            ),
        )
        hmac_auth = HMACAuth(request)
        with self.assertRaises(PermissionDenied):
            hmac_auth.user_role

    @freeze_time("2017-06-22 17:16:00")
    def test_user_role_raise_permission_denied_for_invalid_digest_algorithm(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
            HTTP_PROXY_AUTHORIZATION=(
                "hmac "
                'username="alice123", '
                'algorithm="hmac-not-exist", '
                'headers="date request-line", '
                'signature="ujWCGHeec9Xd6UD2zlyxiNMCiXnDOWeVFMu5VeRUxtw="'
            ),
        )
        hmac_auth = HMACAuth(request)
        with self.assertRaises(PermissionDenied):
            hmac_auth.user_role

    @freeze_time("2017-06-22 17:16:00")
    def test_user_role_raise_permission_denied_if_invalid_signature(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
            HTTP_PROXY_AUTHORIZATION=(
                "hmac "
                'username="alice123", '
                'algorithm="hmac-sha256", '
                'headers="date request-line", '
                'signature="invalid-signature"'
            ),
        )
        hmac_auth = HMACAuth(request)
        with self.assertRaises(PermissionDenied):
            hmac_auth.user_role

    def test_return_public_role_if_missing_auth_header(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
        )
        hmac_auth = HMACAuth(request)
        self.assertEqual(hmac_auth.user_role, UserRole.PUBLIC)

    @freeze_time("2017-06-22 17:16:00")
    def test_user_role_return_expected_user_role(self):
        group_roles = [
            ("ltj_admin", UserRole.ADMIN),
            ("ltj_virka_hki", UserRole.OFFICE_HKI),
            ("ltj_virka", UserRole.OFFICE),
        ]
        for group, expected_role in group_roles:
            request = self.factory.get(
                "/test-url/",
                HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
                HTTP_HOST="hmac.com",
                HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
                HTTP_PROXY_AUTHORIZATION=(
                    "hmac "
                    'username="alice123", '
                    'algorithm="hmac-sha256", '
                    'headers="date request-line", '
                    'signature="ujWCGHeec9Xd6UD2zlyxiNMCiXnDOWeVFMu5VeRUxtw="'
                ),
                HTTP_X_FORWARDED_GROUPS=group,
            )
            hmac_auth = HMACAuth(request)
            self.assertEqual(hmac_auth.user_role, expected_role)

    def test_user_role_raise_permission_denied_for_invalid_group(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
            HTTP_PROXY_AUTHORIZATION=(
                "hmac "
                'username="alice123", '
                'algorithm="hmac-sha256", '
                'headers="date request-line", '
                'signature="ujWCGHeec9Xd6UD2zlyxiNMCiXnDOWeVFMu5VeRUxtw="'
            ),
            HTTP_X_FORWARDED_GROUPS="invalid_group",
        )
        hmac_auth = HMACAuth(request)
        with self.assertRaises(PermissionDenied):
            hmac_auth.user_role
