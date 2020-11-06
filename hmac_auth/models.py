from django.db import models
from django.utils.translation import ugettext_lazy as _


class HMACGroup(models.Model):
    ADMIN = "admin"
    OFFICE_HKI = "office_hki"
    OFFICE = "office"
    PERMISSION_LEVEL_CHOICES = [
        (ADMIN, _("Admin")),
        (OFFICE_HKI, _("Office HKI")),
        (OFFICE, _("Office")),
    ]

    name = models.CharField(_("group name"), max_length=200)
    permission_level = models.CharField(
        choices=PERMISSION_LEVEL_CHOICES, default=OFFICE, max_length=50
    )

    def __str__(self):
        return self.name

    @property
    def is_admin_group(self):
        return self.permission_level == HMACGroup.ADMIN

    @property
    def is_office_hki_group(self):
        return self.permission_level == HMACGroup.OFFICE_HKI

    @property
    def is_office_group(self):
        return self.permission_level == HMACGroup.OFFICE
