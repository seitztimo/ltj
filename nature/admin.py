from django.contrib import admin

from .models import Feature
from .forms import FeatureForm


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'created_time', 'last_modified_by', 'last_modified_time')
    list_display = ('id', 'feature_class', 'name')
    form = FeatureForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('feature_class')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.username
        obj.last_modified_by = request.user.username
        obj.save()
