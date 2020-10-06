import os
import zipfile

import shapefile
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from nature.models import FeatureClass
from .importers import REQUIRED_SHAPEFILE_EXTENSIONS, SHAPEFILE_FIELD_MAPPING


@deconstructible
class ZippedShapefilesValidator:
    messages = {
        "invalid_zipfile": _("%(filename)s is not a valid zip file."),
        "mismatched_filenames": _("Files do not have a common filename prefix."),
        "missing_required_files": _(".shp, .shx and .dbf files are required."),
        "fields_not_allowed": _(
            "Fields not allowed: %(fields)s. Allowed shapefile fields are: %(allowed_fields)s."
        ),
        "feature_classes_not_exist": _(
            "Feature classes do not exist: %(feature_classes)s."
        ),
    }

    def __call__(self, value):
        if not zipfile.is_zipfile(value.file):
            raise ValidationError(
                self.messages["invalid_zipfile"],
                code="invalid_zipfile",
                params={"filename": value.file.name},
            )

        with zipfile.ZipFile(value.file) as zfile:
            self._validate_files(zfile)

            dbf, shp, shx = sorted(
                [
                    name
                    for name in zfile.namelist()
                    if name.endswith(REQUIRED_SHAPEFILE_EXTENSIONS)
                ]
            )
            with zfile.open(shp) as shp, zfile.open(shx) as shx, zfile.open(dbf) as dbf:
                shapefile_reader = shapefile.Reader(shp=shp, shx=shx, dbf=dbf)

            self._validate_fields(shapefile_reader)
            self._validate_feature_classes(shapefile_reader)

    def _validate_files(self, zfile):
        filenames, extensions = [], []
        for filename in zfile.namelist():
            if filename.endswith(REQUIRED_SHAPEFILE_EXTENSIONS):
                filename, extension = os.path.splitext(filename)
                filenames.append(filename)
                extensions.append(extension)

        if len(set(filenames)) > 1:  # check files have common filename prefix
            raise ValidationError(
                self.messages["mismatched_filenames"],
                code="mismatched_filenames",
            )

        if set(extensions) != set(REQUIRED_SHAPEFILE_EXTENSIONS):
            raise ValidationError(
                self.messages["missing_required_files"],
                code="missing_required_files",
            )

    def _validate_fields(self, shapefile_reader):
        shapefile_fields = [
            field[0] for field in shapefile_reader.fields[1:]
        ]  # first field reserved as deletion flag
        fields_not_allowed = set(shapefile_fields) - set(SHAPEFILE_FIELD_MAPPING.keys())
        if fields_not_allowed:
            raise ValidationError(
                self.messages["fields_not_allowed"],
                code="fields_not_allowed",
                params={
                    "fields": ", ".join(fields_not_allowed),
                    "allowed_fields": ", ".join(SHAPEFILE_FIELD_MAPPING.keys()),
                },
            )

    def _validate_feature_classes(self, shapefile_reader):
        shapefile_fields = [
            field[0] for field in shapefile_reader.fields[1:]
        ]  # first field reserved as deletion flag
        feature_class_column_index = shapefile_fields.index("luokkatunn")
        feature_classes = {
            record[feature_class_column_index]
            for record in shapefile_reader.iterRecords()
        }
        db_feature_classes = set(
            FeatureClass.objects.filter(id__in=feature_classes).values_list(
                "id", flat=True
            )
        )
        missing_feature_classes = feature_classes - db_feature_classes
        if missing_feature_classes:
            raise ValidationError(
                self.messages["feature_classes_not_exist"],
                code="feature_classes_not_exist",
                params={"feature_classes": ", ".join(missing_feature_classes)},
            )
