# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Alkupera(models.Model):
    id = models.IntegerField(primary_key=True)
    selitys = models.CharField(max_length=50, blank=True, null=True)
    lahde = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alkupera'


class Arvo(models.Model):
    id = models.IntegerField(primary_key=True)
    luokka = models.CharField(max_length=10, blank=True, null=True)
    selite = models.CharField(max_length=50, blank=True, null=True)
    arvottaja = models.CharField(max_length=50, blank=True, null=True)
    pvm = models.DateField(blank=True, null=True)
    linkki = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arvo'


class ArvoKohde(models.Model):
    arvoid = models.ForeignKey(Arvo, models.DO_NOTHING, db_column='arvoid')
    kohdeid = models.ForeignKey('Kohde', models.DO_NOTHING, db_column='kohdeid')

    class Meta:
        managed = False
        db_table = 'arvo_kohde'
        unique_together = (('arvoid', 'kohdeid'),)


class Esiintyma(models.Model):
    id = models.IntegerField(primary_key=True)
    selitys = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'esiintyma'


class Havaintosarja(models.Model):
    id = models.IntegerField(primary_key=True)
    nimi = models.CharField(max_length=50, blank=True, null=True)
    hloid = models.ForeignKey('Henkilo', models.DO_NOTHING, db_column='hloid', blank=True, null=True)
    kuvaus = models.CharField(max_length=255, blank=True, null=True)
    alkupvm = models.DateField(blank=True, null=True)
    loppupvm = models.DateField(blank=True, null=True)
    menetelma = models.CharField(max_length=255, blank=True, null=True)
    huomioitavaa = models.CharField(max_length=255, blank=True, null=True)
    lisatieto = models.CharField(max_length=255, blank=True, null=True)
    voimassa = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'havaintosarja'


class Henkilo(models.Model):
    id = models.IntegerField(primary_key=True)
    sukunimi = models.CharField(max_length=25, blank=True, null=True)
    etunimi = models.CharField(max_length=25, blank=True, null=True)
    asiantuntemus = models.CharField(max_length=150, blank=True, null=True)
    huomioitavaa = models.CharField(max_length=255, blank=True, null=True)
    yritys = models.CharField(max_length=100, blank=True, null=True)
    viranomainen = models.BooleanField()
    puhnro = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    lisaysaika = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'henkilo'


class Julkaisu(models.Model):
    id = models.IntegerField(primary_key=True)
    nimi = models.CharField(max_length=150, blank=True, null=True)
    tekija = models.CharField(max_length=100, blank=True, null=True)
    sarja = models.CharField(max_length=100, blank=True, null=True)
    painopaikka = models.CharField(max_length=50, blank=True, null=True)
    vuosi = models.CharField(max_length=50, blank=True, null=True)
    lisatieto = models.CharField(max_length=255, blank=True, null=True)
    julktyyppiid = models.ForeignKey('Julktyyppi', models.DO_NOTHING, db_column='julktyyppiid')
    linkki = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'julkaisu'


class Julktyyppi(models.Model):
    id = models.IntegerField(primary_key=True)
    nimi = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'julktyyppi'


class Kohde(models.Model):
    id = models.IntegerField(primary_key=True)
    tunnus = models.CharField(max_length=10, blank=True, null=True)
    luokkatunnus = models.ForeignKey('Luokka', models.DO_NOTHING, db_column='luokkatunnus')
    geometry1 = models.GeometryField()
    nimi = models.CharField(max_length=80, blank=True, null=True)
    kuvaus = models.CharField(max_length=255, blank=True, null=True)
    huom = models.CharField(max_length=255, blank=True, null=True)
    voimassa = models.BooleanField()
    digipvm = models.DateField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    digitoija = models.CharField(max_length=50, blank=True, null=True)
    suojaustasoid = models.ForeignKey('Suojaustaso', models.DO_NOTHING, db_column='suojaustasoid')
    pvm_editoitu = models.DateTimeField(blank=True, null=True)
    muokkaaja = models.CharField(max_length=10, blank=True, null=True)
    pinta_ala = models.FloatField(blank=True, null=True)
    teksti = models.CharField(max_length=4000, blank=True, null=True)
    teksti_www = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kohde'


class KohdeHistoria(models.Model):
    id = models.IntegerField(primary_key=True)
    tunnus = models.CharField(max_length=10, blank=True, null=True)
    luokkatunnus = models.CharField(max_length=10)
    geometry1 = models.GeometryField()
    nimi = models.CharField(max_length=80, blank=True, null=True)
    kuvaus = models.CharField(max_length=255, blank=True, null=True)
    huom = models.CharField(max_length=255, blank=True, null=True)
    voimassa = models.BooleanField()
    digipvm = models.DateField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    digitoija = models.CharField(max_length=50, blank=True, null=True)
    suojaustasoid = models.ForeignKey('Suojaustaso', models.DO_NOTHING, db_column='suojaustasoid')
    pvm_editoitu = models.DateTimeField(blank=True, null=True)
    muokkaaja = models.CharField(max_length=10, blank=True, null=True)
    pinta_ala = models.FloatField(blank=True, null=True)
    teksti = models.CharField(max_length=4000, blank=True, null=True)
    teksti_www = models.CharField(max_length=4000, blank=True, null=True)
    historia_pvm = models.DateTimeField()
    kohde_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kohde_historia'


class KohdeJulk(models.Model):
    kohdeid = models.ForeignKey(Kohde, models.DO_NOTHING, db_column='kohdeid')
    julkid = models.ForeignKey(Julkaisu, models.DO_NOTHING, db_column='julkid')

    class Meta:
        managed = False
        db_table = 'kohde_julk'
        unique_together = (('kohdeid', 'julkid'),)


class Kohdelinkki(models.Model):
    id = models.IntegerField(primary_key=True)
    tekstiid = models.ForeignKey(Kohde, models.DO_NOTHING, db_column='tekstiid')
    linkki = models.CharField(max_length=4000, blank=True, null=True)
    linkkiteksti = models.CharField(max_length=4000, blank=True, null=True)
    tyyppiid = models.ForeignKey('Linkkityyppi', models.DO_NOTHING, db_column='tyyppiid')
    jarjestys = models.IntegerField(blank=True, null=True)
    linkin_teksti = models.CharField(max_length=1000, blank=True, null=True)
    suojaustasoid = models.ForeignKey('Suojaustaso', models.DO_NOTHING, db_column='suojaustasoid')

    class Meta:
        managed = False
        db_table = 'kohdelinkki'


class LajSaa(models.Model):
    lajid = models.ForeignKey('Lajirekisteri', models.DO_NOTHING, db_column='lajid')
    saaid = models.ForeignKey('Saados', models.DO_NOTHING, db_column='saaid')

    class Meta:
        managed = False
        db_table = 'laj_saa'
        unique_together = (('lajid', 'saaid'),)


class Lajihavainto(models.Model):
    id = models.IntegerField(primary_key=True)
    kohdeid = models.ForeignKey(Kohde, models.DO_NOTHING, db_column='kohdeid')
    lajid = models.ForeignKey('Lajirekisteri', models.DO_NOTHING, db_column='lajid')
    hsaid = models.ForeignKey(Havaintosarja, models.DO_NOTHING, db_column='hsaid', blank=True, null=True)
    runsausid = models.ForeignKey('Runsaus', models.DO_NOTHING, db_column='runsausid', blank=True, null=True)
    yleisyysid = models.ForeignKey('Yleisyys', models.DO_NOTHING, db_column='yleisyysid', blank=True, null=True)
    hloid = models.ForeignKey(Henkilo, models.DO_NOTHING, db_column='hloid', blank=True, null=True)
    lkm = models.CharField(max_length=30, blank=True, null=True)
    liikkumislkid = models.ForeignKey('Liikkumislk', models.DO_NOTHING, db_column='liikkumislkid', blank=True, null=True)
    alkuperaid = models.ForeignKey(Alkupera, models.DO_NOTHING, db_column='alkuperaid', blank=True, null=True)
    pesimisvarmuusid = models.ForeignKey('Pesimisvarmuus', models.DO_NOTHING, db_column='pesimisvarmuusid', blank=True, null=True)
    kuvaus = models.CharField(max_length=255, blank=True, null=True)
    huom = models.CharField(max_length=100, blank=True, null=True)
    pvm = models.DateField(blank=True, null=True)
    esiintymaid = models.ForeignKey(Esiintyma, models.DO_NOTHING, db_column='esiintymaid', blank=True, null=True)
    suojaustasoid = models.ForeignKey('Suojaustaso', models.DO_NOTHING, db_column='suojaustasoid')
    pvm_luotu = models.DateTimeField()
    pvm_editoitu = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lajihavainto'


class Lajirekisteri(models.Model):
    id = models.IntegerField(primary_key=True)
    ryhma = models.CharField(max_length=5, blank=True, null=True)
    elioryhma1 = models.CharField(max_length=50, blank=True, null=True)
    elioryhma2 = models.CharField(max_length=50, blank=True, null=True)
    lahko_suomi = models.CharField(max_length=150, blank=True, null=True)
    lahko_tiet = models.CharField(max_length=150, blank=True, null=True)
    heimo_suomi = models.CharField(max_length=150, blank=True, null=True)
    heimo_tiet = models.CharField(max_length=150, blank=True, null=True)
    nimi_suomi1 = models.CharField(max_length=150, blank=True, null=True)
    nimi_suomi2 = models.CharField(max_length=150, blank=True, null=True)
    nimi_tiet1 = models.CharField(max_length=150, blank=True, null=True)
    nimi_tiet2 = models.CharField(max_length=150, blank=True, null=True)
    alalaji1 = models.CharField(max_length=150, blank=True, null=True)
    alalaji2 = models.CharField(max_length=150, blank=True, null=True)
    auktori1 = models.CharField(max_length=150, blank=True, null=True)
    auktori2 = models.CharField(max_length=150, blank=True, null=True)
    nimilyhenne1 = models.CharField(max_length=10, blank=True, null=True)
    nimilyhenne2 = models.CharField(max_length=10, blank=True, null=True)
    nimi_ruotsi = models.CharField(max_length=150, blank=True, null=True)
    nimi_englanti = models.CharField(max_length=150, blank=True, null=True)
    rekisteripvm = models.DateTimeField(blank=True, null=True)
    suojaustasoid = models.ForeignKey('Suojaustaso', models.DO_NOTHING, db_column='suojaustasoid')
    lisatieto = models.CharField(max_length=255, blank=True, null=True)
    koodi = models.CharField(max_length=20, blank=True, null=True)
    linkki = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lajirekisteri'


class Liikkumislk(models.Model):
    id = models.IntegerField(primary_key=True)
    arvo = models.IntegerField(blank=True, null=True)
    selitys = models.CharField(max_length=50, blank=True, null=True)
    lahde = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'liikkumislk'


class Linkkityyppi(models.Model):
    id = models.IntegerField(primary_key=True)
    nimi = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linkkityyppi'


class LtyyppiSaados(models.Model):
    ltyyppiid = models.ForeignKey('Ltyyppirekisteri', models.DO_NOTHING, db_column='ltyyppiid')
    saadosid = models.ForeignKey('Saados', models.DO_NOTHING, db_column='saadosid')

    class Meta:
        managed = False
        db_table = 'ltyyppi_saados'
        unique_together = (('ltyyppiid', 'saadosid'),)


class Ltyyppihavainto(models.Model):
    id = models.IntegerField(primary_key=True)
    kohdeid = models.ForeignKey(Kohde, models.DO_NOTHING, db_column='kohdeid')
    ltyypid = models.ForeignKey('Ltyyppirekisteri', models.DO_NOTHING, db_column='ltyypid')
    osuus_kuviosta = models.IntegerField(blank=True, null=True)
    lisatieto = models.CharField(max_length=255, blank=True, null=True)
    hsaid = models.ForeignKey(Havaintosarja, models.DO_NOTHING, db_column='hsaid')
    pvm_luotu = models.DateTimeField()
    pvm_editoitu = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltyyppihavainto'


class Ltyyppirekisteri(models.Model):
    id = models.IntegerField(primary_key=True)
    nimi = models.CharField(max_length=50, blank=True, null=True)
    koodi = models.CharField(max_length=10, blank=True, null=True)
    kuvaus = models.CharField(max_length=255, blank=True, null=True)
    lisatieto = models.CharField(max_length=255, blank=True, null=True)
    ltyyppiryhma = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ltyyppirekisteri'


class Luokka(models.Model):
    tunnus = models.CharField(primary_key=True, max_length=10)
    nimi = models.CharField(max_length=50, blank=True, null=True)
    lisatieto = models.CharField(max_length=255, blank=True, null=True)
    paatunnus = models.CharField(max_length=40, blank=True, null=True)
    raportointi = models.BooleanField()
    www = models.BooleanField()
    metadata = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'luokka'


class Pesimisvarmuus(models.Model):
    id = models.IntegerField(primary_key=True)
    arvo = models.CharField(max_length=50, blank=True, null=True)
    selitys = models.CharField(max_length=50, blank=True, null=True)
    lahde = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pesimisvarmuus'


class Runsaus(models.Model):
    id = models.IntegerField(primary_key=True)
    arvo = models.CharField(max_length=5, blank=True, null=True)
    selitys = models.CharField(max_length=30, blank=True, null=True)
    lahde = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'runsaus'


class Ruutu(models.Model):
    id = models.ForeignKey(Kohde, models.DO_NOTHING, db_column='id', primary_key=True)
    nro = models.CharField(max_length=10, blank=True, null=True)
    selvitysaste = models.IntegerField(blank=True, null=True)
    lisatieto = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ruutu'


class Saados(models.Model):
    id = models.IntegerField(primary_key=True)
    nimi = models.CharField(max_length=255, blank=True, null=True)
    pykala = models.CharField(max_length=100, blank=True, null=True)
    lisatieto = models.CharField(max_length=255, blank=True, null=True)
    arvo = models.CharField(max_length=10, blank=True, null=True)
    arvon_selitys = models.CharField(max_length=255, blank=True, null=True)
    voimassa = models.BooleanField()
    voimaantulo = models.DateTimeField(blank=True, null=True)
    linkki = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saados'


class Sohjelma(models.Model):
    id = models.IntegerField(primary_key=True)
    nimi = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sohjelma'


class SuoPeruste(models.Model):
    perusteid = models.ForeignKey('Suoperuste', models.DO_NOTHING, db_column='perusteid')
    suoid = models.ForeignKey('Suojelu', models.DO_NOTHING, db_column='suoid')

    class Meta:
        managed = False
        db_table = 'suo_peruste'
        unique_together = (('perusteid', 'suoid'),)


class Suojaustaso(models.Model):
    id = models.IntegerField(primary_key=True)
    selitys = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suojaustaso'


class Suojelu(models.Model):
    id = models.ForeignKey(Kohde, models.DO_NOTHING, db_column='id', primary_key=True)
    ilmoitettu_pinta_ala = models.CharField(max_length=50, blank=True, null=True)
    maapinta_ala = models.CharField(max_length=50, blank=True, null=True)
    vesipinta_ala = models.CharField(max_length=50, blank=True, null=True)
    liikkuminen = models.CharField(max_length=255, blank=True, null=True)
    maaraykset = models.CharField(max_length=255, blank=True, null=True)
    lisatieto = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suojelu'


class SuojeluSohjelma(models.Model):
    suojeluid = models.ForeignKey(Suojelu, models.DO_NOTHING, db_column='suojeluid')
    sohjelmaid = models.ForeignKey(Sohjelma, models.DO_NOTHING, db_column='sohjelmaid')

    class Meta:
        managed = False
        db_table = 'suojelu_sohjelma'
        unique_together = (('suojeluid', 'sohjelmaid'),)


class Suoperuste(models.Model):
    id = models.IntegerField(primary_key=True)
    peruste = models.CharField(max_length=50, blank=True, null=True)
    tarkperuste = models.CharField(max_length=50, blank=True, null=True)
    alaperuste = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suoperuste'


class TapSaados(models.Model):
    tapid = models.ForeignKey('Tapahtuma', models.DO_NOTHING, db_column='tapid')
    saaid = models.ForeignKey(Saados, models.DO_NOTHING, db_column='saaid')

    class Meta:
        managed = False
        db_table = 'tap_saados'
        unique_together = (('tapid', 'saaid'),)


class Tapahtuma(models.Model):
    id = models.IntegerField(primary_key=True)
    diaarinro = models.CharField(max_length=20, blank=True, null=True)
    kuvaus = models.CharField(max_length=255, blank=True, null=True)
    tapahtumatyyppiid = models.ForeignKey('Tapahtumatyyppi', models.DO_NOTHING, db_column='tapahtumatyyppiid')
    paivittaja = models.CharField(max_length=20, blank=True, null=True)
    pvm = models.DateField(blank=True, null=True)
    hloid = models.ForeignKey(Henkilo, models.DO_NOTHING, db_column='hloid', blank=True, null=True)
    linkki = models.CharField(max_length=4000, blank=True, null=True)
    suojaustasoid = models.ForeignKey(Suojaustaso, models.DO_NOTHING, db_column='suojaustasoid')

    class Meta:
        managed = False
        db_table = 'tapahtuma'


class TapahtumaKohde(models.Model):
    kohdeid = models.ForeignKey(Kohde, models.DO_NOTHING, db_column='kohdeid')
    tapid = models.ForeignKey(Tapahtuma, models.DO_NOTHING, db_column='tapid')

    class Meta:
        managed = False
        db_table = 'tapahtuma_kohde'
        unique_together = (('kohdeid', 'tapid'),)


class Tapahtumatyyppi(models.Model):
    id = models.IntegerField(primary_key=True)
    nimi = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tapahtumatyyppi'


class Yleisyys(models.Model):
    id = models.IntegerField(primary_key=True)
    arvo = models.CharField(max_length=5, blank=True, null=True)
    selitys = models.CharField(max_length=30, blank=True, null=True)
    lahde = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'yleisyys'
