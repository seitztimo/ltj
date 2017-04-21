from django.core.exceptions import FieldError
from rest_framework.fields import SerializerMethodField
from rest_framework.reverse import reverse
from rest_framework import serializers, viewsets, routers, relations
from munigeo.api import GeoModelSerializer
from nature.models import ProtectionLevel, Permission, PERMISSIONS
from nature.models import *

# the abstract serializers


class ProtectedManyRelatedField(relations.ManyRelatedField):
    """
    Handles view permissions for related field listings with ProtectedNatureModel instances.
    """
    def to_representation(self, iterable):
        try:
            iterable = iterable.filter(protection_level=Permission.PUBLIC)
        except FieldError:
            # this allows the field to be used even with non-protected models
            pass
        return super().to_representation(iterable)


class ProtectedHyperlinkedRelatedField(relations.HyperlinkedRelatedField):
    """
    Handles view permissions for related field listings with ProtectedNatureModel instances.
    """
    @classmethod
    def many_init(cls, *args, **kwargs):
        # the correct arguments must be passed on to the parent
        list_kwargs = {'child_relation': cls(*args, **kwargs)}
        for key in kwargs.keys():
            if key in relations.MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        return ProtectedManyRelatedField(**list_kwargs)


class SpanOneToOneProtectedHyperlinkedRelatedField(ProtectedHyperlinkedRelatedField):
    """
    Allows linking directly back to the feature, instead of an object with the same id as feature.
    Useful for spanning useless one-to-one mappings.
    """

    def get_url(self, obj, view_name, request, format):
        kwargs = {'pk': obj.pk}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class ProtectedHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Handles view permissions for related field listings with ProtectedNatureModel instances.
    """
    serializer_related_field = ProtectedHyperlinkedRelatedField


class ProtectedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Handles view permissions for ProtectedNatureModel instances.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        try:
            return qs.filter(protection_level=Permission.PUBLIC)
        except FieldError:
            # this allows the viewset to be used even with non-protected models
            return qs

# the model serializers


class ConservationProgrammeSerializer(ProtectedHyperlinkedModelSerializer):
    protected_features = SpanOneToOneProtectedHyperlinkedRelatedField(many=True,
                                                                      source='protections',
                                                                      view_name='feature-detail',
                                                                      queryset=Feature.objects.all())

    class Meta:
        model = ConservationProgramme
        fields = ('id', 'name', 'protected_features')


class CriterionSerializer(ProtectedHyperlinkedModelSerializer):
    protected_features = SpanOneToOneProtectedHyperlinkedRelatedField(many=True,
                                                                      source='protections',
                                                                      view_name='feature-detail',
                                                                      queryset=Feature.objects.all())

    class Meta:
        model = Criterion
        fields = ('id', 'criterion', 'specific_criterion', 'subcriterion', 'protected_features')


class SquareSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Square
        fields = ('number', 'degree_of_determination', 'additional_info')


class ProtectionSerializer(ProtectedHyperlinkedModelSerializer):

    class Meta:
        model = Protection
        fields = ('reported_area', 'land_area', 'water_area', 'hiking', 'regulations', 'additional_info',
                  'criteria', 'conservation_programmes')


class FeatureSerializer(ProtectedHyperlinkedModelSerializer, GeoModelSerializer):
    square = SquareSerializer()
    protection = ProtectionSerializer()
    text = SerializerMethodField()

    def get_text(self, obj):
        # now this is a silly feature: text should not be public if text_www exists
        if obj.text_www:
            return obj.text_www
        else:
            return obj.text

    class Meta:
        model = Feature
        fields = ('url', 'name', 'fid', 'feature_class', 'geometry1', 'description', 'notes', 'active',
                  'created_time', 'last_modified_time', 'number', 'area', 'text', 'values', 'publications',
                  'observations', 'habitat_type_observations', 'links', 'square', 'protection', 'events')


class FeatureClassSerializer(ProtectedHyperlinkedModelSerializer):

    class Meta:
        model = FeatureClass
        fields = ('url', 'name', 'additional_info', 'super_class', 'reporting', 'www', 'metadata', 'features')


class ValueSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Value
        fields = ('url', 'explanation', 'type', 'date', 'link', 'features')


class PublicationSerializer(ProtectedHyperlinkedModelSerializer):
    publication_type = serializers.StringRelatedField()

    class Meta:
        model = Publication
        fields = ('url', 'publication_type', 'name', 'author', 'series', 'place_of_printing', 'year',
                  'additional_info', 'link', 'features')


class SpeciesSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Species
        fields = ('url', 'code', 'taxon', 'taxon_1', 'name_fi', 'name_sci_1', 'name_subspecies_1', 'registry_date',
                  'regulations', 'observations')


class AbundanceSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Abundance
        fields = ('id', 'value', 'explanation', 'source')


class IncidenceSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Incidence
        fields = ('id', 'value', 'explanation', 'source')


class MobilitySerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Mobility
        fields = ('id', 'value', 'explanation', 'source')


class OriginSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Origin
        fields = ('id', 'explanation', 'source')


class BreedingCategorySerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = BreedingCategory
        fields = ('id', 'value', 'explanation', 'source')


class ObservationSerializer(ProtectedHyperlinkedModelSerializer):
    occurrence = serializers.StringRelatedField()
    abundance = AbundanceSerializer()
    incidence = IncidenceSerializer()
    mobility = MobilitySerializer()
    origin = OriginSerializer()
    breeding_category = BreedingCategorySerializer()

    class Meta:
        model = Observation
        fields = ('url', 'location', 'species', 'series', 'abundance', 'incidence', 'number', 'mobility', 'origin',
                  'breeding_category', 'description', 'notes', 'date', 'occurrence', 'created_time', 'last_modified_time')


class ObservationSeriesSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = ObservationSeries
        fields = ('url', 'name', 'description', 'start_date', 'end_date', 'method', 'notes', 'additional_info',
                  'valid', 'observations', 'habitat_type_observations')


class EventTypeSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = EventType
        fields = ('id', 'name')


class EventSerializer(ProtectedHyperlinkedModelSerializer):
    type = EventTypeSerializer()

    class Meta:
        model = Event
        fields = ('url', 'register_id', 'description', 'type', 'date', 'link', 'features', 'regulations')


class PersonSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Person


class RegulationSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Regulation
        fields = ('url', 'name', 'paragraph', 'additional_info', 'value', 'value_explanation', 'valid',
                  'date_of_entry', 'link', 'species', 'events', 'habitat_types')


class HabitatTypeSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = HabitatType
        fields = ('url', 'name', 'code', 'description', 'additional_info', 'group', 'regulations',
                  'habitat_type_observations')


class HabitatTypeObservationSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = HabitatTypeObservation
        fields = ('url', 'feature', 'habitat_type', 'group_fraction', 'additional_info', 'observation_series',
                  'created_time', 'last_modified_time')


class FeatureViewSet(ProtectedViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureClassViewSet(ProtectedViewSet):
    queryset = FeatureClass.objects.all()
    serializer_class = FeatureClassSerializer


class ValueViewSet(ProtectedViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer


class PublicationViewSet(ProtectedViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class RegulationViewSet(ProtectedViewSet):
    queryset = Regulation.objects.all()
    serializer_class = RegulationSerializer


class SpeciesViewSet(ProtectedViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class ObservationViewSet(ProtectedViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer


class ObservationSeriesViewSet(ProtectedViewSet):
    queryset = ObservationSeries.objects.all()
    serializer_class = ObservationSeriesSerializer


class HabitatTypeViewSet(ProtectedViewSet):
    queryset = HabitatType.objects.all()
    serializer_class = HabitatTypeSerializer


class HabitatTypeObservationViewSet(ProtectedViewSet):
    queryset = HabitatTypeObservation.objects.all()
    serializer_class = HabitatTypeObservationSerializer


class EventViewSet(ProtectedViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AbundanceViewSet(ProtectedViewSet):
    queryset = Abundance.objects.all()
    serializer_class = AbundanceSerializer


class IncidenceViewSet(ProtectedViewSet):
    queryset = Incidence.objects.all()
    serializer_class = IncidenceSerializer


class MobilityViewSet(ProtectedViewSet):
    queryset = Mobility.objects.all()
    serializer_class = MobilitySerializer


class OriginViewSet(ProtectedViewSet):
    queryset = Origin.objects.all()
    serializer_class = OriginSerializer


class BreedingCategoryViewSet(ProtectedViewSet):
    queryset = BreedingCategory.objects.all()
    serializer_class = BreedingCategorySerializer


class ProtectionCriterionViewSet(ProtectedViewSet):
    queryset = Criterion.objects.all()
    serializer_class = CriterionSerializer


class ConservationProgrammeViewSet(ProtectedViewSet):
    queryset = ConservationProgramme.objects.all()
    serializer_class = ConservationProgrammeSerializer

router = routers.DefaultRouter()
router.register(r'feature', FeatureViewSet)
router.register(r'feature_class', FeatureClassViewSet)
router.register(r'value', ValueViewSet)
router.register(r'species', SpeciesViewSet)
router.register(r'observation', ObservationViewSet)
router.register(r'observation_series', ObservationSeriesViewSet)
router.register(r'habitat_type', HabitatTypeViewSet)
router.register(r'habitat_type_observation', HabitatTypeObservationViewSet)
router.register(r'publication', PublicationViewSet)
router.register(r'regulation', RegulationViewSet)
router.register(r'event', EventViewSet)
router.register(r'protection_criterion', ProtectionCriterionViewSet)
router.register(r'conservation_programme', ConservationProgrammeViewSet)
