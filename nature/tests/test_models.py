from django.test import TestCase

from ..models import Origin


class TestOrigin(TestCase):

    def setUp(self):
        self.origin = Origin()

    def test_smoke(self):
        pass
