from unittest.mock import MagicMock, patch

from django.http import QueryDict
from django.test import Client, TestCase, RequestFactory, override_settings
from django.urls import reverse

from nature.tests.factories import (
    FeatureClassFactory, ObservationFactory, FeatureFactory,
    ObservationSeriesFactory, HabitatTypeObservationFactory,
    SpeciesRegulationFactory,
    SpeciesFactory)
from nature.tests.utils import make_user
from ..views import FeatureWFSView, SpeciesReportView, FeatureObservationsReportView


class TestProtectedReportViewMixin(TestCase):

    def setUp(self):
        feature_class_open_data = FeatureClassFactory(open_data=True)
        feature_class_non_open_data = FeatureClassFactory(open_data=False)
        self.feature_open_data = FeatureFactory(feature_class=feature_class_open_data)
        self.feature_non_open_data = FeatureFactory(feature_class=feature_class_non_open_data)
        self.admin = make_user(username='test_admin', is_admin=True)
        self.user = make_user(username='test_user', is_admin=False)

    def test_admin_access_report_non_open_data_success(self):
        url = reverse('nature:feature-report', kwargs={'pk': self.feature_non_open_data.id})
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_report_open_data_success(self):
        url = reverse('nature:feature-report', kwargs={'pk': self.feature_open_data.id})
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_access_report_non_open_data_not_found(self):
        url = reverse('nature:feature-report', kwargs={'pk': self.feature_non_open_data.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_access_report_open_data_success(self):
        url = reverse('nature:feature-report', kwargs={'pk': self.feature_open_data.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_access_report_non_open_data_not_found(self):
        url = reverse('nature:feature-report', kwargs={'pk': self.feature_non_open_data.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_access_report_open_data_success(self):
        url = reverse('nature:feature-report', kwargs={'pk': self.feature_open_data.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class MockResponse:

    def __init__(self, content, content_type, status_code):
        self.content = content
        self.status_code = status_code
        self.headers = {'content-type': content_type}


@patch('requests.get', MagicMock(side_effect=lambda url: MockResponse(b'abc', 'application/xml', 400)))
class TestFeatureWFSView(TestCase):

    @property
    def test_wfs_url(self):
        query_dict = QueryDict(mutable=True)
        query_dict.update({
            'service': 'WFS',
            'version': '1.1.0',
            'typeName': 'test-feature',
            'outputFormat': 'application/json',
            'srsname': 'EPSG:3879',
            'bbox': '0,1,2,3,EPSG:3879'
        })
        return '{0}?{1}'.format(reverse('nature:wfs'), query_dict.urlencode())

    def setUp(self):
        self.user = make_user()
        self.view = FeatureWFSView()
        factory = RequestFactory()
        self.request = factory.get(self.test_wfs_url)
        self.view.request = self.request

    def test_get(self):
        response = self.view.get(self.request)
        self.assertEqual(response.content, b'abc')
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertEqual(response.status_code, 400)

    @override_settings(
        WFS_SERVER_URL='http://testserver/',
        WFS_NAMESPACE='test-namespace',
    )
    def test_get_wfs_url(self):
        FeatureClassFactory(id='FC-ID-1')
        FeatureClassFactory(id='FC-ID-2')

        wfs_url = self.view._get_wfs_url()
        server_url, query_string = wfs_url.split('?')
        self.assertEqual(server_url, 'http://testserver/')

        query_dict = QueryDict(query_string)
        expected_dict = {
            'service': 'WFS',
            'version': '1.1.0',
            'typeName': 'test-namespace:test-feature',
            'outputFormat': 'application/json',
            'srsname': 'EPSG:3879',
            'bbox': '0,1,2,3,EPSG:3879'
        }
        self.assertEqual(query_dict.dict(), expected_dict)


class TestSpeciesReportView(TestCase):

    def setUp(self):
        self.species = SpeciesFactory()
        feature_class = FeatureClassFactory(open_data=False)
        feature = FeatureFactory(feature_class=feature_class)
        self.observation = ObservationFactory(feature=feature, species=self.species)

        feature_class_open_data = FeatureClassFactory(open_data=True)
        feature_open_data = FeatureFactory(feature_class=feature_class_open_data)
        self.observation_open_data = ObservationFactory(feature=feature_open_data, species=self.species)

        self.view = SpeciesReportView()
        factory = RequestFactory()
        view_kwargs = {'pk': self.species.pk}
        self.request = factory.get(reverse('nature:species-report', kwargs=view_kwargs))

    def test_get_context_data_for_staff(self):
        self.request.user = make_user(is_admin=True)
        self.view.request = self.request
        self.view.object = self.species
        context = self.view.get_context_data()
        self.assertQuerysetEqual(
            context['observations'],
            [repr(self.observation), repr(self.observation_open_data)],
            ordered=False,
        )

    def test_get_context_data_for_non_staff(self):
        self.request.user = make_user(is_admin=False)
        self.view.request = self.request
        self.view.object = self.species
        context = self.view.get_context_data()
        self.assertQuerysetEqual(
            context['observations'],
            [repr(self.observation_open_data)],
            ordered=False,
        )


class TestFeatureObservationsReportView(TestCase):

    def setUp(self):
        self.feature = FeatureFactory()
        self.view = FeatureObservationsReportView()
        self.factory = RequestFactory()

    def test_get_content_data(self):
        request = self.factory.get(reverse('nature:feature-observations-report', kwargs={'pk': self.feature.id}))
        request.user = make_user()
        self.view.request = request
        self.view.object = self.feature
        context_data = self.view.get_context_data()
        self.assertEqual(list(context_data['feature_observations'].query.order_by), ['species__name_fi'])


class TestReportViews(TestCase):
    """
    TestCase that verifies that report views can be rendered correctly
    """
    def setUp(self):
        self.client = Client()

    def test_feature_report(self):
        feature = FeatureFactory()
        url = reverse('nature:feature-report', kwargs={'pk': feature.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_observationseries_report(self):
        observation_series = ObservationSeriesFactory()
        url = reverse('nature:observationseries-report', kwargs={'pk': observation_series.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_feature_observations_report(self):
        feature = FeatureFactory()
        ObservationFactory(feature=feature)
        url = reverse('nature:feature-observations-report', kwargs={'pk': feature.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_feature_habitattypeobservations_report(self):
        feature = FeatureFactory()
        HabitatTypeObservationFactory(feature=feature)
        url = reverse('nature:feature-habitattypeobservations-report', kwargs={'pk': feature.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_species_report(self):
        species_regulation = SpeciesRegulationFactory()
        url = reverse('nature:species-report', kwargs={'pk': species_regulation.species_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_species_regulations_report(self):
        species_regulation = SpeciesRegulationFactory()
        url = reverse('nature:species-regulations-report', kwargs={'pk': species_regulation.species_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_observation_report(self):
        observation = ObservationFactory()
        url = reverse('nature:observation-report', kwargs={'pk': observation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
