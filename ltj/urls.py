from django.urls import include, path
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from nature.api import router

urlpatterns = [
    path("helauth/", include("helusers.urls")),
    path("admin/", admin.site.urls),
    path("v1/", include(router.urls)),
    path("ltj/", include("nature.urls")),
]

admin.site.site_title = _("Luontotietojärjestelmä site admin")
admin.site.site_url = "/admin"
