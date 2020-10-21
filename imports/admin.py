from django.contrib import admin
from django.contrib import messages
from django.db import transaction

from .models import ShapefileImport
from .importers import ShapefileImporter, ImportValidationError


@admin.register(ShapefileImport)
class ShapefileImportAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by", "created_time")
    actions = None

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # only do imports when creating new instances
            try:
                import_log = ShapefileImporter.import_features(obj.shapefiles)
                for level, msg in import_log:
                    messages.add_message(request, level, msg)
                obj.created_by = request.user
            except ImportValidationError as e:
                for message in e.messages:
                    messages.add_message(request, messages.ERROR, message)
                return
        super().save_model(request, obj, form, change)
