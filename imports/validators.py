import os
import zipfile

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

REQUIRED_SHAPEFILE_EXTENSIONS = (".shp", ".shx", ".dbf")


@deconstructible
class ZippedShapefilesValidator:
    messages = {
        "invalid_zipfile": _("%(filename)s is not a valid zip file."),
        "mismatched_filenames": _("Files do not have a common filename prefix."),
        "missing_required_files": _(".shp, .shx and .dbf files are required."),
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
