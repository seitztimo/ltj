# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSException


class ProtectionLevelEnabledQuerySet(models.QuerySet):
    """Custom queryset to filter protection level enabled queryset based on user roles"""

    def for_admin(self):
        """ADMIN have access to all objects"""
        return self

    def for_admin_and_staff(self):
        """ADMIN_AND_STAFF have access to objects of which the protection level is PUBLIC or ADMIN_AND_STAFF"""
        return self.filter(protection_level__in=[ProtectionLevelMixin.PUBLIC, ProtectionLevelMixin.ADMIN_AND_STAFF])

    def for_public(self):
        """PUBLIC have access to objects of which the protection level is PUBLIC"""
        return self.filter(protection_level=ProtectionLevelMixin.PUBLIC)


class ProtectionLevelMixin(models.Model):
    ADMIN_ONLY = 1
    ADMIN_AND_STAFF = 2
    PUBLIC = 3

    PROTECTION_LEVEL_CHOICES = (
        (ADMIN_ONLY, "Administrators only"),
        (ADMIN_AND_STAFF, "Administrators and staff"),
        (PUBLIC, "Public"),
    )

    protection_level = models.IntegerField(choices=PROTECTION_LEVEL_CHOICES, default=PUBLIC, db_column='suojaustasoid')

    objects = ProtectionLevelEnabledQuerySet.as_manager()

    class Meta:
        abstract = True


class PermissiveGeometryField(models.GeometryField):
    """
    Required to catch exceptions if curved geometries are encountered. Currently, the GEOS library, GeoDjango
    and GeoJSON do not support curved geometries.
    """

    def from_db_value(self, value, expression, connection, context):
        try:
            value = super().from_db_value(value, expression, connection, context)
        except GEOSException:
            value = None
        return value


class Origin(models.Model):
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selitys')
    source = models.CharField(max_length=50, blank=True, null=True, db_column='lahde')

    class Meta:
        ordering = ['id']
        db_table = 'alkupera'

    def __str__(self):
        return str(self.explanation)


class Value(models.Model):
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selite')
    value_type = models.CharField(max_length=10, blank=True, null=True, db_column='luokka')
    valuator = models.CharField(max_length=50, blank=True, null=True, db_column='arvottaja')
    date = models.DateField(blank=True, null=True, db_column='pvm')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')

    class Meta:
        ordering = ['id']
        db_table = 'arvo'

    def __str__(self):
        return str(self.explanation)


class ValueFeature(models.Model):
    """Through model for Value & Feature m2m relation"""
    value = models.ForeignKey(Value, models.CASCADE, db_column='arvoid')
    feature = models.ForeignKey('Feature', models.CASCADE, db_column='kohdeid')

    class Meta:
        db_table = 'arvo_kohde'
        unique_together = (('value', 'feature'),)


class Occurrence(models.Model):
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selitys')

    class Meta:
        ordering = ['id']
        db_table = 'esiintyma'

    def __str__(self):
        return str(self.explanation)


class ObservationSeries(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, db_column='nimi')
    person = models.ForeignKey('Person', models.PROTECT, blank=True, null=True, db_column='hloid',
                               related_name='observation_series')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    start_date = models.DateField(blank=True, null=True, db_column='alkupvm')
    end_date = models.DateField(blank=True, null=True, db_column='loppupvm')
    method = models.CharField(max_length=255, blank=True, null=True, db_column='menetelma')
    notes = models.CharField(max_length=255, blank=True, null=True, db_column='huomioitavaa')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    valid = models.BooleanField(db_column='voimassa')

    class Meta:
        ordering = ['id']
        db_table = 'havaintosarja'
        verbose_name = 'observation series'
        verbose_name_plural = 'observation series'

    def __str__(self):
        return self.name or 'Observation series {0}'.format(self.id)


class Person(models.Model):
    surname = models.CharField(max_length=25, blank=True, null=True, db_column='sukunimi')
    first_name = models.CharField(max_length=25, blank=True, null=True, db_column='etunimi')
    expertise = models.CharField(max_length=150, blank=True, null=True, db_column='asiantuntemus')
    notes = models.CharField(max_length=255, blank=True, null=True, db_column='huomioitavaa')
    company = models.CharField(max_length=100, blank=True, null=True, db_column='yritys')
    public_servant = models.BooleanField(db_column='viranomainen')
    telephone = models.CharField(max_length=50, blank=True, null=True, db_column='puhnro')
    email = models.CharField(max_length=100, blank=True, null=True, db_column='email')
    created_time = models.DateTimeField(blank=True, null=True, auto_now_add=True, db_column='lisaysaika')

    class Meta:
        ordering = ['id']
        db_table = 'henkilo'

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.surname)


class Publication(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True, db_column='nimi')
    author = models.CharField(max_length=100, blank=True, null=True, db_column='tekija')
    series = models.CharField(max_length=100, blank=True, null=True, db_column='sarja')
    place_of_printing = models.CharField(max_length=50, blank=True, null=True, db_column='painopaikka')
    year = models.CharField(max_length=50, blank=True, null=True, db_column='vuosi')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    publication_type = models.ForeignKey('PublicationType', models.PROTECT, db_column='julktyyppiid',
                                         related_name='publications')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')

    class Meta:
        ordering = ['id']
        db_table = 'julkaisu'
        verbose_name = 'publication'
        verbose_name_plural = 'publications'

    def __str__(self):
        return str(self.name)


class PublicationType(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, db_column='nimi')

    class Meta:
        ordering = ['id']
        db_table = 'julktyyppi'

    def __str__(self):
        return str(self.name)


class ProtectedFeatureQueryset(ProtectionLevelEnabledQuerySet):

    def open_data(self):
        return self.filter(feature_class__open_data=True)


class AbstractFeature(ProtectionLevelMixin, models.Model):
    """AbstractFeature model that provides common fields for Feature and HistoricalFeature """
    fid = models.CharField(max_length=10, blank=True, null=True, db_column='tunnus')
    geometry = PermissiveGeometryField(db_column='geometry1', srid=settings.SRID)
    name = models.CharField(max_length=80, blank=True, null=True, db_column='nimi')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    notes = models.CharField(max_length=255, blank=True, null=True, db_column='huom')
    active = models.BooleanField(db_column='voimassa', default=True)
    created_time = models.DateField(blank=True, null=True, auto_now_add=True, db_column='digipvm')
    number = models.IntegerField(blank=True, null=True, db_column='numero')
    created_by = models.CharField(max_length=50, blank=True, null=True, db_column='digitoija')
    last_modified_time = models.DateTimeField(blank=True, null=True, auto_now=True, db_column='pvm_editoitu')
    last_modified_by = models.CharField(max_length=10, blank=True, null=True, db_column='muokkaaja')
    area = models.FloatField(verbose_name='Area (ha)', blank=True, null=True, editable=False, db_column='pinta_ala')
    text = models.CharField(max_length=40000, blank=True, null=True, db_column='teksti')
    text_www = models.CharField(max_length=40000, blank=True, null=True, db_column='teksti_www')

    objects = ProtectedFeatureQueryset.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.geometry and self.geometry.dims == 2:
            # save area for Polygon, MultiPolygon or GeometryCollection with Polygon
            # or MultiPolygon
            self.area = self.geometry.area / 10000  # area in hectare
        super().save(*args, **kwargs)

    @property
    def formatted_area(self):
        if not self.area:
            return 0.0
        return float("{0:.2f}".format(self.area))


class Feature(AbstractFeature):
    feature_class = models.ForeignKey('FeatureClass', models.PROTECT, db_column='luokkatunnus', related_name='features')
    values = models.ManyToManyField('Value', through=ValueFeature, related_name='features')
    publications = models.ManyToManyField('Publication', through='FeaturePublication', related_name='features')

    class Meta:
        ordering = ['id']
        db_table = 'kohde'
        verbose_name = 'feature'
        verbose_name_plural = 'features'

    def __str__(self):
        return self.name or 'Feature {0}'.format(self.id)


class HistoricalFeature(AbstractFeature):
    feature_class = models.ForeignKey('FeatureClass', models.PROTECT, db_column='luokkatunnus',
                                      related_name='historical_features')
    archived_time = models.DateTimeField(db_column='historia_pvm')
    feature = models.ForeignKey(Feature, models.SET_NULL, db_column='kohde_id', blank=True, null=True,
                                related_name='historical_features')

    class Meta:
        ordering = ['id']
        db_table = 'kohde_historia'

    def __str__(self):
        return self.name or 'Historical feature {0}'.format(self.id)


class FeaturePublication(models.Model):
    """Through model for Feature & Publication m2m relation"""
    feature = models.ForeignKey(Feature, models.CASCADE, db_column='kohdeid')
    publication = models.ForeignKey(Publication, models.CASCADE, db_column='julkid')

    class Meta:
        db_table = 'kohde_julk'
        unique_together = (('feature', 'publication'),)


class FeatureLink(ProtectionLevelMixin, models.Model):
    feature = models.ForeignKey(Feature, models.CASCADE, db_column='tekstiid', related_name='links')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')
    text = models.CharField(max_length=4000, blank=True, null=True, db_column='linkkiteksti')
    link_type = models.ForeignKey('LinkType', models.PROTECT, db_column='tyyppiid')
    ordering = models.IntegerField(blank=True, null=True, db_column='jarjestys')
    link_text = models.CharField(max_length=100, blank=True, null=True, db_column='linkin_teksti')

    class Meta:
        ordering = ['id']
        db_table = 'kohdelinkki'

    def __str__(self):
        return str(self.link)


class SpeciesRegulation(models.Model):
    """Through model for Species & Regulation m2m relation"""
    species = models.ForeignKey('Species', models.CASCADE, db_column='lajid')
    regulation = models.ForeignKey('Regulation', models.CASCADE, db_column='saaid')

    class Meta:
        db_table = 'laj_saa'
        unique_together = (('species', 'regulation'),)


class Observation(ProtectionLevelMixin, models.Model):
    code = models.CharField(max_length=100, blank=True, null=True, db_column='hav_koodi')
    # This field should be filled and unique, but we do not know the values yet, see details
    # in https://github.com/City-of-Helsinki/ltj/issues/4
    uri = models.URLField(blank=True)
    feature = models.ForeignKey(Feature, models.PROTECT, db_column='kohdeid', related_name='observations')
    species = models.ForeignKey('Species', models.PROTECT, db_column='lajid', related_name='observations')
    series = models.ForeignKey(ObservationSeries, models.PROTECT, db_column='hsaid', blank=True, null=True,
                               related_name='observations')
    abundance = models.ForeignKey('Abundance', models.PROTECT, db_column='runsausid', blank=True, null=True,
                                  related_name='observations')
    frequency = models.ForeignKey('Frequency', models.PROTECT, db_column='yleisyysid', blank=True, null=True,
                                  related_name='observations')
    observer = models.ForeignKey(Person, models.PROTECT, db_column='hloid', blank=True, null=True,
                                 related_name='observations')
    number = models.CharField(max_length=30, blank=True, null=True, db_column='lkm')
    local_or_migrating = models.ForeignKey('Mobility', models.PROTECT, db_column='liikkumislkid', blank=True, null=True,
                                           related_name='observations')
    origin = models.ForeignKey(Origin, models.PROTECT, db_column='alkuperaid', blank=True, null=True,
                               related_name='observations')
    breeding_degree = models.ForeignKey('BreedingDegree', models.PROTECT, db_column='pesimisvarmuusid', blank=True,
                                        null=True, related_name='observations')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    notes = models.CharField(max_length=100, blank=True, null=True, db_column='huom')
    date = models.DateField(blank=True, null=True, db_column='pvm')
    occurrence = models.ForeignKey(Occurrence, models.PROTECT, db_column='esiintymaid', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, db_column='pvm_luotu')
    last_modified_time = models.DateTimeField(blank=True, null=True, auto_now=True, db_column='pvm_editoitu')

    class Meta:
        ordering = ['id']
        db_table = 'lajihavainto'

    def __str__(self):
        return self.code or 'Observation {0}'.format(self.id)


class Species(ProtectionLevelMixin, models.Model):
    taxon = models.CharField(max_length=5, blank=True, null=True, db_column='ryhma')
    taxon_1 = models.CharField(max_length=50, blank=True, null=True, db_column='elioryhma1')
    taxon_2 = models.CharField(max_length=50, blank=True, null=True, db_column='elioryhma2')
    order_fi = models.CharField(max_length=150, blank=True, null=True, db_column='lahko_suomi')
    order_la = models.CharField(max_length=150, blank=True, null=True, db_column='lahko_tiet')
    family_fi = models.CharField(max_length=150, blank=True, null=True, db_column='heimo_suomi')
    family_la = models.CharField(max_length=150, blank=True, null=True, db_column='heimo_tiet')
    name_fi = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_suomi1')
    name_fi_2 = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_suomi2')
    name_sci_1 = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_tiet1')
    name_sci_2 = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_tiet2')
    name_subspecies_1 = models.CharField(max_length=150, blank=True, null=True, db_column='alalaji1')
    name_subspecies_2 = models.CharField(max_length=150, blank=True, null=True, db_column='alalaji2')
    author_1 = models.CharField(max_length=150, blank=True, null=True, db_column='auktori1')
    author_2 = models.CharField(max_length=150, blank=True, null=True, db_column='auktori2')
    name_abbreviated_1 = models.CharField(max_length=10, blank=True, null=True, db_column='nimilyhenne1')
    name_abbreviated_2 = models.CharField(max_length=10, blank=True, null=True, db_column='nimilyhenne2')
    name_sv = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_ruotsi')
    name_en = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_englanti')
    registry_date = models.DateTimeField(blank=True, null=True, db_column='rekisteripvm')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    code = models.CharField(max_length=100, blank=True, null=True, db_column='koodi')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')
    regulations = models.ManyToManyField('Regulation', through=SpeciesRegulation, related_name='species')

    class Meta:
        ordering = ['id']
        db_table = 'lajirekisteri'
        verbose_name = 'species'
        verbose_name_plural = 'species'

    def __str__(self):
        name_list = [self.name_fi, self.name_sci_1, self.name_subspecies_1]
        return ', '.join([name for name in name_list if name])


class Mobility(models.Model):
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selitys')
    source = models.CharField(max_length=50, blank=True, null=True, db_column='lahde')
    value = models.IntegerField(blank=True, null=True, db_column='arvo')

    class Meta:
        ordering = ['id']
        db_table = 'liikkumislk'

    def __str__(self):
        return str(self.explanation)


class LinkType(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, db_column='nimi')  # type name

    class Meta:
        ordering = ['id']
        db_table = 'linkkityyppi'
        verbose_name = 'link type'
        verbose_name_plural = 'link types'

    def __str__(self):
        return str(self.name)


class HabitatTypeRegulation(models.Model):
    """Through model for HabitatType & Regulation m2m relation"""
    habitat_type = models.ForeignKey('HabitatType', models.CASCADE, db_column='ltyyppiid')
    regulation = models.ForeignKey('Regulation', models.CASCADE, db_column='saadosid')

    class Meta:
        db_table = 'ltyyppi_saados'
        unique_together = (('habitat_type', 'regulation'),)


class HabitatTypeObservation(models.Model):
    feature = models.ForeignKey(Feature, models.PROTECT, db_column='kohdeid', related_name='habitat_type_observations')
    habitat_type = models.ForeignKey('HabitatType', models.PROTECT, db_column='ltyypid',
                                     related_name='habitat_type_observations')
    group_fraction = models.IntegerField(blank=True, null=True, db_column='osuus_kuviosta')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    observation_series = models.ForeignKey(ObservationSeries, models.PROTECT, db_column='hsaid',
                                           related_name='habitat_type_observations')
    created_time = models.DateTimeField(auto_now_add=True, db_column='pvm_luotu')
    last_modified_time = models.DateTimeField(blank=True, null=True, auto_now=True, db_column='pvm_editoitu')

    class Meta:
        ordering = ['id']
        db_table = 'ltyyppihavainto'

    def __str__(self):
        return '{0} {1}'.format(self.habitat_type, self.feature)


class HabitatType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, db_column='nimi')
    code = models.CharField(max_length=10, blank=True, null=True, db_column='koodi')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    group = models.CharField(max_length=50, blank=True, null=True, db_column='ltyyppiryhma')
    regulations = models.ManyToManyField('Regulation', through=HabitatTypeRegulation, related_name='habitat_types')

    class Meta:
        ordering = ['id']
        db_table = 'ltyyppirekisteri'

    def __str__(self):
        return str(self.name)


class ProtectedFeatureClassQueryset(models.QuerySet):

    def open_data(self):
        return self.filter(open_data=True)


class FeatureClass(models.Model):
    id = models.CharField(primary_key=True, max_length=10, db_column='tunnus')
    name = models.CharField(max_length=50, blank=True, null=True, db_column='nimi')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    super_class = models.ForeignKey('FeatureClass', models.PROTECT, blank=True, null=True, db_column='paatunnus',
                                    related_name='subclasses')
    reporting = models.BooleanField(db_column='raportointi', default=True)
    open_data = models.BooleanField(db_column='avoin_data', default=False)
    www = models.BooleanField(default=True)
    metadata = models.CharField(max_length=4000, blank=True, null=True)

    objects = ProtectedFeatureClassQueryset.as_manager()

    class Meta:
        ordering = ['id']
        db_table = 'luokka'
        verbose_name = 'feature class'
        verbose_name_plural = 'feature classes'

    def __str__(self):
        return self.name or 'Feature class {0}'.format(self.id)


class BreedingDegree(models.Model):
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selitys')
    source = models.CharField(max_length=50, blank=True, null=True, db_column='lahde')
    value = models.CharField(max_length=50, blank=True, null=True, db_column='arvo')

    class Meta:
        ordering = ['id']
        db_table = 'pesimisvarmuus'

    def __str__(self):
        return str(self.explanation)


class Abundance(models.Model):
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selitys')
    source = models.CharField(max_length=50, blank=True, null=True, db_column='lahde')
    value = models.CharField(max_length=5, blank=True, null=True, db_column='arvo')

    class Meta:
        ordering = ['id']
        db_table = 'runsaus'

    def __str__(self):
        return str(self.explanation)


class Square(models.Model):
    id = models.OneToOneField(Feature, models.CASCADE, db_column='id', primary_key=True, related_name='square')
    number = models.CharField(max_length=10, blank=True, null=True, db_column='nro')
    degree_of_determination = models.IntegerField(blank=True, null=True, db_column='selvitysaste')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')

    class Meta:
        ordering = ['id']
        db_table = 'ruutu'

    def __str__(self):
        return str(self.number)


class Regulation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, db_column='nimi')
    paragraph = models.CharField(max_length=100, blank=True, null=True, db_column='pykala')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    value = models.CharField(max_length=10, blank=True, null=True, db_column='arvo')
    value_explanation = models.CharField(max_length=255, blank=True, null=True, db_column='arvon_selitys')
    valid = models.BooleanField(db_column='voimassa')
    date_of_entry = models.DateTimeField(blank=True, null=True, db_column='voimaantulo')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')

    class Meta:
        ordering = ['id']
        db_table = 'saados'

    def __str__(self):
        return str(self.name)


class ConservationProgramme(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, db_column='nimi')

    class Meta:
        ordering = ['id']
        db_table = 'sohjelma'

    def __str__(self):
        return str(self.name)


class ProtectionCriterion(models.Model):
    """Through model for Protection & Criterion m2m relation """
    criterion = models.ForeignKey('Criterion', models.CASCADE, db_column='perusteid')
    protection = models.ForeignKey('Protection', models.CASCADE, db_column='suoid')

    class Meta:
        db_table = 'suo_peruste'
        unique_together = (('criterion', 'protection'),)


class ProtectionLevel(models.Model):
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selitys')

    class Meta:
        ordering = ['id']
        db_table = 'suojaustaso'

    def __str__(self):
        return str(self.explanation)


class Protection(models.Model):
    id = models.OneToOneField(Feature, models.CASCADE, db_column='id', primary_key=True, related_name='protection')
    reported_area = models.CharField(max_length=50, blank=True, null=True, db_column='ilmoitettu_pinta_ala')
    land_area = models.CharField(max_length=50, blank=True, null=True, db_column='maapinta_ala')
    water_area = models.CharField(max_length=50, blank=True, null=True, db_column='vesipinta_ala')
    hiking = models.CharField(max_length=255, blank=True, null=True, db_column='liikkuminen')
    regulations = models.CharField(max_length=255, blank=True, null=True, db_column='maaraykset')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    criteria = models.ManyToManyField('Criterion', through=ProtectionCriterion, related_name='protections')
    conservation_programmes = models.ManyToManyField('ConservationProgramme',
                                                     through='ProtectionConservationProgramme',
                                                     related_name='protections')

    class Meta:
        ordering = ['id']
        db_table = 'suojelu'

    def __str__(self):
        return str(self.reported_area)


class ProtectionConservationProgramme(models.Model):
    """Through model for Protection & ConservationProgramme m2m relation"""
    protection = models.ForeignKey(Protection, models.CASCADE, db_column='suojeluid')
    conservation_programme = models.ForeignKey(ConservationProgramme, models.CASCADE, db_column='sohjelmaid')

    class Meta:
        db_table = 'suojelu_sohjelma'
        unique_together = (('protection', 'conservation_programme'),)


class Criterion(models.Model):
    criterion = models.CharField(max_length=50, blank=True, null=True, db_column='peruste')
    specific_criterion = models.CharField(max_length=50, blank=True, null=True, db_column='tarkperuste')
    subcriterion = models.CharField(max_length=50, blank=True, null=True, db_column='alaperuste')

    class Meta:
        ordering = ['id']
        db_table = 'suoperuste'

    def __str__(self):
        return str(self.criterion)


class TransactionRegulation(models.Model):
    """Through model for Transaction & Regulation m2m relation"""
    transaction = models.ForeignKey('Transaction', models.CASCADE, db_column='tapid')
    regulation = models.ForeignKey(Regulation, models.CASCADE, db_column='saaid')

    class Meta:
        db_table = 'tap_saados'
        unique_together = (('transaction', 'regulation'),)


class Transaction(ProtectionLevelMixin, models.Model):
    register_id = models.CharField(max_length=20, blank=True, null=True, db_column='diaarinro')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    transaction_type = models.ForeignKey('TransactionType', models.PROTECT, db_column='tapahtumatyyppiid')
    last_modified_by = models.CharField(max_length=20, blank=True, null=True, db_column='paivittaja')
    date = models.DateField(blank=True, null=True, db_column='pvm')
    person = models.ForeignKey(Person, models.PROTECT, db_column='hloid', blank=True, null=True)
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')
    features = models.ManyToManyField(Feature, through='TransactionFeature', related_name='transactions')
    regulations = models.ManyToManyField(Regulation, through='TransactionRegulation', related_name='transactions')

    class Meta:
        ordering = ['id']
        db_table = 'tapahtuma'

    def __str__(self):
        return str(self.register_id)


class TransactionFeature(models.Model):
    """Through model for Transaction & Feature m2m relation"""
    feature = models.ForeignKey(Feature, models.CASCADE, db_column='kohdeid')
    transaction = models.ForeignKey(Transaction, models.CASCADE, db_column='tapid')

    class Meta:
        db_table = 'tapahtuma_kohde'
        unique_together = (('feature', 'transaction'),)


class TransactionType(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, db_column='nimi')

    class Meta:
        ordering = ['id']
        db_table = 'tapahtumatyyppi'

    def __str__(self):
        return str(self.name)


class Frequency(models.Model):
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selitys')
    source = models.CharField(max_length=50, blank=True, null=True, db_column='lahde')
    value = models.CharField(max_length=5, blank=True, null=True, db_column='arvo')

    class Meta:
        ordering = ['id']
        db_table = 'yleisyys'

    def __str__(self):
        return str(self.explanation)
