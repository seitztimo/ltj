import os
from unittest.mock import patch

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

    @patch('imports.admin.messages.add_message')
    @patch('imports.importers.ShapefileImporter.import_features')
    def test_save_model(self, mock_import, mock_add_message):
        shp_import_admin = ShapefileImportAdmin(ShapefileImport, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        shp_import = ShapefileImportFactory.build()
        shp_import_admin.save_model(request, shp_import, None, None)
        self.assertEqual(shp_import.created_by, self.user)
        mock_import.assert_called_once_with(shp_import.shapefiles)
        mock_add_message.assert_called()

        os.remove(shp_import.shapefiles.path)
