from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory


from .factories import FeatureFactory
from ..admin import FeatureAdmin
from ..models import Feature


class TestFeatureAdmin(TestCase):

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create(username='testuser', is_staff=True)
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

