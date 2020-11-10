from unittest.mock import MagicMock, patch, PropertyMock

from django.contrib.auth.models import AnonymousUser
from django.http import QueryDict
from django.test import Client, TestCase, RequestFactory, override_settings
from django.urls import reverse
from django.utils.translation import activate
from freezegun import freeze_time

from hmac_auth.models import HMACGroup
from hmac_auth.tests.factories import HMACGroupFactory
from nature.models import PROTECTION_LEVELS, OFFICE_HKI_ONLY_FEATURE_CLASS_ID
from nature.tests.factories import (
    FeatureClassFactory,
    ObservationFactory,
    FeatureFactory,
    ObservationSeriesFactory,
    HabitatTypeObservationFactory,
    SpeciesRegulationFactory,
    SpeciesFactory,
)
from nature.tests.utils import make_user
from ..enums import UserRole
from ..views import FeatureWFSView, SpeciesReportView, FeatureObservationsReportView


@override_settings(SHARED_SECRET="test-secret-key", ALLOWED_HOSTS=["localhost"])
class TestFeatureReportHMACAuth(TestCase):
    def setUp(self):
        activate("fi")
        HMACGroupFactory(name="ltj_admin", permission_level=HMACGroup.ADMIN)
        HMACGroupFactory(name="ltj_virka_hki", permission_level=HMACGroup.OFFICE_HKI)
        HMACGroupFactory(name="ltj_virka", permission_level=HMACGroup.OFFICE)

        feature_class_office_hki = FeatureClassFactory(
            id=OFFICE_HKI_ONLY_FEATURE_CLASS_ID
        )
        self.feature_admin = FeatureFactory(protection_level=PROTECTION_LEVELS["ADMIN"])
        self.feature_office_hki = FeatureFactory(
            protection_level=PROTECTION_LEVELS["OFFICE"],
            feature_class=feature_class_office_hki,
        )
        self.feature_office = FeatureFactory(
            protection_level=PROTECTION_LEVELS["OFFICE"]
        )
        self.feature_public = FeatureFactory(
            protection_level=PROTECTION_LEVELS["PUBLIC"]
        )

    @freeze_time("2019-01-17 12:00:00")
    def test_hmac_admin_group_can_access_all_reports(self):
        headers = {
            "HTTP_HOST": "localhost",
            "HTTP_DATE": "Fri, 17 Jan 2019 12:00:00 GMT",
            "HTTP_REQUEST_LINE": "GET /test-path HTTP/1.1",
            "HTTP_X_FORWARDED_GROUPS": "ltj_admin",
            "HTTP_PROXY_AUTHORIZATION": (
                "hmac "
                'username="ltj", '
                'algorithm="hmac-sha256", '
                'headers="host date request-line x-forwarded-groups", '
                'signature="IxMslVab+oyOZwloianoQDsV5WkzPYlzWgyEbvybGGU="'
            ),
        }

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_admin.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Admin</title>".encode("utf-8"), response.content
        )

        url = reverse(
            "nature:feature-report", kwargs={"pk": self.feature_office_hki.id}
        )
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Admin</title>".encode("utf-8"), response.content
        )

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_office.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Admin</title>".encode("utf-8"), response.content
        )

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_public.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Admin</title>".encode("utf-8"), response.content
        )

    @freeze_time("2019-01-17 12:00:00")
    def test_hmac_office_hki_group_can_access_non_admin_reports(self):
        headers = {
            "HTTP_HOST": "localhost",
            "HTTP_DATE": "Fri, 17 Jan 2019 12:00:00 GMT",
            "HTTP_REQUEST_LINE": "GET /test-path HTTP/1.1",
            "HTTP_X_FORWARDED_GROUPS": "ltj_virka_hki",
            "HTTP_PROXY_AUTHORIZATION": (
                "hmac "
                'username="ltj", '
                'algorithm="hmac-sha256", '
                'headers="host date request-line x-forwarded-groups", '
                'signature="TWu+GOyJipcU0yI+P+baZjJlxRf15bjR6aLBGp4qgEc="'
            ),
        }

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_admin.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 404)

        url = reverse(
            "nature:feature-report", kwargs={"pk": self.feature_office_hki.id}
        )
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Virka Hki</title>".encode("utf-8"), response.content
        )

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_office.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Virka Hki</title>".encode("utf-8"), response.content
        )

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_public.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Virka Hki</title>".encode("utf-8"), response.content
        )

    @freeze_time("2019-01-17 12:00:00")
    def test_hmac_office_group_can_access_office_and_public_reports(self):
        headers = {
            "HTTP_HOST": "localhost",
            "HTTP_DATE": "Fri, 17 Jan 2019 12:00:00 GMT",
            "HTTP_REQUEST_LINE": "GET /test-path HTTP/1.1",
            "HTTP_X_FORWARDED_GROUPS": "ltj_virka",
            "HTTP_PROXY_AUTHORIZATION": (
                "hmac "
                'username="ltj", '
                'algorithm="hmac-sha256", '
                'headers="host date request-line x-forwarded-groups", '
                'signature="QnEwM4vSpaCwFFIqFfTXrA29+JM9vhV3F2qvwERZxsk="'
            ),
        }

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_admin.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 404)

        url = reverse(
            "nature:feature-report", kwargs={"pk": self.feature_office_hki.id}
        )
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 404)

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_office.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Virka</title>".encode("utf-8"), response.content
        )

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_public.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Virka</title>".encode("utf-8"), response.content
        )

    @freeze_time("2019-01-17 12:00:00")
    def test_request_without_auth_header_can_access_public_reports(self):
        headers = {
            "HTTP_HOST": "localhost",
            "HTTP_DATE": "Fri, 17 Jan 2019 12:00:00 GMT",
            "HTTP_REQUEST_LINE": "GET /test-path HTTP/1.1",
        }

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_admin.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 404)

        url = reverse(
            "nature:feature-report", kwargs={"pk": self.feature_office_hki.id}
        )
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 404)

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_office.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 404)

        url = reverse("nature:feature-report", kwargs={"pk": self.feature_public.id})
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<title>Kohderaportti - Yleisö</title>".encode("utf-8"), response.content
        )


class TestProtectedReportViewMixin(TestCase):
    def setUp(self):
        feature_class_www = FeatureClassFactory(www=True)
        feature_class_non_www = FeatureClassFactory(www=False)
        self.feature_www = FeatureFactory(feature_class=feature_class_www)
        self.feature_non_www = FeatureFactory(feature_class=feature_class_non_www)
        self.admin = make_user(username="test_admin", is_admin=True)
        self.user = make_user(username="test_user", is_admin=False)

    def test_admin_access_report_non_www_success(self):
        url = reverse("nature:feature-report", kwargs={"pk": self.feature_non_www.id})
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_report_www_success(self):
        url = reverse("nature:feature-report", kwargs={"pk": self.feature_www.id})
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_access_report_non_www_not_found(self):
        url = reverse("nature:feature-report", kwargs={"pk": self.feature_non_www.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_access_report_www_success(self):
        url = reverse("nature:feature-report", kwargs={"pk": self.feature_www.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_access_report_non_www_not_found(self):
        url = reverse("nature:feature-report", kwargs={"pk": self.feature_non_www.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_access_report_www_success(self):
        url = reverse("nature:feature-report", kwargs={"pk": self.feature_www.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class MockResponse:
    def __init__(self, content, content_type, status_code):
        self.content = content
        self.status_code = status_code
        self.headers = {"content-type": content_type}


@patch(
    "requests.get",
    MagicMock(side_effect=lambda url: MockResponse(b"abc", "application/xml", 400)),
)
class TestFeatureWFSView(TestCase):
    @property
    def test_wfs_url(self):
        query_dict = QueryDict(mutable=True)
        query_dict.update(
            {
                "service": "WFS",
                "version": "1.1.0",
                "typeName": "test-feature",
                "outputFormat": "application/json",
                "srsname": "EPSG:3879",
                "bbox": "0,1,2,3,EPSG:3879",
            }
        )
        return "{0}?{1}".format(reverse("nature:wfs"), query_dict.urlencode())

    def setUp(self):
        self.user = make_user()
        self.view = FeatureWFSView()
        factory = RequestFactory()
        self.request = factory.get(self.test_wfs_url)
        self.view.request = self.request

    def test_get(self):
        response = self.view.get(self.request)
        self.assertEqual(response.content, b"abc")
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertEqual(response.status_code, 400)

    @override_settings(
        WFS_SERVER_URL="http://testserver/",
        WFS_NAMESPACE="test-namespace",
    )
    def test_get_wfs_url(self):
        FeatureClassFactory(id="FC-ID-1")
        FeatureClassFactory(id="FC-ID-2")

        wfs_url = self.view._get_wfs_url()
        server_url, query_string = wfs_url.split("?")
        self.assertEqual(server_url, "http://testserver/")

        query_dict = QueryDict(query_string)
        expected_dict = {
            "service": "WFS",
            "version": "1.1.0",
            "typeName": "test-namespace:test-feature",
            "outputFormat": "application/json",
            "srsname": "EPSG:3879",
            "bbox": "0,1,2,3,EPSG:3879",
        }
        self.assertEqual(query_dict.dict(), expected_dict)


class TestSpeciesReportView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.species = SpeciesFactory()
        feature_class = FeatureClassFactory(www=False)
        feature_class_www = FeatureClassFactory(www=True)
        feature_class_office_hki = FeatureClassFactory(
            id=OFFICE_HKI_ONLY_FEATURE_CLASS_ID, www=False
        )
        feature_admin = FeatureFactory(
            feature_class=feature_class,
            protection_level=PROTECTION_LEVELS["ADMIN"],
        )
        feature_office_hki = FeatureFactory(
            feature_class=feature_class_office_hki,
            protection_level=PROTECTION_LEVELS["OFFICE"],
        )
        feature_office = FeatureFactory(
            feature_class=feature_class,
            protection_level=PROTECTION_LEVELS["OFFICE"],
        )
        feature_www = FeatureFactory(
            feature_class=feature_class_www,
            protection_level=PROTECTION_LEVELS["PUBLIC"],
        )

        self.observation_admin = ObservationFactory(
            protection_level=PROTECTION_LEVELS["ADMIN"],
            feature=feature_admin,
            species=self.species,
        )
        self.observation_office_hki = ObservationFactory(
            protection_level=PROTECTION_LEVELS["OFFICE"],
            feature=feature_office_hki,
            species=self.species,
        )
        self.observation_office = ObservationFactory(
            protection_level=PROTECTION_LEVELS["OFFICE"],
            feature=feature_office,
            species=self.species,
        )
        self.observation_www = ObservationFactory(
            protection_level=PROTECTION_LEVELS["PUBLIC"],
            feature=feature_www,
            species=self.species,
        )

    @patch(
        "nature.views.HMACAuth.user_role",
        new_callable=PropertyMock(return_value=UserRole.ADMIN),
    )
    def test_get_context_data_for_admin(self, *args):
        view = SpeciesReportView()
        view_kwargs = {"pk": self.species.pk}
        request = self.factory.get(reverse("nature:species-report", kwargs=view_kwargs))
        request.user = AnonymousUser()
        view.request = request
        view.object = self.species

        context = view.get_context_data()
        self.assertQuerysetEqual(
            context["observations"],
            [
                repr(self.observation_admin),
                repr(self.observation_office_hki),
                repr(self.observation_office),
                repr(self.observation_www),
            ],
            ordered=False,
        )
        self.assertEqual(context["secret_observation_count"], 0)

    @patch(
        "nature.views.HMACAuth.user_role",
        new_callable=PropertyMock(return_value=UserRole.OFFICE_HKI),
    )
    def test_get_context_data_for_office_hki(self, *args):
        view = SpeciesReportView()
        view_kwargs = {"pk": self.species.pk}
        request = self.factory.get(reverse("nature:species-report", kwargs=view_kwargs))
        request.user = AnonymousUser()
        view.request = request
        view.object = self.species

        context = view.get_context_data()
        self.assertQuerysetEqual(
            context["observations"],
            [
                repr(self.observation_office_hki),
                repr(self.observation_office),
                repr(self.observation_www),
            ],
            ordered=False,
        )
        self.assertEqual(context["secret_observation_count"], 1)

    @patch(
        "nature.views.HMACAuth.user_role",
        new_callable=PropertyMock(return_value=UserRole.OFFICE),
    )
    def test_get_context_data_for_office(self, *args):
        view = SpeciesReportView()
        view_kwargs = {"pk": self.species.pk}
        request = self.factory.get(reverse("nature:species-report", kwargs=view_kwargs))
        request.user = AnonymousUser()
        view.request = request
        view.object = self.species

        context = view.get_context_data()
        self.assertQuerysetEqual(
            context["observations"],
            [repr(self.observation_office), repr(self.observation_www)],
            ordered=False,
        )
        self.assertEqual(context["secret_observation_count"], 2)

    @patch(
        "nature.views.HMACAuth.user_role",
        new_callable=PropertyMock(return_value=UserRole.PUBLIC),
    )
    def test_get_context_data_for_public_www(self, *args):
        view = SpeciesReportView()
        view_kwargs = {"pk": self.species.pk}
        request = self.factory.get(reverse("nature:species-report", kwargs=view_kwargs))
        request.user = AnonymousUser()
        view.request = request
        view.object = self.species

        context = view.get_context_data()
        self.assertQuerysetEqual(
            context["observations"],
            [repr(self.observation_www)],
        )
        self.assertEqual(context["secret_observation_count"], 0)


class TestFeatureObservationsReportView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        feature_class = FeatureClassFactory(www=True)
        self.feature = FeatureFactory(
            feature_class=feature_class,
            protection_level=PROTECTION_LEVELS["PUBLIC"],
        )
        self.observation_admin = ObservationFactory(
            protection_level=PROTECTION_LEVELS["ADMIN"],
            feature=self.feature,
        )
        self.observation_office = ObservationFactory(
            protection_level=PROTECTION_LEVELS["OFFICE"],
            feature=self.feature,
        )
        self.observation_www = ObservationFactory(
            protection_level=PROTECTION_LEVELS["PUBLIC"],
            feature=self.feature,
        )

    @patch(
        "nature.views.HMACAuth.user_role",
        new_callable=PropertyMock(return_value=UserRole.ADMIN),
    )
    def test_get_context_data_for_admin(self, *args):
        view = FeatureObservationsReportView()
        view_kwargs = {"pk": self.feature.pk}
        request = self.factory.get(
            reverse("nature:feature-observations-report", kwargs=view_kwargs)
        )
        request.user = AnonymousUser()
        view.request = request
        view.object = self.feature

        context = view.get_context_data()
        self.assertQuerysetEqual(
            context["observations"],
            [
                repr(self.observation_admin),
                repr(self.observation_office),
                repr(self.observation_www),
            ],
            ordered=False,
        )
        self.assertEqual(context["secret_observation_count"], 0)

    @patch(
        "nature.views.HMACAuth.user_role",
        new_callable=PropertyMock(return_value=UserRole.OFFICE_HKI),
    )
    def test_get_context_data_for_office_hki(self, *args):
        view = FeatureObservationsReportView()
        view_kwargs = {"pk": self.feature.pk}
        request = self.factory.get(
            reverse("nature:feature-observations-report", kwargs=view_kwargs)
        )
        request.user = AnonymousUser()
        view.request = request
        view.object = self.feature

        context = view.get_context_data()
        self.assertQuerysetEqual(
            context["observations"],
            [repr(self.observation_office), repr(self.observation_www)],
            ordered=False,
        )
        self.assertEqual(context["secret_observation_count"], 1)

    @patch(
        "nature.views.HMACAuth.user_role",
        new_callable=PropertyMock(return_value=UserRole.OFFICE),
    )
    def test_get_context_data_for_office(self, *args):
        view = FeatureObservationsReportView()
        view_kwargs = {"pk": self.feature.pk}
        request = self.factory.get(
            reverse("nature:feature-observations-report", kwargs=view_kwargs)
        )
        request.user = AnonymousUser()
        view.request = request
        view.object = self.feature

        context = view.get_context_data()
        self.assertQuerysetEqual(
            context["observations"],
            [repr(self.observation_office), repr(self.observation_www)],
            ordered=False,
        )
        self.assertEqual(context["secret_observation_count"], 1)

    @patch(
        "nature.views.HMACAuth.user_role",
        new_callable=PropertyMock(return_value=UserRole.PUBLIC),
    )
    def test_get_context_data_for_public_www(self, *args):
        view = FeatureObservationsReportView()
        view_kwargs = {"pk": self.feature.pk}
        request = self.factory.get(
            reverse("nature:feature-observations-report", kwargs=view_kwargs)
        )
        request.user = AnonymousUser()
        view.request = request
        view.object = self.feature

        context = view.get_context_data()
        self.assertQuerysetEqual(
            context["observations"],
            [repr(self.observation_www)],
            ordered=False,
        )
        self.assertEqual(context["secret_observation_count"], 0)


class TestReportViews(TestCase):
    """
    TestCase that verifies that report views can be rendered correctly
    """

    def setUp(self):
        self.client = Client()

    def test_feature_report(self):
        feature = FeatureFactory()
        url = reverse("nature:feature-report", kwargs={"pk": feature.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_observationseries_report(self):
        observation_series = ObservationSeriesFactory()
        url = reverse(
            "nature:observationseries-report", kwargs={"pk": observation_series.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_feature_observations_report(self):
        feature = FeatureFactory()
        ObservationFactory(feature=feature)
        url = reverse("nature:feature-observations-report", kwargs={"pk": feature.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_feature_habitattypeobservations_report(self):
        feature = FeatureFactory()
        HabitatTypeObservationFactory(feature=feature)
        url = reverse(
            "nature:feature-habitattypeobservations-report", kwargs={"pk": feature.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_species_report(self):
        species_regulation = SpeciesRegulationFactory()
        url = reverse(
            "nature:species-report", kwargs={"pk": species_regulation.species_id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_species_regulations_report(self):
        species_regulation = SpeciesRegulationFactory()
        url = reverse(
            "nature:species-regulations-report",
            kwargs={"pk": species_regulation.species_id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_observation_report(self):
        observation = ObservationFactory()
        url = reverse("nature:observation-report", kwargs={"pk": observation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
