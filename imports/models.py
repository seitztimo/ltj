from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .validators import ZippedShapefilesValidator


class ShapefileImport(models.Model):
    shapefiles = models.FileField(
        _('shapefiles'),
        upload_to='shapefiles/',
        validators=[
            FileExtensionValidator(allowed_extensions=['zip']),
            ZippedShapefilesValidator(),
        ],
        help_text=_('Zipped shapefiles that contains .shp, .shx and .dbf files with a common filename prefix')
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _('shapefile import')
        verbose_name_plural = _('shapefile imports')

    def __str__(self):
        return self.shapefiles.name
