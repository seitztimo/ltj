from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.contrib.gis.geos import Point, Polygon
from django.utils.translation import activate

from .factories import (
    OriginFactory, ValueFactory, OccurrenceFactory,
    ObservationSeriesFactory, PersonFactory,
    PublicationFactory, PublicationTypeFactory,
    FeatureFactory, HistoricalFeatureFactory,
    FeatureLinkFactory, ObservationFactory,
    SpeciesFactory, MigrationClassFactory,
    LinkTypeFactory, HabitatTypeFactory,
    HabitatTypeObservationFactory, FeatureClassFactory,
    BreedingDegreeFactory, AbundanceFactory,
    SquareFactory, RegulationFactory,
    ConservationProgrammeFactory, ProtectionFactory,
    CriterionFactory, TransactionFactory,
    TransactionTypeFactory, FrequencyFactory,
    TransactionFeatureFactory)

from ..models import Feature, FeatureClass, ProtectionLevelMixin


class TestProtectionLevelEnabledQuerySet(TestCase):

    def setUp(self):
        self.feature_admin = FeatureFactory(
            name='admin',
            protection_level=ProtectionLevelMixin.ADMIN_ONLY,
        )
        self.feature_admin_and_staff = FeatureFactory(
            name='admin_and_staff',
            protection_level=ProtectionLevelMixin.ADMIN_AND_STAFF,
        )
        self.feature_public = FeatureFactory(
            name='public',
            protection_level=ProtectionLevelMixin.PUBLIC,
        )

    def test_for_admin(self):
        qs = Feature.objects.for_admin()
        self.assertIn(self.feature_admin, qs)
        self.assertIn(self.feature_admin_and_staff, qs)
        self.assertIn(self.feature_public, qs)

    def test_for_admin_and_staff(self):
        qs = Feature.objects.for_admin_and_staff()
        self.assertNotIn(self.feature_admin, qs)
        self.assertIn(self.feature_admin_and_staff, qs)
        self.assertIn(self.feature_public, qs)

    def test_for_public(self):
        qs = Feature.objects.for_public()
        self.assertNotIn(self.feature_admin, qs)
        self.assertNotIn(self.feature_admin_and_staff, qs)
        self.assertIn(self.feature_public, qs)


class TestOrigin(TestCase):

    def setUp(self):
        self.origin = OriginFactory(explanation='origin')

    def test__str__(self):
        self.assertEqual(self.origin.__str__(), 'origin')


class TestValue(TestCase):

    def setUp(self):
        self.value = ValueFactory(explanation='value')

    def test__str__(self):
        self.assertEqual(self.value.__str__(), 'value')


class TestOccurrence(TestCase):

    def setUp(self):
        self.occurrence = OccurrenceFactory(explanation='occurrence')

    def test__str__(self):
        self.assertEqual(self.occurrence.__str__(), 'occurrence')


class TestObservationSeries(TestCase):

    def setUp(self):
        self.observation_series = ObservationSeriesFactory(name='observation series')

    def test__str__(self):
        self.assertEqual(self.observation_series.__str__(), 'observation series')

        self.observation_series.id = 123
        self.observation_series.name = None
        self.assertEqual(self.observation_series.__str__(), 'Observation series 123')


class TestPerson(TestCase):

    def setUp(self):
        self.person = PersonFactory(surname='Surname', first_name='Firstname')

    def test__str__(self):
        self.assertEqual(self.person.__str__(), 'Firstname Surname')


class TestPublication(TestCase):

    def setUp(self):
        self.publication = PublicationFactory(name='publication')

    def test__str__(self):
        self.assertEqual(self.publication.__str__(), 'publication')


class TestPublicationType(TestCase):

    def setUp(self):
        self.publication_type = PublicationTypeFactory(name='publication type')

    def test__str__(self):
        self.assertEqual(self.publication_type.__str__(), 'publication type')


class TestProtectedFeatureQueryset(TestCase):

    def setUp(self):
        open_data_feature_class = FeatureClassFactory(open_data=True)
        self.open_data_feature = FeatureFactory(feature_class=open_data_feature_class)

        not_open_data_feature_class = FeatureClassFactory(open_data=False)
        self.not_open_data_feature = FeatureFactory(feature_class=not_open_data_feature_class)

    def test_open_data(self):
        qs = Feature.objects.open_data()
        self.assertIn(self.open_data_feature, qs)
        self.assertNotIn(self.not_open_data_feature, qs)


class TestFeature(TestCase):

    def setUp(self):
        self.feature = FeatureFactory(name='feature')

    def test__str__(self):
        self.assertEqual(self.feature.__str__(), 'feature')

        self.feature.id = 123
        self.feature.name = None
        self.assertEqual(self.feature.__str__(), 'Feature 123')

    def test_save(self):
        self.feature.geometry = Point(1, 1)
        self.feature.save()
        self.assertIsNone(self.feature.area)

        self.feature.geometry = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        self.feature.save()
        self.assertAlmostEqual(self.feature.area, 4 / 10000)

    def test_formatted_area(self):
        # No area
        self.assertIsNone(self.feature.area)
        self.assertEqual(self.feature.formatted_area, 0.0)

        # Rounded up
        round_up_area = 57.83757384
        self.feature.area = round_up_area
        self.feature.save()
        self.assertEqual(self.feature.area, round_up_area)
        self.assertEqual(self.feature.formatted_area, 57.84)

        # Rounded down
        round_down_area = 57.833
        self.feature.area = round_down_area
        self.feature.save()
        self.assertEqual(self.feature.area, round_down_area)
        self.assertEqual(self.feature.formatted_area, 57.83)

    def test_feature_is_protected(self):
        with patch('nature.models.FeatureClass.is_protected', new_callable=MagicMock(return_value=True)):
            self.assertTrue(self.feature.is_protected)

    def test_feature_is_not_protected(self):
        with patch('nature.models.FeatureClass.is_protected', new_callable=MagicMock(return_value=False)):
            self.assertFalse(self.feature.is_protected)


class TestHistoricalFeature(TestCase):

    def setUp(self):
        self.historical_feature = HistoricalFeatureFactory(name='historical feature')

    def test__str__(self):
        self.assertEqual(self.historical_feature.__str__(), 'historical feature')

        self.historical_feature.id = 123
        self.historical_feature.name = None
        self.assertEqual(self.historical_feature.__str__(), 'Historical feature 123')

    def test_save(self):
        self.historical_feature.geometry = Point(1, 1)
        self.historical_feature.save()
        self.assertIsNone(self.historical_feature.area)

        self.historical_feature.geometry = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        self.historical_feature.save()
        self.assertAlmostEqual(self.historical_feature.area, 4 / 10000)


class TestFeatureLink(TestCase):

    def setUp(self):
        self.feature_link = FeatureLinkFactory(link='feature link')

    def test__str__(self):
        self.assertEqual(self.feature_link.__str__(), 'feature link')


class TestObservation(TestCase):

    def setUp(self):
        self.observation = ObservationFactory(code='123')

    def test__str__(self):
        self.assertEqual(self.observation.__str__(), '123')

        self.observation.id = 321
        self.observation.code = None
        self.assertEqual(self.observation.__str__(), 'Observation 321')


class TestSpecies(TestCase):

    def setUp(self):
        self.species = SpeciesFactory(
            name_fi='name_fi',
            name_sci_1='name_sci',
            name_subspecies_1='name_subspecies'
        )

    def test__str__(self):
        self.assertEqual(self.species.__str__(), 'name_fi, name_sci, name_subspecies')

        self.species.name_fi = None
        self.assertEqual(self.species.__str__(), 'name_sci, name_subspecies')


class TestMigrationClass(TestCase):

    def setUp(self):
        self.migrationclass = MigrationClassFactory(explanation='migrationclass')

    def test__str__(self):
        self.assertEqual(self.migrationclass.__str__(), 'migrationclass')


class TestLinkType(TestCase):

    def setUp(self):
        self.link_type = LinkTypeFactory(name='link type')

    def test__str__(self):
        self.assertEqual(self.link_type.__str__(), 'link type')


class TestHabitatTypeObservation(TestCase):

    def setUp(self):
        habitat_type = HabitatTypeFactory(name='habitat type')
        feature = FeatureFactory(name='feature')
        self.habitat_type_observation = HabitatTypeObservationFactory(
            feature=feature,
            habitat_type=habitat_type,
        )

    def test__str__(self):
        self.assertEqual(self.habitat_type_observation.__str__(), 'habitat type feature')


class TestHabitatType(TestCase):

    def setUp(self):
        self.habitat_type = HabitatTypeFactory(name='habitat type')

    def test__str__(self):
        self.assertEqual(self.habitat_type.__str__(), 'habitat type')


class TestProtectedFeatureClassQueryset(TestCase):

    def setUp(self):
        self.open_data_feature_class = FeatureClassFactory(open_data=True)
        self.not_open_data_feature_class = FeatureClassFactory(open_data=False)

    def test_open_data(self):
        qs = FeatureClass.objects.open_data()
        self.assertIn(self.open_data_feature_class, qs)
        self.assertNotIn(self.not_open_data_feature_class, qs)


class TestFeatureClass(TestCase):

    def setUp(self):
        self.feature_class = FeatureClassFactory(name='feature class')

    def test__str__(self):
        self.assertEqual(self.feature_class.__str__(), 'feature class')

        self.feature_class.id = 123
        self.feature_class.name = None
        self.assertEqual(self.feature_class.__str__(), 'Feature class 123')

    def test_feature_class_is_protected(self):
        self.feature_class.super_class = FeatureClassFactory(id=FeatureClass.PROTECTED_FEATURE_CLASS_ID)
        self.assertTrue(self.feature_class.is_protected)

    def test_feature_class_is_not_protected(self):
        self.assertFalse(self.feature_class.is_protected)

        self.feature_class.super_class = FeatureClassFactory()
        self.assertFalse(self.feature_class.is_protected)


class TestBreedingDegree(TestCase):

    def setUp(self):
        self.breeding_degree = BreedingDegreeFactory(explanation='breeding degree')

    def test__str__(self):
        self.assertEqual(self.breeding_degree.__str__(), 'breeding degree')


class TestAbundance(TestCase):

    def setUp(self):
        self.abundance = AbundanceFactory(explanation='abundance')

    def test__str__(self):
        self.assertEqual(self.abundance.__str__(), 'abundance')


class TestSquare(TestCase):

    def setUp(self):
        self.square = SquareFactory(number=2)

    def test__str__(self):
        self.assertEqual(self.square.__str__(), '2')


class TestRegulation(TestCase):

    def setUp(self):
        self.regulation = RegulationFactory(name='regulation')

    def test__str__(self):
        self.assertEqual(self.regulation.__str__(), 'regulation')


class TestConservationProgramme(TestCase):

    def setUp(self):
        self.conservation_programme = ConservationProgrammeFactory(name='programme')

    def test__str__(self):
        self.assertEqual(self.conservation_programme.__str__(), 'programme')


class TestProtection(TestCase):

    def setUp(self):
        self.protection = ProtectionFactory(reported_area='protection')

    def test__str__(self):
        self.assertEqual(self.protection.__str__(), 'protection')


class TestCriterion(TestCase):

    def setUp(self):
        self.criterion = CriterionFactory(criterion='criterion')

    def test__str__(self):
        self.assertEqual(self.criterion.__str__(), 'criterion')


class TestTransaction(TestCase):

    def setUp(self):
        self.transaction = TransactionFactory(register_id='transaction')

    def test__str__(self):
        activate('en')
        self.assertEqual(self.transaction.__str__(), 'Transaction #{0}'.format(self.transaction.id))


class TestTransactionFeature(TestCase):

    def setUp(self):
        self.transaction_feature = TransactionFeatureFactory()

    def test__str__(self):
        self.assertEqual(
            self.transaction_feature.__str__(),
            '{0} - {1}'.format(self.transaction_feature.feature, self.transaction_feature.transaction)
        )


class TestTransactionType(TestCase):

    def setUp(self):
        self.transaction_type = TransactionTypeFactory(name='transaction type')

    def test__str__(self):
        self.assertEqual(self.transaction_type.__str__(), 'transaction type')


class TestFrequency(TestCase):

    def setUp(self):
        self.frequency = FrequencyFactory(explanation='frequency')

    def test__str__(self):
        self.assertEqual(self.frequency.__str__(), 'frequency')
