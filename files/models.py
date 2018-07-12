from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class File(models.Model):
    file = models.FileField(_('file'), upload_to='files/')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'), related_name='created_files')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True, null=True, blank=True)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('last modified by'),
                                         related_name='modified_files')
    last_modified_time = models.DateTimeField(_('last modified time'), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __str__(self):
        return self.file.name
