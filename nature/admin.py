from django.contrib.gis import admin

from .models import Feature, Observation
from .forms import FeatureForm


class ObservationInline(admin.TabularInline):
    model = Observation
    fields = ('species', 'series', 'protection_level', 'created_time')
    readonly_fields = ('created_time', )
    extra = 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('species', 'series')


@admin.register(Feature)
class FeatureAdmin(admin.OSMGeoAdmin):
    readonly_fields = ('created_by', 'created_time', 'last_modified_by', 'last_modified_time')
    list_display = ('id', 'feature_class', 'name')
    form = FeatureForm
    inlines = [ObservationInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('feature_class')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.username
        obj.last_modified_by = request.user.username
        obj.save()
