import os
import zipfile
import shapefile
from django.conf import settings

from ..importers import SHAPEFILE_FIELD_MAPPING


class ZippedShapefilesGenerator:
    """A helper class to generate zipped shapefiles for given features"""
    shape_fields = [
        ['id', 'N', 10, 0],
        ['tunnus', 'C', 10, 0],
        ['luokkatunn', 'C', 10, 0],
        ['nimi', 'C', 80, 0],
        ['kuvaus', 'C', 254, 0],
        ['huom', 'C', 254, 0],
        ['voimassa', 'C', 254, 0],
        ['digipvm', 'D', 8, 0],
        ['numero', 'N', 10, 0],
        ['digitoija', 'C', 50, 0],
        ['suojaustas', 'N', 10, 0],
        ['pvm_editoi', 'C', 24, 0],
        ['muokkaaja', 'C', 10, 0],
        ['pinta_ala', 'N', 24, 15],
    ]

    @classmethod
    def create_shapefiles(cls, features):
        with zipfile.ZipFile(settings.MEDIA_ROOT + '/shapefiles/testshapefiles.zip', 'w') as zfile:
            shapefiles = ['{}.{}'.format(zfile.filename.split('.')[0], ext) for ext in ['shp', 'shx', 'dbf']]
            for shp_file in shapefiles:
                shp_writer = shapefile.Writer(shp_file, shapeType=shapefile.POINT)
                shp_writer.fields = cls.shape_fields
                for feature in features:
                    shp_writer.point(*feature.geometry)
                    shp_writer.record(*cls._get_record(feature))
                shp_writer.close()
                zfile.write(shp_file, shp_file.split('/')[-1])
            zfile.close()
            for shp_file in shapefiles:
                os.remove(shp_file)
        return zfile.filename

    @classmethod
    def _get_record(cls, feature):
        shape_field_names = [shape_field[0] for shape_field in cls.shape_fields]
        return [getattr(feature, SHAPEFILE_FIELD_MAPPING[field_name]) for field_name in shape_field_names]
