from django.db import models


class FakeFeatureClassProtectionLevelOpenDataModel(models.Model):
    feature_class = models.CharField()
    protection_level = models.BooleanField()
    open_data = models.BooleanField()

    class Meta:
        abstract = True


class FakeFeatureClassProtectionLevelModel(models.Model):
    feature_class = models.CharField()
    protection_level = models.BooleanField()

    class Meta:
        abstract = True


class FakeFeatureClassModel(models.Model):
    feature_class = models.CharField()

    class Meta:
        abstract = True


class FakeProtectionLevelModel(models.Model):
    protection_level = models.IntegerField()

    class Meta:
        abstract = True


class FakeFeatureModel(models.Model):
    feature = models.CharField()

    class Meta:
        abstract = True


class FakeOpenDataModel(models.Model):
    open_data = models.BooleanField()

    class Meta:
        abstract = True
