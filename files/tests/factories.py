import factory


class FileFactory(factory.django.DjangoModelFactory):
    file = factory.django.FileField(filename='testfile')

    class Meta:
        model = 'files.File'
