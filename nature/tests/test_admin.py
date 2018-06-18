from unittest.mock import patch, MagicMock

from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory

from .factories import FeatureFactory, ObservationFactory, PublicationFactory
from .utils import make_user
from ..admin import FeatureAdmin, ObservationInline, PublicationAdmin, ProtectionInline, SquareInline
from ..models import Feature, Publication


class TestObservationInline(TestCase):

    def setUp(self):
        self.user = make_user()
        self.site = AdminSite()
        self.factory = RequestFactory()

        feature = FeatureFactory()
        self.observation = ObservationFactory(feature=feature)

    def test_get_queryset(self):
        observation_inline = ObservationInline(Feature, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        # test select_related is used
        observation = observation_inline.get_queryset(request).first()
        self.assertNumQueries(0, getattr, observation, 'species')
        self.assertNumQueries(0, getattr, observation, 'series')


class TestFeatureAdmin(TestCase):

    def setUp(self):
        self.user = make_user()
        self.feature = FeatureFactory()
        self.site = AdminSite()
        self.factory = RequestFactory()

    def test_get_queryset(self):
        fa = FeatureAdmin(Feature, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        # test select_related is used
        feature = fa.get_queryset(request).first()
        self.assertNumQueries(0, getattr, feature, 'feature_class')

    def test_save_model(self):
        fa = FeatureAdmin(Feature, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        feature = FeatureFactory.build(feature_class=self.feature.feature_class)
        fa.save_model(request, feature, None, None)
        self.assertEqual(feature.created_by, 'testuser')
        self.assertEqual(feature.last_modified_by, 'testuser')

        feature = FeatureFactory(created_by='otheruser')
        fa.save_model(request, feature, None, None)
        self.assertEqual(feature.created_by, 'otheruser')
        self.assertEqual(feature.last_modified_by, 'testuser')

    def test_inline_instances_include_protection_inline_if_feature_is_protected(self):
        fa = FeatureAdmin(Feature, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        with patch('nature.models.Feature.is_protected', new_callable=MagicMock(return_value=True)):
            feature = FeatureFactory()
            inline_instances = fa.get_inline_instances(request, feature)
            self.assertTrue(isinstance(inline_instances[-1], ProtectionInline))

    def test_inline_instances_include_square_inline_if_feature_is_square(self):
        fa = FeatureAdmin(Feature, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        with patch('nature.models.Feature.is_square', new_callable=MagicMock(return_value=True)):
            feature = FeatureFactory()
            inline_instances = fa.get_inline_instances(request, feature)
            self.assertTrue(isinstance(inline_instances[-1], SquareInline))

    def test_no_additional_inline_instances_for_normal_feature(self):
        fa = FeatureAdmin(Feature, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        feature = FeatureFactory()
        inline_instances = fa.get_inline_instances(request, feature)
        self.assertFalse(isinstance(inline_instances[-1], (ProtectionInline, SquareInline)))

    def test_no_additional_inline_instances_on_add(self):
        fa = FeatureAdmin(Feature, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        inline_instances = fa.get_inline_instances(request)
        self.assertFalse(isinstance(inline_instances[-1], (ProtectionInline, SquareInline)))


class TestPublicationAdmin(TestCase):

    def setUp(self):
        self.user = make_user()
        self.publication = PublicationFactory()
        self.site = AdminSite()
        self.factory = RequestFactory()

    def test_get_queryset(self):
        pa = PublicationAdmin(Publication, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        # test select_related is used
        publication = pa.get_queryset(request).first()
        self.assertNumQueries(0, getattr, publication, 'publication_type')
