import factory


class ShapefileImportFactory(factory.django.DjangoModelFactory):
    shapefiles = factory.django.FileField(filename='testshapefiles.zip')

    class Meta:
        model = 'imports.ShapefileImport'
