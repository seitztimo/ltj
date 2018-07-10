from unittest.mock import MagicMock, patch

from django.http import QueryDict
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse

from nature.tests.factories import FeatureClassFactory, ObservationFactory
from nature.tests.utils import make_user
from ..views import FeatureWFSView, SpeciesReportView


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
        self.observation = ObservationFactory()
        self.species = self.observation.species
        self.feature_class = self.observation.feature.feature_class

        self.view = SpeciesReportView()
        factory = RequestFactory()
        view_kwargs = {'pk': self.species.pk}
        self.request = factory.get(reverse('nature:species-report', kwargs=view_kwargs))
        self.view.request = self.request
        self.view.kwargs = view_kwargs

    def test_get_context_data(self):
        self.view.get(self.request)
        context = self.view.get_context_data()
        self.assertEqual(len(context['feature_classes']), 1)
        self.assertTrue(context['feature_classes'][self.feature_class.id])
        self.assertEqual(
            context['feature_classes'][self.feature_class.id],
            {
                'name': self.feature_class.name,
                'observations': [self.observation]
            }
        )
