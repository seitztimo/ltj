from django.test import TestCase

from .factories import FeatureFactory, CriterionFactory, ConservationProgrammeFactory
from ..forms import ProtectionInlineForm


class TestProtectionInlineForm(TestCase):
    def setUp(self):
        self.feature = FeatureFactory()
        self.criteria_1 = CriterionFactory()
        self.criteria_2 = CriterionFactory()
        self.conservation_programme_1 = ConservationProgrammeFactory()
        self.conservation_programme_2 = ConservationProgrammeFactory()

    def test_save(self):
        form_data = {
            "id": self.feature.id,
            "reported_area": "Test reported area",
            "criteria": [
                self.criteria_1.id,
                self.criteria_2.id,
            ],
            "conservation_programmes": [
                self.conservation_programme_1.id,
                self.conservation_programme_2.id,
            ],
        }
        form = ProtectionInlineForm(form_data)
        self.assertTrue(form.is_valid())

        protection = form.save()
        self.assertEqual(protection.criteria.count(), 2)
        self.assertEqual(protection.conservation_programmes.count(), 2)
