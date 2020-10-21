from collections import UserDict

from django.conf import settings
from django.contrib.gis.gdal import SpatialReference


class MockAttribute:
    def __init__(self, value):
        self.value = value


class MockFeature(UserDict):
    def __init__(self, data, ogr_geom):
        super().__init__(data)
        self.geom = ogr_geom


def create_mock_data_source(features):
    """
    Create a mock DataSource class that include the given features

    :param features: features to be included in the layer
    :return: A mock DataSource class
    """

    class MockLayer:
        def __init__(self):
            self.srs = SpatialReference(settings.SRID)
            self.fields = list(features[0].keys())
            self.mock_features = features

        def __iter__(self):
            yield from self.mock_features

        def __len__(self):
            return len(self.mock_features)

        def get_fields(self, field_name):
            return [feature.get(field_name).value for feature in self.mock_features]

    class MockDataSource:
        def __init__(self, ds_input):
            self.mock_layers = [MockLayer()]

        def __getitem__(self, index):
            return self.mock_layers[index]

    return MockDataSource


def create_mock_zip_file_class(filenames):
    """
    Create a mock ZipFile class
    :param filenames:  a list of files to be contained by zipfile instance
    :return: A mocked ZipFile class
    """

    class MockZipFile:
        def __init__(self, file):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def namelist(self):
            return filenames

        def extractall(self, path):
            pass

    return MockZipFile
