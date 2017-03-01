# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.gis.db import models


class Permission:
    ADMIN_ONLY = 0
    ADMIN_AND_STAFF = 1
    PUBLIC = 2


PERMISSIONS = (
    (Permission.ADMIN_ONLY, "Administrators only"),
    (Permission.ADMIN_AND_STAFF, "Administrators and staff"),
    (Permission.PUBLIC, "Public"),
)


class NatureModel(models.Model):

    def __str__(self):
        try:
            return str(self.name)
        except AttributeError:
            try:
                return str(self.id)
            except AttributeError:
                return super().__str__(self)

    class Meta:
        abstract = True


# These seem to be the standard building blocks of most ltj tables


class ProtectedNatureModel(NatureModel):
    protection_level = models.ForeignKey('ProtectionLevel', models.PROTECT, db_column='suojaustasoid')

    class Meta:
        abstract = True


class Category(NatureModel):
    id = models.IntegerField(primary_key=True)
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selitys')

    def __str__(self):
        return str(self.explanation)

    class Meta:
        abstract = True


class CategoryWithSource(Category):
    source = models.CharField(max_length=50, blank=True, null=True, db_column='lahde')

    class Meta:
        abstract = True


class Type(NatureModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True, db_column='nimi')

    class Meta:
        abstract = True

# Now, for the actual data


class Origin(CategoryWithSource):

    class Meta:
        managed = False
        db_table = 'alkupera'


class Value(NatureModel):
    id = models.IntegerField(primary_key=True)
    explanation = models.CharField(max_length=50, blank=True, null=True, db_column='selite')
    type = models.CharField(max_length=10, blank=True, null=True, db_column='luokka')
    valuator = models.CharField(max_length=50, blank=True, null=True, db_column='arvottaja')
    date = models.DateField(blank=True, null=True, db_column='pvm')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')

    class Meta:
        managed = False
        db_table = 'arvo'


class ValueFeature(NatureModel):
    value_id = models.ForeignKey(Value, models.CASCADE, db_column='arvoid')
    feature_id = models.ForeignKey('Feature', models.CASCADE, db_column='kohdeid')

    class Meta:
        managed = False
        db_table = 'arvo_kohde'
        unique_together = (('value_id', 'feature_id'),)


class Occurrence(Category):

    class Meta:
        managed = False
        db_table = 'esiintyma'


class ObservationSeries(NatureModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, db_column='nimi')
    person = models.ForeignKey('Person', models.PROTECT, blank=True, null=True, db_column='hloid', related_name='observation_series')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    start_date = models.DateField(blank=True, null=True, db_column='alkupvm')
    end_date = models.DateField(blank=True, null=True, db_column='loppupvm')
    method = models.CharField(max_length=255, blank=True, null=True, db_column='menetelma')
    notes = models.CharField(max_length=255, blank=True, null=True, db_column='huomioitavaa')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    valid = models.BooleanField(db_column='voimassa')

    class Meta:
        managed = False
        db_table = 'havaintosarja'


class Person(NatureModel):
    id = models.IntegerField(primary_key=True)
    surname = models.CharField(max_length=25, blank=True, null=True, db_column='sukunimi')
    first_name = models.CharField(max_length=25, blank=True, null=True, db_column='etunimi')
    expertise = models.CharField(max_length=150, blank=True, null=True, db_column='asiantuntemus')
    notes = models.CharField(max_length=255, blank=True, null=True, db_column='huomioitavaa')
    company = models.CharField(max_length=100, blank=True, null=True, db_column='yritys')
    public_servant = models.BooleanField(db_column='viranomainen')
    telephone = models.CharField(max_length=50, blank=True, null=True, db_column='puhnro')
    email = models.CharField(max_length=100, blank=True, null=True, db_column='email')
    created_time = models.DateTimeField(blank=True, null=True, db_column='lisaysaika')

    class Meta:
        managed = False
        db_table = 'henkilo'


class Publication(NatureModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True, null=True, db_column='nimi')
    author = models.CharField(max_length=100, blank=True, null=True, db_column='tekija')
    series = models.CharField(max_length=100, blank=True, null=True, db_column='sarja')
    place_of_printing = models.CharField(max_length=50, blank=True, null=True, db_column='painopaikka')
    year = models.CharField(max_length=50, blank=True, null=True, db_column='vuosi')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    publication_type = models.ForeignKey('PublicationType', models.PROTECT, db_column='julktyyppiid', related_name='publications')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')

    class Meta:
        managed = False
        db_table = 'julkaisu'


class PublicationType(Type):

    class Meta:
        managed = False
        db_table = 'julktyyppi'


class Feature(ProtectedNatureModel):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=10, blank=True, null=True, db_column='tunnus')
    feature_class = models.ForeignKey('FeatureClass', models.PROTECT, db_column='luokkatunnus', related_name='features')
    geometry1 = models.GeometryField()
    name = models.CharField(max_length=80, blank=True, null=True, db_column='nimi')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    notes = models.CharField(max_length=255, blank=True, null=True, db_column='huom')
    active = models.BooleanField(db_column='voimassa')
    created_time = models.DateField(blank=True, null=True, db_column='digipvm')
    number = models.IntegerField(blank=True, null=True, db_column='numero')
    created_by = models.CharField(max_length=50, blank=True, null=True, db_column='digitoija')
    last_modified_time = models.DateTimeField(blank=True, null=True, db_column='pvm_editoitu')
    last_modified_by = models.CharField(max_length=10, blank=True, null=True, db_column='muokkaaja')
    area = models.FloatField(blank=True, null=True, db_column='pinta_ala')
    text = models.CharField(max_length=4000, blank=True, null=True, db_column='teksti')
    text_www = models.CharField(max_length=4000, blank=True, null=True, db_column='teksti_www')
    values = models.ManyToManyField('Value', through=ValueFeature, related_name='features')
    publications = models.ManyToManyField('Publication', through='FeaturePublication', related_name='features')

    class Meta:
        managed = False
        db_table = 'kohde'


class HistoricalFeature(Feature):
    archived_time = models.DateTimeField(db_column='historia_pvm')
    feature = models.ForeignKey(Feature, models.SET_NULL, db_column='kohde_id', blank=True, null=True, related_name='historical_features')

    class Meta:
        managed = False
        db_table = 'kohde_historia'


class FeaturePublication(NatureModel):
    feature_id = models.ForeignKey(Feature, models.CASCADE, db_column='kohdeid')
    publication_id = models.ForeignKey(Publication, models.CASCADE, db_column='julkid')

    class Meta:
        managed = False
        db_table = 'kohde_julk'
        unique_together = (('feature_id', 'publication_id'),)


class FeatureLink(ProtectedNatureModel):
    id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature, models.CASCADE, db_column='tekstiid', related_name='links')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')
    text = models.CharField(max_length=4000, blank=True, null=True, db_column='linkkiteksti')
    type = models.ForeignKey('LinkType', models.PROTECT, db_column='tyyppiid')
    ordering = models.IntegerField(blank=True, null=True, db_column='jarjestys')
    link_text = models.CharField(max_length=1000, blank=True, null=True, db_column='linkin_teksti')

    class Meta:
        managed = False
        db_table = 'kohdelinkki'


class SpeciesRegulation(NatureModel):
    species_id = models.ForeignKey('Species', models.CASCADE, db_column='lajid')
    regulation_id = models.ForeignKey('Regulation', models.CASCADE, db_column='saaid')

    class Meta:
        managed = False
        db_table = 'laj_saa'
        unique_together = (('species_id', 'regulation_id'),)


class Observation(ProtectedNatureModel):
    id = models.IntegerField(primary_key=True)
    location = models.ForeignKey(Feature, models.PROTECT, db_column='kohdeid', related_name='observations')
    species = models.ForeignKey('Species', models.PROTECT, db_column='lajid', related_name='observations')
    series = models.ForeignKey(ObservationSeries, models.PROTECT, db_column='hsaid', blank=True, null=True, related_name='observations')
    abundance = models.ForeignKey('Abundance', models.PROTECT, db_column='runsausid', blank=True, null=True, related_name='observations')
    incidence = models.ForeignKey('Incidence', models.PROTECT, db_column='yleisyysid', blank=True, null=True, related_name='observations')
    observer = models.ForeignKey(Person, models.PROTECT, db_column='hloid', blank=True, null=True, related_name='observations')
    number = models.CharField(max_length=30, blank=True, null=True, db_column='lkm')
    mobility = models.ForeignKey('Mobility', models.PROTECT, db_column='liikkumislkid', blank=True, null=True, related_name='observations')
    origin = models.ForeignKey(Origin, models.PROTECT, db_column='alkuperaid', blank=True, null=True, related_name='observations')
    breeding_category = models.ForeignKey('BreedingCategory', models.PROTECT, db_column='pesimisvarmuusid', blank=True, null=True, related_name='observations')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    notes = models.CharField(max_length=100, blank=True, null=True, db_column='huom')
    date = models.DateField(blank=True, null=True, db_column='pvm')
    occurrence = models.ForeignKey(Occurrence, models.PROTECT, db_column='esiintymaid', blank=True, null=True)
    created_time = models.DateTimeField(db_column='pvm_luotu')
    last_modified_time = models.DateTimeField(blank=True, null=True, db_column='pvm_editoitu')

    class Meta:
        managed = False
        db_table = 'lajihavainto'


class Species(ProtectedNatureModel):
    id = models.IntegerField(primary_key=True)
    taxon = models.CharField(max_length=5, blank=True, null=True, db_column='ryhma')
    taxon_1 = models.CharField(max_length=50, blank=True, null=True, db_column='elioryhma1')
    taxon_2 = models.CharField(max_length=50, blank=True, null=True, db_column='elioryhma2')
    order_fi = models.CharField(max_length=150, blank=True, null=True, db_column='lahko_suomi')
    order_la = models.CharField(max_length=150, blank=True, null=True, db_column='lahko_tiet')
    family_fi = models.CharField(max_length=150, blank=True, null=True, db_column='heimo_suomi')
    family_la = models.CharField(max_length=150, blank=True, null=True, db_column='heimo_tiet')
    name_fi_1 = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_suomi1')
    name_fi_2 = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_suomi2')
    name_la_1 = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_tiet1')
    name_la_2 = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_tiet2')
    subspecies_1 = models.CharField(max_length=150, blank=True, null=True, db_column='alalaji1')
    subspecies_2 = models.CharField(max_length=150, blank=True, null=True, db_column='alalaji2')
    author_1 = models.CharField(max_length=150, blank=True, null=True, db_column='auktori1')
    author_2 = models.CharField(max_length=150, blank=True, null=True, db_column='auktori2')
    name_abbreviated_1 = models.CharField(max_length=10, blank=True, null=True, db_column='nimilyhenne1')
    name_abbreviated_2 = models.CharField(max_length=10, blank=True, null=True, db_column='nimilyhenne2')
    name_sv = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_ruotsi')
    name_en = models.CharField(max_length=150, blank=True, null=True, db_column='nimi_englanti')
    registry_date = models.DateTimeField(blank=True, null=True, db_column='rekisteripvm')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    code = models.CharField(max_length=20, blank=True, null=True, db_column='koodi')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')
    regulations = models.ManyToManyField('Regulation', through=SpeciesRegulation, related_name='species')

    class Meta:
        managed = False
        db_table = 'lajirekisteri'


class Mobility(CategoryWithSource):
    value = models.IntegerField(blank=True, null=True, db_column='arvo')

    class Meta:
        managed = False
        db_table = 'liikkumislk'


class LinkType(Type):

    class Meta:
        managed = False
        db_table = 'linkkityyppi'


class HabitatTypeRegulation(NatureModel):
    habitat_type_id = models.ForeignKey('HabitatType', models.CASCADE, db_column='ltyyppiid')
    regulation_id = models.ForeignKey('Regulation', models.CASCADE, db_column='saadosid')

    class Meta:
        managed = False
        db_table = 'ltyyppi_saados'
        unique_together = (('habitat_type_id', 'regulation_id'),)


class HabitatTypeObservation(NatureModel):
    id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature, models.PROTECT, db_column='kohdeid', related_name='habitat_type_observations')
    habitat_type = models.ForeignKey('HabitatType', models.PROTECT, db_column='ltyypid', related_name='habitat_type_observations')
    group_fraction = models.IntegerField(blank=True, null=True, db_column='osuus_kuviosta')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    observation_series = models.ForeignKey(ObservationSeries, models.PROTECT, db_column='hsaid', related_name='habitat_type_observations')
    created_time = models.DateTimeField(db_column='pvm_luotu')
    last_modified_time = models.DateTimeField(blank=True, null=True, db_column='pvm_editoitu')

    class Meta:
        managed = False
        db_table = 'ltyyppihavainto'


class HabitatType(NatureModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, db_column='nimi')
    code = models.CharField(max_length=10, blank=True, null=True, db_column='koodi')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    group = models.CharField(max_length=50, blank=True, null=True, db_column='ltyyppiryhma')
    regulations = models.ManyToManyField('Regulation', through=HabitatTypeRegulation, related_name='habitat_types')

    class Meta:
        managed = False
        db_table = 'ltyyppirekisteri'


class FeatureClass(NatureModel):
    id = models.CharField(primary_key=True, max_length=10, db_column='tunnus')
    name = models.CharField(max_length=50, blank=True, null=True, db_column='nimi')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    super_class = models.ForeignKey('FeatureClass', models.PROTECT, blank=True, null=True, db_column='paatunnus', related_name='subclasses')
    reporting = models.BooleanField(db_column='raportointi')
    www = models.BooleanField()
    metadata = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'luokka'


class BreedingCategory(CategoryWithSource):
    value = models.CharField(max_length=50, blank=True, null=True, db_column='arvo')

    class Meta:
        managed = False
        db_table = 'pesimisvarmuus'


class Abundance(CategoryWithSource):
    value = models.CharField(max_length=5, blank=True, null=True, db_column='arvo')

    class Meta:
        managed = False
        db_table = 'runsaus'


class Tile(NatureModel):
    id = models.OneToOneField(Feature, models.CASCADE, db_column='id', primary_key=True, related_name='tile')
    number = models.CharField(max_length=10, blank=True, null=True, db_column='nro')
    degree_of_determination = models.IntegerField(blank=True, null=True, db_column='selvitysaste')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')

    class Meta:
        managed = False
        db_table = 'ruutu'


class Regulation(NatureModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True, db_column='nimi')
    paragraph = models.CharField(max_length=100, blank=True, null=True, db_column='pykala')
    additional_info = models.CharField(max_length=255, blank=True, null=True, db_column='lisatieto')
    value = models.CharField(max_length=10, blank=True, null=True, db_column='arvo')
    value_explanation = models.CharField(max_length=255, blank=True, null=True, db_column='arvon_selitys')
    valid = models.BooleanField(db_column='voimassa')
    date_of_entry = models.DateTimeField(blank=True, null=True, db_column='voimaantulo')
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')

    class Meta:
        managed = False
        db_table = 'saados'


class ConservationProgramme(Type):

    class Meta:
        managed = False
        db_table = 'sohjelma'


class ProtectionCriterion(NatureModel):
    criterion_id = models.ForeignKey('Criterion', models.CASCADE, db_column='perusteid')
    protection_id = models.ForeignKey('Protection', models.CASCADE, db_column='suoid')

    class Meta:
        managed = False
        db_table = 'suo_peruste'
        unique_together = (('criterion_id', 'protection_id'),)


class ProtectionLevel(Category):

    class Meta:
        managed = False
        db_table = 'suojaustaso'


class Protection(NatureModel):
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
        managed = False
        db_table = 'suojelu'


class ProtectionConservationProgramme(NatureModel):
    protection_id = models.ForeignKey(Protection, models.CASCADE, db_column='suojeluid')
    conservation_programme_id = models.ForeignKey(ConservationProgramme, models.CASCADE, db_column='sohjelmaid')

    class Meta:
        managed = False
        db_table = 'suojelu_sohjelma'
        unique_together = (('protection_id', 'conservation_programme_id'),)


class Criterion(NatureModel):
    id = models.IntegerField(primary_key=True)
    criterion = models.CharField(max_length=50, blank=True, null=True, db_column='peruste')
    specific_criterion = models.CharField(max_length=50, blank=True, null=True, db_column='tarkperuste')
    subcriterion = models.CharField(max_length=50, blank=True, null=True, db_column='alaperuste')

    class Meta:
        managed = False
        db_table = 'suoperuste'


class EventRegulation(NatureModel):
    event_id = models.ForeignKey('Event', models.CASCADE, db_column='tapid')
    regulation_id = models.ForeignKey(Regulation, models.CASCADE, db_column='saaid')

    class Meta:
        managed = False
        db_table = 'tap_saados'
        unique_together = (('event_id', 'regulation_id'),)


class Event(ProtectedNatureModel):
    id = models.IntegerField(primary_key=True)
    register_id = models.CharField(max_length=20, blank=True, null=True, db_column='diaarinro')
    description = models.CharField(max_length=255, blank=True, null=True, db_column='kuvaus')
    type = models.ForeignKey('EventType', models.PROTECT, db_column='tapahtumatyyppiid')
    last_modified_by = models.CharField(max_length=20, blank=True, null=True, db_column='paivittaja')
    date = models.DateField(blank=True, null=True, db_column='pvm')
    person = models.ForeignKey(Person, models.PROTECT, db_column='hloid', blank=True, null=True)
    link = models.CharField(max_length=4000, blank=True, null=True, db_column='linkki')
    features = models.ManyToManyField(Feature, through='EventFeature', related_name='events')
    regulations = models.ManyToManyField(Regulation, through='EventRegulation', related_name='events')

    class Meta:
        managed = False
        db_table = 'tapahtuma'


class EventFeature(NatureModel):
    feature_id = models.ForeignKey(Feature, models.CASCADE, db_column='kohdeid')
    event_id = models.ForeignKey(Event, models.CASCADE, db_column='tapid')

    class Meta:
        managed = False
        db_table = 'tapahtuma_kohde'
        unique_together = (('feature_id', 'event_id'),)


class EventType(Type):

    class Meta:
        managed = False
        db_table = 'tapahtumatyyppi'


class Incidence(CategoryWithSource):
    value = models.CharField(max_length=5, blank=True, null=True, db_column='arvo')

    class Meta:
        managed = False
        db_table = 'yleisyys'
