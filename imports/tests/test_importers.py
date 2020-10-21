import datetime
from unittest.mock import patch

from django.conf import settings
from django.contrib.gis.geos import Point, Polygon
from django.test import TestCase

from nature.models import Feature
from nature.tests.factories import FeatureClassFactory, FeatureFactory
from .utils import (
    create_mock_zip_file_class,
    MockFeature,
    MockAttribute,
    create_mock_data_source,
)
from ..importers import ShapefileImporter, ImportValidationError

TEST_POINT = Point(10, 20, srid=settings.SRID)
TEST_POLYGON = Polygon([(0, 0), (20, 20), (20, 0), (0, 0)], srid=settings.SRID)

MOCK_FEATURE_1 = MockFeature(
    {
        "id": MockAttribute(1),
        "tunnus": MockAttribute("f-1"),
        "luokkatunn": MockAttribute("ABC"),
        "nimi": MockAttribute("feature 1"),
        "kuvaus": MockAttribute("feature 1 description"),
        "huom": MockAttribute("feature 1 notes"),
        "voimassa": MockAttribute("t"),
        "digipvm": MockAttribute(datetime.date(2020, 10, 1)),
        "numero": MockAttribute(1),
        "digitoija": MockAttribute("test creator"),
        "suojaustas": MockAttribute(3),
        "pvm_editoi": MockAttribute(None),
        "muokkaaja": MockAttribute(None),
        "pinta_ala": MockAttribute(20),
    },
    TEST_POINT.ogr,
)

MOCK_FEATURE_2 = MockFeature(
    {
        "id": MockAttribute(2),
        "tunnus": MockAttribute("f-2"),
        "luokkatunn": MockAttribute("ABC"),
        "nimi": MockAttribute("feature 2"),
        "kuvaus": MockAttribute("feature 2 description"),
        "huom": MockAttribute("feature 2 notes"),
        "voimassa": MockAttribute("t"),
        "digipvm": MockAttribute(datetime.date(2020, 11, 1)),
        "numero": MockAttribute(1),
        "digitoija": MockAttribute("test creator"),
        "suojaustas": MockAttribute(3),
        "pvm_editoi": MockAttribute(None),
        "muokkaaja": MockAttribute(None),
        "pinta_ala": MockAttribute(20),
    },
    TEST_POLYGON.ogr,
)

MOCK_FEATURE_WITH_INVALID_FIELD = MockFeature(
    {
        "id": MockAttribute(2),
        "tunnus": MockAttribute("f-2"),
        "luokkatunn": MockAttribute("ABC"),
        "nimi": MockAttribute("feature 2"),
        "kuvaus": MockAttribute("feature 2 description"),
        "huom": MockAttribute("feature 2 notes"),
        "voimassa": MockAttribute("t"),
        "digipvm": MockAttribute(datetime.date(2020, 11, 1)),
        "numero": MockAttribute(1),
        "digitoija": MockAttribute("test creator"),
        "suojaustas": MockAttribute(3),
        "pvm_editoi": MockAttribute(None),
        "muokkaaja": MockAttribute(None),
        "pinta_ala": MockAttribute(20),
        "an_invalid_field": MockAttribute(123),
    },
    TEST_POLYGON.ogr,
)

MOCK_FEATURE_WITH_INVALID_FEATURE_CLASS = MockFeature(
    {
        "id": MockAttribute(2),
        "tunnus": MockAttribute("f-2"),
        "luokkatunn": MockAttribute("INVALID-FEATURE-CLASS"),
        "nimi": MockAttribute("feature 2"),
        "kuvaus": MockAttribute("feature 2 description"),
        "huom": MockAttribute("feature 2 notes"),
        "voimassa": MockAttribute("t"),
        "digipvm": MockAttribute(datetime.date(2020, 11, 1)),
        "numero": MockAttribute(1),
        "digitoija": MockAttribute("test creator"),
        "suojaustas": MockAttribute(3),
        "pvm_editoi": MockAttribute(None),
        "muokkaaja": MockAttribute(None),
        "pinta_ala": MockAttribute(20),
    },
    TEST_POLYGON.ogr,
)


class TestShapefilesImporter(TestCase):
    def setUp(self):
        self.feature_class = FeatureClassFactory(id="ABC")
        self.feature_to_update = FeatureFactory(
            name="feature-to-update", feature_class=self.feature_class
        )

    @patch(
        "imports.importers.DataSource",
        create_mock_data_source([MOCK_FEATURE_1, MOCK_FEATURE_2]),
    )
    @patch(
        "imports.importers.zipfile.ZipFile",
        create_mock_zip_file_class(["test.shp", "test.shx", "test.dbf"]),
    )
    def test_import(self):
        # make sure only feature 1 exist before importing
        self.assertQuerysetEqual(Feature.objects.all(), [repr(self.feature_to_update)])
        ShapefileImporter.import_features("dummy-shapefiles.zip")
        # verify new feature created
        self.assertEqual(Feature.objects.count(), 2)
        # verify existing feature updated
        self.feature_to_update.refresh_from_db()
        self.assertEqual(self.feature_to_update.name, "feature 1")

    @patch(
        "imports.importers.DataSource",
        create_mock_data_source([MOCK_FEATURE_WITH_INVALID_FIELD]),
    )
    @patch(
        "imports.importers.zipfile.ZipFile",
        create_mock_zip_file_class(["test.shp", "test.shx", "test.dbf"]),
    )
    def test_raise_import_validation_error_if_layer_contains_invalid_fields(self):
        with self.assertRaises(ImportValidationError) as context:
            ShapefileImporter.import_features("dummy-shapefiles.zip")
        self.assertEqual(context.exception.code, "fields_not_allowed")

    @patch(
        "imports.importers.DataSource",
        create_mock_data_source([MOCK_FEATURE_WITH_INVALID_FEATURE_CLASS]),
    )
    @patch(
        "imports.importers.zipfile.ZipFile",
        create_mock_zip_file_class(["test.shp", "test.shx", "test.dbf"]),
    )
    def test_raise_import_validation_error_if_layer_contains_invalid_feature_classes(
        self,
    ):
        with self.assertRaises(ImportValidationError) as context:
            ShapefileImporter.import_features("dummy-shapefiles.zip")
        self.assertEqual(context.exception.code, "feature_classes_not_exist")
