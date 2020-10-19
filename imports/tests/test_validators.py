from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import ShapefileImportFactory
from .utils import create_mock_zip_file_class
from ..validators import ZippedShapefilesValidator


class TestValidateZippedShapefiles(TestCase):
    def setUp(self):
        self.validator = ZippedShapefilesValidator()

    @patch(
        "imports.validators.zipfile.ZipFile",
        create_mock_zip_file_class(["test.shp", "test.shx", "test.dbf"]),
    )
    @patch("imports.validators.zipfile.is_zipfile", return_value=True)
    def test_not_raise_validation_error_for_valid_zipped_shapefiles(
        self, mock_is_zipfile
    ):
        shp_import = ShapefileImportFactory.build()
        try:
            self.validator(shp_import.shapefiles)
        except ValidationError:
            self.fail("Should not raise ValidationError for valid zipped shapefiles")

    @patch("imports.validators.zipfile.is_zipfile", return_value=False)
    def test_raise_validation_error_for_invalid_zip_file(self, mock_is_zipfile):
        shp_import = ShapefileImportFactory.build()
        with self.assertRaises(ValidationError) as context:
            self.validator(shp_import.shapefiles)
        self.assertEqual(context.exception.code, "invalid_zipfile")

    @patch(
        "imports.validators.zipfile.ZipFile",
        create_mock_zip_file_class(["test.shp", "test.shx", "abc.dbf"]),
    )
    @patch("imports.validators.zipfile.is_zipfile", return_value=True)
    def test_raise_validation_error_for_mismatched_filenames(self, mock_is_zipfile):
        shp_import = ShapefileImportFactory.build()
        with self.assertRaises(ValidationError) as context:
            self.validator(shp_import.shapefiles)
        self.assertEqual(context.exception.code, "mismatched_filenames")

    @patch(
        "imports.validators.zipfile.ZipFile",
        create_mock_zip_file_class(["test.shp", "test.shx"]),
    )
    @patch("imports.validators.zipfile.is_zipfile", return_value=True)
    def test_raise_validation_error_for_missing_required_files(self, mock_is_zipfile):
        shp_import = ShapefileImportFactory.build()
        with self.assertRaises(ValidationError) as context:
            self.validator(shp_import.shapefiles)
        self.assertEqual(context.exception.code, "missing_required_files")
