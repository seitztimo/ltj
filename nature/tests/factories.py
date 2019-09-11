import datetime

import factory
from django.contrib.gis.geos import Point
from nature.models import PROTECTION_LEVELS


class OriginFactory(factory.django.DjangoModelFactory):
    explanation = factory.Faker('text', max_nb_chars=50)
    source = factory.Faker('text', max_nb_chars=50)

    class Meta:
        model = 'nature.Origin'


class ValueFactory(factory.django.DjangoModelFactory):
    explanation = factory.Faker('text', max_nb_chars=50)
    value = factory.Faker('text', max_nb_chars=10)
    valuator = factory.Faker('text', max_nb_chars=50)
    link = factory.Faker('paragraph')

    class Meta:
        model = 'nature.Value'


class OccurrenceFactory(factory.django.DjangoModelFactory):
    explanation = factory.Faker('text', max_nb_chars=50)

    class Meta:
        model = 'nature.Occurrence'


class PersonFactory(factory.django.DjangoModelFactory):
    surname = factory.Faker('last_name')
    first_name = factory.Faker('first_name')
    public_servant = True

    class Meta:
        model = 'nature.Person'


class ObservationSeriesFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=50)
    person = factory.SubFactory(PersonFactory)
    description = factory.Faker('paragraph')
    valid = True

    class Meta:
        model = 'nature.ObservationSeries'


class PublicationTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=20)

    class Meta:
        model = 'nature.PublicationType'


class PublicationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=150)
    author = factory.Faker('name')
    publication_type = factory.SubFactory(PublicationTypeFactory)

    class Meta:
        model = 'nature.Publication'


class FeatureClassFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: "fc-{0}".format(n))
    name = factory.Faker('text', max_nb_chars=50)
    reporting = True
    www = True
    open_data = True

    class Meta:
        model = 'nature.FeatureClass'


class FeatureFactory(factory.django.DjangoModelFactory):
    fid = factory.Sequence(lambda n: "f-{0}".format(n))
    feature_class = factory.SubFactory(FeatureClassFactory)
    geometry = Point(1, 1)
    name = factory.Faker('text', max_nb_chars=80)
    active = True
    protection_level = PROTECTION_LEVELS['PUBLIC']

    class Meta:
        model = 'nature.Feature'


class HistoricalFeatureFactory(factory.django.DjangoModelFactory):
    fid = factory.Sequence(lambda n: "hf-{0}".format(n))
    feature_class = factory.SubFactory(FeatureClassFactory)
    geometry = Point(1, 1)
    name = factory.Faker('text', max_nb_chars=80)
    active = True
    protection_level = PROTECTION_LEVELS['PUBLIC']
    archived_time = factory.Faker('date_time_this_year', before_now=True, tzinfo=datetime.timezone.utc)
    feature = 1

    class Meta:
        model = 'nature.HistoricalFeature'


class FeatureValueFactory(factory.django.DjangoModelFactory):
    feature = factory.SubFactory(FeatureFactory)
    value = factory.SubFactory(ValueFactory)

    class Meta:
        model = 'nature.FeatureValue'


class LinkTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=20)

    class Meta:
        model = 'nature.LinkType'


class FeatureLinkFactory(factory.django.DjangoModelFactory):
    feature = factory.SubFactory(FeatureFactory)
    link = factory.Faker('paragraph')
    text = factory.Faker('paragraph')
    link_type = factory.SubFactory(LinkTypeFactory)
    protection_level = PROTECTION_LEVELS['PUBLIC']

    class Meta:
        model = 'nature.FeatureLink'


class SpeciesFactory(factory.django.DjangoModelFactory):
    taxon = factory.Faker('text', max_nb_chars=5)
    taxon_1 = factory.Faker('text', max_nb_chars=50)
    taxon_2 = factory.Faker('text', max_nb_chars=50)
    name_fi = factory.Faker('text', max_nb_chars=150)
    protection_level = PROTECTION_LEVELS['PUBLIC']

    class Meta:
        model = 'nature.Species'


class ObservationFactory(factory.django.DjangoModelFactory):
    code = factory.Faker('text', max_nb_chars=100)
    feature = factory.SubFactory(FeatureFactory)
    species = factory.SubFactory(SpeciesFactory)
    series = factory.SubFactory(ObservationSeriesFactory)
    protection_level = PROTECTION_LEVELS['PUBLIC']

    class Meta:
        model = 'nature.Observation'


class MigrationClassFactory(factory.django.DjangoModelFactory):
    explanation = factory.Faker('text', max_nb_chars=50)
    source = factory.Faker('text', max_nb_chars=50)
    value = 1

    class Meta:
        model = 'nature.MigrationClass'


class HabitatTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=50)
    code = factory.Faker('text', max_nb_chars=10)

    class Meta:
        model = 'nature.HabitatType'


class HabitatTypeObservationFactory(factory.django.DjangoModelFactory):
    feature = factory.SubFactory(FeatureFactory)
    habitat_type = factory.SubFactory(HabitatTypeFactory)
    observation_series = factory.SubFactory(ObservationSeriesFactory)

    class Meta:
        model = 'nature.HabitatTypeObservation'


class BreedingDegreeFactory(factory.django.DjangoModelFactory):
    explanation = factory.Faker('text', max_nb_chars=50)
    source = factory.Faker('text', max_nb_chars=50)
    value = 1

    class Meta:
        model = 'nature.BreedingDegree'


class AbundanceFactory(factory.django.DjangoModelFactory):
    explanation = factory.Faker('text', max_nb_chars=50)
    source = factory.Faker('text', max_nb_chars=50)
    value = 1

    class Meta:
        model = 'nature.Abundance'


class SquareFactory(factory.django.DjangoModelFactory):
    id = factory.SubFactory(FeatureFactory)
    number = 1

    class Meta:
        model = 'nature.Square'


class RegulationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=255)
    valid = True

    class Meta:
        model = 'nature.Regulation'


class SpeciesRegulationFactory(factory.django.DjangoModelFactory):
    species = factory.SubFactory(SpeciesFactory)
    regulation = factory.SubFactory(RegulationFactory)

    class Meta:
        model = 'nature.SpeciesRegulation'


class ConservationProgrammeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=20)

    class Meta:
        model = 'nature.ConservationProgramme'


class CriterionFactory(factory.django.DjangoModelFactory):
    criterion = factory.Faker('text', max_nb_chars=50)

    class Meta:
        model = 'nature.Criterion'


class ProtectionFactory(factory.django.DjangoModelFactory):
    id = factory.SubFactory(FeatureFactory)

    class Meta:
        model = 'nature.Protection'


class TransactionTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=20)

    class Meta:
        model = 'nature.TransactionType'


class TransactionFactory(factory.django.DjangoModelFactory):
    register_id = factory.Faker('text', max_nb_chars=20)
    transaction_type = factory.SubFactory(TransactionTypeFactory)
    protection_level = PROTECTION_LEVELS['PUBLIC']

    class Meta:
        model = 'nature.Transaction'


class TransactionFeatureFactory(factory.django.DjangoModelFactory):
    feature = factory.SubFactory(FeatureFactory)
    transaction = factory.SubFactory(TransactionFactory)

    class Meta:
        model = 'nature.TransactionFeature'


class FrequencyFactory(factory.django.DjangoModelFactory):
    explanation = factory.Faker('text', max_nb_chars=50)
    source = factory.Faker('text', max_nb_chars=50)
    value = 1

    class Meta:
        model = 'nature.Frequency'
