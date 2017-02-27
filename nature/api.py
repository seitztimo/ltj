from rest_framework import serializers, viewsets, routers
from nature.models import Feature, Species, Observation, Publication, Event, Person, Regulation, HabitatType, HabitatTypeObservation, FeatureClass, Value
from nature.models import ProtectionLevel, Permission, PERMISSIONS


class FeatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'name', 'type', 'feature_class', 'geometry1', 'description', 'notes', 'active',
                  'created_time', 'last_modified_time', 'number', 'area', 'text', 'values', 'publications')


class FeatureClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FeatureClass
        fields = '__all__'


class ValueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FeatureClass
        fields = ('id', 'explanation', 'type', 'date', 'link')


class PublicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Species


class ObservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Observation


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event


class PublicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publication


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person


class RegulationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Regulation


class HabitatTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HabitatType


class HabitatTypeObservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HabitatTypeObservation


class ProtectedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Handles view permissions for ProtectedNatureModel instances.
    """

    def get_queryset(self):
        return super().get_queryset().filter(protection_level=Permission.PUBLIC)


class FeatureViewSet(ProtectedViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeatureClass.objects.all()
    serializer_class = FeatureClassSerializer


class ValueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
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
