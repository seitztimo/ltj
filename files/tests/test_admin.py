import os

from django.contrib.admin import AdminSite
from django.test import TestCase, RequestFactory

from nature.tests.utils import make_user
from .factories import FileFactory
from ..admin import FileAdmin
from ..models import File


class TestFileAdmin(TestCase):

    def setUp(self):
        self.user = make_user()
        self.site = AdminSite()
        self.factory = RequestFactory()

    def test_save_model(self):
        file_admin = FileAdmin(File, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        # test creating new file instance
        file = FileFactory.build()
        file_admin.save_model(request, file, None, None)
        self.assertEqual(file.created_by, self.user)
        self.assertEqual(file.last_modified_by, self.user)

        # test updating existing file instance
        new_user = make_user(username='new-user')
        request.user = new_user
        file_admin.save_model(request, file, None, None)
        self.assertEqual(file.created_by, self.user)
        self.assertEqual(file.last_modified_by, new_user)

        os.remove(file.file.path)

    def test_get_queryset(self):
        file_admin = FileAdmin(File, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        file_admin.get_queryset(request)
        self.assertEqual(file_admin.request, request)

    def test_url(self):
        file_admin = FileAdmin(File, self.site)
        request = self.factory.get('/fake-url/')
        request.user = self.user

        file = FileFactory.build()
        file_admin.get_queryset(request)
        self.assertEqual(file_admin.url(file), request.build_absolute_uri(file.file.url))
