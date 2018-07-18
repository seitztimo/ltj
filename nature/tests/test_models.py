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
    TransactionFeatureFactory, FeatureValueFactory)

from ..models import (
    Feature, FeatureClass, PROTECTION_LEVELS,
    CITY_EMPLOYEE_ONLY_FEATURE_CLASS_ID, Observation, FeatureValue)


class TestFeatureClassQuerySet(TestCase):

    def setUp(self):
        self.feature_class = FeatureClassFactory(open_data=False)
        self.feature_class_open_data = FeatureClassFactory(open_data=True)

    def test_open_data(self):
        qs = FeatureClass.objects.open_data()
        self.assertQuerysetEqual(qs, [repr(self.feature_class_open_data)])


class ProtectionLevelQuerySet(TestCase):

    def setUp(self):
        self.feature_admin = FeatureFactory(protection_level=PROTECTION_LEVELS['ADMIN'])
        self.feature_office = FeatureFactory(protection_level=PROTECTION_LEVELS['OFFICE'])
        self.feature_public = FeatureFactory(protection_level=PROTECTION_LEVELS['PUBLIC'])

    def test_for_admin(self):
        qs = Feature.objects.for_admin()
        expected_queryset = [
            repr(self.feature_admin),
            repr(self.feature_office),
            repr(self.feature_public),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_for_office(self):
        qs = Feature.objects.for_office()
        expected_queryset = [
            repr(self.feature_office),
            repr(self.feature_public),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_for_public(self):
        qs = Feature.objects.for_public()
        expected_queryset = [repr(self.feature_public)]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_open_data(self):
        qs = Feature.objects.open_data()
        expected_queryset = [repr(self.feature_public)]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)


class TestFeatureQuerySet(TestCase):

    def setUp(self):
        non_open_feature_class = FeatureClassFactory(open_data=False)
        open_feature_class = FeatureClassFactory(open_data=True)
        city_employee_feature_class = FeatureClassFactory(id=CITY_EMPLOYEE_ONLY_FEATURE_CLASS_ID, open_data=False)
        self.feature_admin = FeatureFactory(
            protection_level=PROTECTION_LEVELS['ADMIN'],
            feature_class=non_open_feature_class,
        )
        self.feature_office_city_employee = FeatureFactory(
            protection_level=PROTECTION_LEVELS['OFFICE'],
            feature_class=city_employee_feature_class,
        )
        self.feature_office_non_city_employee = FeatureFactory(
            protection_level=PROTECTION_LEVELS['OFFICE'],
            feature_class=non_open_feature_class,
        )
        self.feature_public = FeatureFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature_class=non_open_feature_class,
        )
        self.feature_public_open_data = FeatureFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature_class=open_feature_class,
        )

    def test_for_office_city_employee(self):
        qs = Feature.objects.for_office_city_employee()
        expected_queryset = [
            repr(self.feature_office_city_employee),
            repr(self.feature_office_non_city_employee),
            repr(self.feature_public),
            repr(self.feature_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_for_office_non_city_employee(self):
        qs = Feature.objects.for_office_non_city_employee()
        expected_queryset = [
            repr(self.feature_office_non_city_employee),
            repr(self.feature_public),
            repr(self.feature_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_open_data(self):
        qs = Feature.objects.open_data()
        expected_queryset = [repr(self.feature_public_open_data)]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)


class TestFeatureRelatedQuerySet(TestCase):

    def setUp(self):
        non_open_feature_class = FeatureClassFactory(open_data=False)
        open_feature_class = FeatureClassFactory(open_data=True)
        city_employee_feature_class = FeatureClassFactory(id=CITY_EMPLOYEE_ONLY_FEATURE_CLASS_ID, open_data=False)
        # features
        self.feature_admin = FeatureFactory(
            protection_level=PROTECTION_LEVELS['ADMIN'],
            feature_class=non_open_feature_class,
        )
        self.feature_office_city_employee = FeatureFactory(
            protection_level=PROTECTION_LEVELS['OFFICE'],
            feature_class=city_employee_feature_class,
        )
        self.feature_office_non_city_employee = FeatureFactory(
            protection_level=PROTECTION_LEVELS['OFFICE'],
            feature_class=non_open_feature_class,
        )
        self.feature_public = FeatureFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature_class=non_open_feature_class,
        )
        self.feature_public_open_data = FeatureFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature_class=open_feature_class,
        )
        # feature values
        self.feature_value_admin = FeatureValueFactory(feature=self.feature_admin)
        self.feature_value_office_city_employee = FeatureValueFactory(feature=self.feature_office_city_employee)
        self.feature_value_office_non_city_employee = FeatureValueFactory(feature=self.feature_office_non_city_employee)
        self.feature_value_public = FeatureValueFactory(feature=self.feature_public)
        self.feature_value_public_open_data = FeatureValueFactory(feature=self.feature_public_open_data)

    def test_for_admin(self):
        qs = FeatureValue.objects.for_admin()
        expected_queryset = [
            repr(self.feature_value_admin),
            repr(self.feature_value_office_city_employee),
            repr(self.feature_value_office_non_city_employee),
            repr(self.feature_value_public),
            repr(self.feature_value_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_for_office_city_employee(self):
        qs = FeatureValue.objects.for_office_city_employee()
        expected_queryset = [
            repr(self.feature_value_office_city_employee),
            repr(self.feature_value_office_non_city_employee),
            repr(self.feature_value_public),
            repr(self.feature_value_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_for_office_non_city_employee(self):
        qs = FeatureValue.objects.for_office_non_city_employee()
        expected_queryset = [
            repr(self.feature_value_office_non_city_employee),
            repr(self.feature_value_public),
            repr(self.feature_value_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_for_public(self):
        qs = FeatureValue.objects.for_public()
        expected_queryset = [
            repr(self.feature_value_public),
            repr(self.feature_value_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_open_data(self):
        qs = FeatureValue.objects.open_data()
        expected_queryset = [
            repr(self.feature_value_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)


class TestFeatureRelatedProtectionLevelQuerySet(TestCase):

    def setUp(self):
        non_open_feature_class = FeatureClassFactory(open_data=False)
        open_feature_class = FeatureClassFactory(open_data=True)
        city_employee_feature_class = FeatureClassFactory(id=CITY_EMPLOYEE_ONLY_FEATURE_CLASS_ID, open_data=False)
        # related features
        self.feature_office_city_employee = FeatureFactory(
            protection_level=PROTECTION_LEVELS['OFFICE'],
            feature_class=city_employee_feature_class,
        )
        self.feature_office_non_city_employee = FeatureFactory(
            protection_level=PROTECTION_LEVELS['OFFICE'],
            feature_class=non_open_feature_class,
        )
        self.feature_public = FeatureFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature_class=non_open_feature_class,
        )
        self.feature_public_open_data = FeatureFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature_class=open_feature_class,
        )

        # observations
        self.observation_office_feature_office_city_employee = ObservationFactory(
            protection_level=PROTECTION_LEVELS['OFFICE'],
            feature=self.feature_office_city_employee,
        )
        self.observation_office_feature_office_non_city_employee = ObservationFactory(
            protection_level=PROTECTION_LEVELS['OFFICE'],
            feature=self.feature_office_non_city_employee,
        )
        self.observation_public_feature_office = ObservationFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature=self.feature_office_non_city_employee,
        )
        self.observation_public_feature_public = ObservationFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature=self.feature_public,
        )
        self.observation_public_feature_public_open_data = ObservationFactory(
            protection_level=PROTECTION_LEVELS['PUBLIC'],
            feature=self.feature_public_open_data,
        )

    def test_for_office_city_employee(self):
        qs = Observation.objects.for_office_city_employee()
        expected_queryset = [
            repr(self.observation_office_feature_office_city_employee),
            repr(self.observation_office_feature_office_non_city_employee),
            repr(self.observation_public_feature_office),
            repr(self.observation_public_feature_public),
            repr(self.observation_public_feature_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_for_office_non_city_employee(self):
        qs = Observation.objects.for_office_non_city_employee()
        expected_queryset = [
            repr(self.observation_office_feature_office_non_city_employee),
            repr(self.observation_public_feature_office),
            repr(self.observation_public_feature_public),
            repr(self.observation_public_feature_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_for_public(self):
        qs = Observation.objects.for_public()
        expected_queryset = [
            repr(self.observation_public_feature_public),
            repr(self.observation_public_feature_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)

    def test_open_data(self):
        qs = Observation.objects.open_data()
        expected_queryset = [
            repr(self.observation_public_feature_public_open_data),
        ]
        self.assertQuerysetEqual(qs, expected_queryset, ordered=False)


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

    def test_feature_is_square(self):
        with patch('nature.models.FeatureClass.is_square', new_callable=MagicMock(return_value=True)):
            self.assertTrue(self.feature.is_square)

    def test_feature_is_not_square(self):
        with patch('nature.models.FeatureClass.is_square', new_callable=MagicMock(return_value=False)):
            self.assertFalse(self.feature.is_square)

    def test_text_display(self):
        self.feature.text = 'text field is set'
        self.assertEqual(self.feature.text_display, 'text field is set')

        self.feature.text_www = 'text_www field is set'
        self.assertEqual(self.feature.text_display, 'text_www field is set')


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
        self.feature_class.super_class = FeatureClassFactory(id=FeatureClass.PROTECTED_SUPER_CLASS_ID)
        self.assertTrue(self.feature_class.is_protected)

    def test_feature_class_is_not_protected(self):
        self.assertFalse(self.feature_class.is_protected)

        self.feature_class.super_class = FeatureClassFactory()
        self.assertFalse(self.feature_class.is_protected)

    def test_feature_class_is_square(self):
        self.feature_class.super_class = FeatureClassFactory(id=FeatureClass.SQUARE_SUPER_CLASS_ID)
        self.assertTrue(self.feature_class.is_square)

    def test_feature_class_is_not_square(self):
        self.assertFalse(self.feature_class.is_square)

        self.feature_class.super_class = FeatureClassFactory()
        self.assertFalse(self.feature_class.is_square)


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
        self.protection = ProtectionFactory()

    def test__str__(self):
        self.assertEqual(self.protection.__str__(), str(self.protection.id))


class TestCriterion(TestCase):

    def setUp(self):
        self.criterion = CriterionFactory(criterion='criterion')

    def test__str__(self):
        self.assertEqual(self.criterion.__str__(), 'criterion')

        self.criterion.subcriterion = 'subcriterion'
        self.assertEqual(self.criterion.__str__(), 'criterion, subcriterion')

        self.criterion.specific_criterion = 'specific_criterion'
        self.assertEqual(self.criterion.__str__(), 'criterion, specific_criterion, subcriterion')


class TestTransaction(TestCase):

    def setUp(self):
        self.transaction = TransactionFactory(register_id='transaction')

    def test__str__(self):
        activate('en')
        self.assertEqual(self.transaction.__str__(), 'Transaction #{0}'.format(self.transaction.id))

        self.transaction.description = 'test description'
        self.assertEqual(self.transaction.__str__(), 'test description')


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
