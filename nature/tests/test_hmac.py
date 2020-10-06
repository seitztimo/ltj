from django.test import TestCase, RequestFactory, override_settings
from freezegun import freeze_time

from nature.hmac import HMACAuth, InvalidAuthorization


@override_settings(SHARED_SECRET="secret")
class TestHMACAuth(TestCase):
    """Test case for HMACAuth

    The tests in this test case use sample requests from
    https://docs.konghq.com/hub/kong-inc/hmac-auth/#hmac-example
    """

    def setUp(self):
        self.factory = RequestFactory()

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
    def test_out_of_clock_skew_raises_exception(self):
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
        with self.assertRaises(InvalidAuthorization):
            hmac_auth.within_clock_skew

    @freeze_time("2017-06-22 17:16:00")
    def test_is_valid_raises_exception_for_non_hmac_auth(self):
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
        with self.assertRaises(InvalidAuthorization):
            hmac_auth.is_valid

    @freeze_time("2017-06-22 17:16:00")
    def test_is_valid_return_false_if_missing_auth_header(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_DATE="Thu, 22 Jun 2017 17:15:21 GMT",
            HTTP_HOST="hmac.com",
            HTTP_REQUEST_LINE="GET /requests HTTP/1.1",
        )
        hmac_auth = HMACAuth(request)
        self.assertFalse(hmac_auth.is_valid)

    @freeze_time("2017-06-22 17:16:00")
    def test_is_valid_raises_exception_if_missing_header_used_in_credentials(self):
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
        with self.assertRaises(InvalidAuthorization):
            hmac_auth.is_valid

    @freeze_time("2017-06-22 17:16:00")
    def test_is_valid_raises_exception_if_missing_required_credential_key(self):
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
        with self.assertRaises(InvalidAuthorization):
            hmac_auth.is_valid

    @freeze_time("2017-06-22 17:16:00")
    def test_is_valid_return_false_for_invalid_digest_algorithm(self):
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
        self.assertFalse(hmac_auth.is_valid)

    @freeze_time("2017-06-22 17:16:00")
    def test_is_valid_return_false_if_invalid_signature(self):
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
        self.assertFalse(hmac_auth.is_valid)

    def test_has_auth_group_return_true(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_X_FORWARDED_GROUPS="ltj_admin;ltj_virka_hki;ltj_virka",
        )
        hmac_auth = HMACAuth(request)
        hmac_auth._is_valid = True
        self.assertTrue(hmac_auth.has_admin_group)
        self.assertTrue(hmac_auth.has_office_hki_group)
        self.assertTrue(hmac_auth.has_office_group)

    def test_has_auth_group_return_false(self):
        request = self.factory.get(
            "/test-url/",
            HTTP_X_FORWARDED_GROUPS="",
        )
        hmac_auth = HMACAuth(request)
        hmac_auth._is_valid = True
        self.assertFalse(hmac_auth.has_admin_group)
        self.assertFalse(hmac_auth.has_office_hki_group)
        self.assertFalse(hmac_auth.has_office_group)
