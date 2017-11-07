from django.contrib.gis import admin

from .models import (
    Feature, FeatureClass, FeatureLink, FeaturePublication,
    Observation, ObservationSeries, Publication,
    Species, LinkType,
)
from .forms import FeatureForm


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_fi', 'name_sci_1', 'name_subspecies_1')
    search_fields = ('name_fi', 'name_sci_1', 'name_subspecies_1')
    list_filter = ('taxon', 'taxon_1')


@admin.register(ObservationSeries)
class ObservationSeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'valid')
    search_fields = ('name',)


class ObservationInline(admin.TabularInline):
    model = Observation
    fields = ('species', 'series', 'protection_level', 'created_time')
    raw_id_fields = ('species',)
    readonly_fields = ('created_time', )
    extra = 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('species', 'series')


@admin.register(LinkType)
class LinkTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class FeatureLinkInline(admin.TabularInline):
    model = FeatureLink
    fields = ('link', 'text', 'link_type', 'ordering')
    extra = 1


@admin.register(FeatureClass)
class FeatureClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'publication_type', 'name')
    search_fields = ('name',)
    list_filter = ('publication_type', 'year')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('publication_type')


class FeaturePublicationInline(admin.TabularInline):
    model = FeaturePublication
    raw_id_fields = ('publication',)
    extra = 1


@admin.register(Feature)
class FeatureAdmin(admin.OSMGeoAdmin):
    readonly_fields = ('created_by', 'created_time', 'last_modified_by', 'last_modified_time')
    list_display = ('id', 'feature_class', 'name', 'active')
    search_fields = ('feature_class__name', 'name',)
    list_filter = ('feature_class', 'active')
    form = FeatureForm
    inlines = [ObservationInline, FeatureLinkInline, FeaturePublicationInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('feature_class')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.username
        obj.last_modified_by = request.user.username
        obj.save()
