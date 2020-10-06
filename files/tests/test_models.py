import os

from django.test import TestCase

from nature.tests.utils import make_user
from .factories import FileFactory


class TestFile(TestCase):
    def setUp(self):
        user = make_user()
        self.file = FileFactory(uploaded_by=user, last_modified_by=user)

    def tearDown(self):
        os.remove(self.file.file.path)

    def test__str__(self):
        self.assertEqual(str(self.file), "files/testfile")
