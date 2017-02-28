from django.core.exceptions import FieldError
from rest_framework import serializers, viewsets, routers, relations
from rest_framework.utils import model_meta
from nature.models import ProtectionLevel, Permission, PERMISSIONS
from nature.models import Feature, Species, Observation, Publication, Event, Person, Regulation, HabitatType, HabitatTypeObservation, FeatureClass, Value

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


class FeatureSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'name', 'type', 'feature_class', 'geometry1', 'description', 'notes', 'active',
                  'created_time', 'last_modified_time', 'number', 'area', 'text', 'values', 'publications')


class FeatureClassSerializer(ProtectedHyperlinkedModelSerializer):

    class Meta:
        model = FeatureClass
        fields = ('id', 'name', 'additional_info', 'super_class', 'reporting', 'www', 'metadata', 'features')


class ValueSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = FeatureClass
        fields = ('id', 'explanation', 'type', 'date', 'link')


class PublicationSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class SpeciesSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Species


class ObservationSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Observation


class EventSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Event


class PersonSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Person


class RegulationSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = Regulation


class HabitatTypeSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = HabitatType


class HabitatTypeObservationSerializer(ProtectedHyperlinkedModelSerializer):
    class Meta:
        model = HabitatTypeObservation


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


class ObservationViewSet(ProtectedViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer


class SpeciesViewSet(ProtectedViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class EventViewSet(ProtectedViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


router = routers.DefaultRouter()
router.register(r'feature', FeatureViewSet)
router.register(r'feature_class', FeatureClassViewSet)
router.register(r'value', ValueViewSet)
router.register(r'publication', PublicationViewSet)
router.register(r'observation', ObservationViewSet)
router.register(r'species', SpeciesViewSet)
router.register(r'event', EventViewSet)
