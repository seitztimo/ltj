import os

from django.contrib.admin import AdminSite
from django.test import TestCase, RequestFactory

from nature.tests.utils import make_user
from .factories import ShapefileImportFactory
from ..admin import ShapefileImportAdmin
from ..models import ShapefileImport


class TestShapefileImportAdmin(TestCase):

    def setUp(self):
        self.user = make_user()
        self.site = AdminSite()
        self.factory = RequestFactory()

    def test_save_model(self):
        shp_import_admin = ShapefileImportAdmin(ShapefileImport, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        shp_import = ShapefileImportFactory.build()
        shp_import_admin.save_model(request, shp_import, None, None)
        self.assertEqual(shp_import.created_by, self.user)

        os.remove(shp_import.shapefiles.path)
