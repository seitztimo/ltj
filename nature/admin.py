from django.contrib.gis import admin
from django.conf import settings

from .models import (
    Feature, FeatureClass, FeatureLink, FeaturePublication,
    Observation, ObservationSeries, Publication,
    Species, LinkType,
)
from .forms import FeatureForm
from .widgets import NatureOLWidget


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_fi', 'name_sci_1', 'name_subspecies_1', 'code')
    search_fields = ('name_fi', 'name_sci_1', 'name_subspecies_1', 'code', 'id')
    list_filter = ('taxon', 'taxon_1')
    actions = None


@admin.register(ObservationSeries)
class ObservationSeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'valid')
    search_fields = ('name',)
    actions = None


class ObservationInline(admin.TabularInline):
    model = Observation
    fields = ('species', 'series', 'date', 'observer', 'number', 'description', 'notes',
              'protection_level', 'local_or_migrating', 'occurrence', 'origin')
    raw_id_fields = ('species',)
    extra = 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('species', 'series')


@admin.register(LinkType)
class LinkTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class FeatureLinkInline(admin.TabularInline):
    model = FeatureLink
    fields = ('link', 'text', 'link_text', 'link_type', 'ordering', 'protection_level')
    extra = 1


@admin.register(FeatureClass)
class FeatureClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'www', 'open_data')
    search_fields = ('name',)
    actions = None


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'publication_type', 'name', 'year')
    search_fields = ('name',)
    list_filter = ('publication_type', 'year')
    actions = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('publication_type')


class FeaturePublicationInline(admin.TabularInline):
    model = FeaturePublication
    raw_id_fields = ('publication',)
    extra = 1


@admin.register(Feature)
class FeatureAdmin(admin.GeoModelAdmin):
    readonly_fields = ('_area', 'created_by', 'created_time', 'last_modified_by', 'last_modified_time')
    list_display = ('id', 'feature_class', 'fid', 'name', 'active')
    search_fields = ('feature_class__name', 'name', 'fid', 'id')
    list_filter = ('feature_class', 'active')
    form = FeatureForm
    inlines = [ObservationInline, FeatureLinkInline, FeaturePublicationInline]
    actions = None

    widget = NatureOLWidget
    map_template = 'nature/openlayers-nature.html'
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.js'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('feature_class')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.username
        obj.last_modified_by = request.user.username
        obj.save()

    def get_fields(self, request, obj=None):
        form = self.get_form(request, obj, fields=None)
        # Move the feature class field to the beginning of the ordered dict
        if 'feature_class' in form.base_fields:
            form.base_fields.move_to_end('feature_class', last=False)
        return list(form.base_fields) + list(self.get_readonly_fields(request, obj))

    # Return formatted area as area
    def _area(self, obj):
        return obj.formatted_area
    _area.short_description = Feature._meta.get_field('area').verbose_name
