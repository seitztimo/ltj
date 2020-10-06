from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from django.utils.translation import ugettext as _

from .models import ShapefileImport
from .importers import ShapefileImporter


@admin.register(ShapefileImport)
class ShapefileImportAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by", "created_time")
    actions = None

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # only do imports when creating new instances
            num_features = ShapefileImporter.import_features(obj.shapefiles)
            messages.add_message(
                request,
                messages.INFO,
                _("{0} features are imported").format(num_features),
            )
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
