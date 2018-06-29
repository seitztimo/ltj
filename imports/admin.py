from django.contrib import admin
from django.db import transaction

from .models import ShapefileImport
from .importers import ShapefileImporter


@admin.register(ShapefileImport)
class ShapefileImportAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'created_time')
    actions = None

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # only do imports when creating new instances
            ShapefileImporter.import_features(obj.shapefiles)
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
