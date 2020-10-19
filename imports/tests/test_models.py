import os

from django.test import TestCase

from .factories import ShapefileImportFactory


class TestShapefileImport(TestCase):
    def setUp(self):
        self.shp_import = ShapefileImportFactory()

    def tearDown(self):
        os.remove(self.shp_import.shapefiles.path)

    def test__str__(self):
        self.assertTrue(str(self.shp_import).startswith("shapefiles/testshapefiles"))
