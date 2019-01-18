from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from nature.models import FeatureClass, Criterion, ConservationProgramme, Protection, ProtectionCriterion, \
    ProtectionConservationProgramme, Square


class FeatureForm(forms.ModelForm):
    feature_class = forms.ModelChoiceField(
        queryset=FeatureClass.objects.order_by('name'),
        label=FeatureClass._meta.verbose_name.capitalize(),
    )

    class Meta:
        widgets = {
            'text': CKEditorWidget,
            'text_www': CKEditorWidget,
            'description': forms.Textarea,
            'notes': forms.Textarea,
            'name': forms.TextInput(attrs={'size': '80'})
        }
        help_texts = {
            'geometry': (
                'Uuden kohteen digitoiminen: valitse geometriatyyppi kartan yläkulmasta ja digitoi kohde. <br />'
                'Kohdetta voi muokata tarttumalla hiirellä kohteen reunasta. <br />'
                'Voit vaihtaa karttapohjan geometriatyökalujen alta löytyvällä painikkeella. <br />'
                'Valitsemalla "Poista kaikki geometriat" voit korvata vanhan geometrian uudella.'
            ),
            'feature_class': 'Mihin kohdeluokkaan kohde kuuluu',
            'fid': 'Kohdetunnus, voi sisältää numeroita, kirjaimia ja merkkejä',
            'name': 'Kohteen nimi, esim. Harakan etelakarki tai Maununneva. Nimi mieluiten sijaintia kuvaava',
            'description': 'Kohteen lyhyt kuvaus tai pidempi kuvaileva nimi',
            'notes': 'Kohteen tietoihin tai geometriaan liittyvää huomionarvoista tietoa',
            'active': 'Kohde voimassa / ei. Oletuksena ”kyllä”',
            'number': 'Apukentta mm. uusien aineistojen tuontia ja kohteiden erilaisia luokitteluja varten',
            'text': 'Kohteen kuvausteksti',
            'text_www': (
                'Kohteen kuvausteksti, julkinen. Jos kenttä ”teksti_www” on tyhjä, '
                'kentän ”teksti” sisältö on julkinen.'
            ),

        }


class HabitatTypeObservationInlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': '5'}),
        }
        help_texts = {
            'group_fraction': 'Luontotyypin osuus kuviosta prosentteina',
            'additional_info': 'Muuta tietoa luontotyyppihavainnosta',
            'observation_series': 'Havaintosarja, johon havainto kuuluu',
            'created_time': 'Havaintorivin luontihetki, automaattinen',
            'last_modified_time': 'Havaintorivin editointihetki, automaattinen',
        }


class ProtectionInlineForm(forms.ModelForm):
    criteria = forms.ModelMultipleChoiceField(
        queryset=Criterion.objects.all(),
        widget=FilteredSelectMultiple(verbose_name=_('Criteria'), is_stacked=False),
        required=False,
    )
    conservation_programmes = forms.ModelMultipleChoiceField(
        queryset=ConservationProgramme.objects.all(),
        widget=FilteredSelectMultiple(verbose_name=_('Conservation programmes'), is_stacked=False),
        required=False,
    )

    class Meta:
        model = Protection
        fields = '__all__'

    def _save_m2m(self):
        # django does not allow saving m2m with manually specified m2m intermediate
        # tables, so use intermediate model manager instead.
        ProtectionCriterion.objects.filter(protection=self.instance).delete()
        protection_criteria = [
            ProtectionCriterion(
                protection=self.instance,
                criterion=criterion,
            ) for criterion in self.cleaned_data['criteria']
        ]
        ProtectionCriterion.objects.bulk_create(protection_criteria)

        ProtectionConservationProgramme.objects.filter(protection=self.instance).delete()
        protection_conservation_programmes = [
            ProtectionConservationProgramme(
                protection=self.instance,
                conservation_programme=conservation_programme,
            ) for conservation_programme in self.cleaned_data['conservation_programmes']
        ]
        ProtectionConservationProgramme.objects.bulk_create(protection_conservation_programmes)

    @transaction.atomic
    def save(self, commit=True):
        protection = super().save(commit=False)
        if commit:
            protection.save()
            self._save_m2m()

        return protection


class SquareInlineForm(forms.ModelForm):
    class Meta:
        model = Square
        fields = '__all__'
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': '5'}),
        }


class ValueForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'value': 'Arvoluokka, esim. 1, 2 ja 3 tai I, II ja III',
            'explanation': 'Kertoo, mitä luokitus tarkoittaa, esim. paikallisesti tai alueellisesti arvokas',
            'valuator': 'Arvotuksen tekijä',
            'date': 'Päivämäärä',
            'link': 'Linkki lisätietoihin',
        }


class ObservationSeriesForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'name': 'Havaintosarjan nimi. Kertoo, mihin tutkimukseen, ajanjaksoon tai ryhmään havainnot kuuluvat',
            'person': 'Havaintosarjan vastuuhenkilö, henkilo-taulun id',
            'description': 'Havaintosarjan kuvaus',
            'start_date': 'Havaintosarjan alkupäivämäärä',
            'end_date': 'Havaintosarjan loppupäivämääsä',
            'notes': 'Huomioitavaa, esim. mahdolliset tutkimuksen puuttelliset osat.',
            'additional_info': 'Lisätieto',
            'valid': 'Kertoo, onko havaintosarja voimassa vai ei. Oletusarvona ”Kyllä”',
        }


class PersonForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'expertise': 'Henkilön mahdollinen erityisasiantuntemus.',
            'notes': 'Mahdolliset lisätiedot',
            'company': 'Yrityksen nimi',
            'public_servant': 'Tieto onko henkilö viranomainen vai ei',
            'created_time': 'Ajankohta, jolloin henkillö lisätty rekisteriin. Automaattinen.',
        }


class PublicationForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'name': 'Julkaisun nimi',
            'author': 'Julkaisun tekijä / tekijät',
            'series': 'Sarja, jossa julkaistu',
            'place_of_printing': 'Painopaikka',
            'year': 'Julkaisuvuosi',
            'additional_info': 'Lisätietoa julkaisusta, esim. julkaistu myös ruotsiksi, isbn-numero',
            'link': 'Linkki julkaisuun tai siihen liittyvään dokumenttiin',
        }


class FeatureLinkForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'link': 'Linkki esim. kuvaan tai muuhun tiedostoon',
            'text': 'Linkkiin liittyvä teksti. Esim. kuvan kuvateksti',
            'link_text': 'Teksti, jona linkki näkyy raportissa esim. ”Kuva 1”',
            'link_type': 'Linkkityyppi-taulun id, kertoo onko kyseessä kuvalinkki, nettisivulinkki, '
                         'raporttilinkki jne.',
            'ordering': 'K.o. linkin sijainti raportoinnissa suhteessa muihin linkkeihin.',
            'protection_level': 'Suojaustaso 1,2,3',
        }


class ObservationForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'number': 'Havaittujen yksilöiden tai muiden yksiköiden lukumäärä.',
            'migration_class': 'Liikkumislk-taulun id. Kertoo liikkumisluokan. Arvot 1-3, käytetään vain linnuille '
                               '(tarvittaessa myös muille eläimille)',
            'breeding_degree': 'Pesimisvarmuus-taulun id. Kertoo liikkumisluokan. Arvot 1-9, käytetään vain linnuille '
                               '(tarvittaessa myös muille eläimille)',
            'description': 'Havaintoon liittyvää kuvailevaa tietoa, esim. havaitun yksilön sukupuoli, havainnon '
                           'kellonaika, tms.',
            'notes': 'Tiedot esim. havainnon varmuudesta tai muusta huomionarvoisesta tiedosta',
            'date': 'Havainnon päivämäärä (ja kellonaika) Tämä ei ole pakollinen kenttä, koska jos lajiin liittyy '
                    'havaintosarja, päivämäärä tulee havaintosarjasta.',
            'created_time': 'Havaintorivin luontihetki, automaattinen',
            'last_modified_time': 'Havainnon editointihetki, automaattinen',
            'code': 'Havainnon koodi, käytetään tiedonsiirrossa',
        }


class SpeciesForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'taxon': 'Lajin ylin luokittelu ltj:ssä: kasvi /sieni/ eläin',
            'taxon_1': 'Ryhmää tarkempi luokittelu: mm. levä, putkilokasvi, lintu, nisäkäs, sammakkoeläin, matelija ',
            'taxon_2': 'Eliöryhmä1:stä tarkempi luokittelu: sinilevä, viherlevä, lepakko, perhonen',
            'order_fi': 'Lahkon suomenkielinen nimi',
            'order_la': 'Lahkon tieteellinen nimi',
            'family_fi': 'Heimon suomenkielinen nimi',
            'family_la': 'Heimon tieteellinen nimi',
            'name_fi': 'Lajin / alalajin / muun taksonin suomenkielinen nimi',
            'name_fi_2': 'Rinnakkainen tai vanha suomenkielinen nimi',
            'name_sci_1': 'Lajin / alalajin / muun taksonin tieteellinen nimi',
            'name_sci_2': 'Rinnakkainen tai vanha tieteellinen nimi (tähän kirjataan ex-tieteellinen nimi alalajin '
                          'kanssa kokonaan, mikäli myös lajinimi vaihtunut)',
            'name_subspecies_1': 'Alalaji',
            'name_subspecies_2': 'Rinnakkainen tai vanha alalaji (käytetään kun vain alalajitieto muuttunut, muutoin '
                                 'kenttä nimi_tiet_2 epäselvyyksien välttämiseksi)',
            'author_1': 'Lajin / alalajin auktori, lahde ja vuosi. tai kirja, lista tms., jonka nimistöä käytetty '
                        '(retkeilykasvio,  luontodirektiivin lista tms.) Täytetään ainakin niille lajeille/ryhmille, '
                        'joiden nimistö on vastikään vaihtunut tai muutoksia on odotettavissa.',
            'author_2': 'Rinnakkainen tai vanha auktori, lahde ja vuosi. voi olla useita. voi olla viittaus vanhaa '
                        'nimistöä käyttävään kirjaan/listaan.',
            'name_abbreviated_1': (
                'Kasvit: biotooppikartoituksessa 2001 käytetty lyhenne, pääosin muotoa 4+4, myös 4+3, 3+4 ja 3+3. '
                'Linnut: tieteellisen nimen mukainen lyhenne.'
            ),
            'name_abbreviated_2': 'Kasvit: mm. HelFlorassa käytetty lyhenne. Pääosin muotoa 4+4, myös 4+3, 3+4 ja 3+3. '
                                  'Linnut: aikaisemman tiet nimen mukainen lyhenne 3+3',
            'name_sv': 'Ruotsinkielinen nimi',
            'name_en': 'Englanninkielinen nimi',
            'registry_date': 'Päivämäärä, jolloin laji lisätty rekisteriin',
            'protection_level': 'Suojaustaso 3: saa näyttää netissä, 2: vain ylläpitäjät ja virkakäyttäjät, 1: vain '
                                'ylläpitäjät. Oletusarvo 3.',
            'additional_info': 'Kertoo esimerkiksi aikaisemmista nimistötiedoista',
            'code': '2016: lajitietokeskuksen mx-koodi. 0=tarkemmin määrittämättömät',
            'link': 'Lajiin liittyvän sivun/kuvan tms. linkki',
        }


class LinkTypeForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'name': 'Kuvalinkki, pdf-tiedosto jne.',
        }


class HabitatTypeForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'name': 'Luontotyypin nimi. Luontotyypeillä voi olla sama nimi, jos luontotyyppiryhmä on eri.',
            'code': 'Luontotyypin koodi. Luontotyypeillä voi olla sama koodi, jos  luontotyyppiryhmä on eri.',
            'description': 'Luontotyypin kuvaus',
            'additional_info': 'Tähän kirjataan lisätieto, esim. jos kyseessä on EU:n ensisijainen luontotyyppi.',
            'group': 'Kertoo mihin ryhmään luontotyyppi kuuluu, esim. luontodirektiivin luontotyypit',
        }


class FeatureClassForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'name': 'Luokan nimi',
            'additional_info': 'Luokan lisätieto',
            'super_class': 'Pääluokkia ovat suojelukohde ja ruutukohde.K.o. pääkohteeseen kuuluvilla luokilla on '
                           'lisätietoja, jota muilla luokilla ei ole.',
            'reporting': 'Kyllä/Ei-merkintä, jonka mukaisesti luokan kohteet ovat mukana esim. kohderaportoinnissa '
                         'ja hakutoiminnoissa. Oletusarvona ”Kyllä”',
            'www': 'Kyllä/Ei-merkintä, jonka mukaisesti luokka näytetään yleisöversiossa tai ei näytetä.',
            'open_data': 'Kyllä/Ei-merkintä, jonka mukaisesti luokka (luokan kohteet havaintoineen) näytetään '
                         'rajapinnassa avoimena datana tai ei näytetä.',
            'metadata': 'Linkki aineistokuvaukseen',
        }


class RegulationForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'name': 'Asetuksen tms. nimi',
            'paragraph': 'Pykälä tai liite',
            'additional_info': 'Vapaamuotoinen tekstikenttä',
            'value': 'Esim. IUCN-luokka (NT, RT jne.)',
            'value_explanation': 'Arvo-kentässä olevan lyhenteen selite',
            'valid': 'Voimassaolo. Oletuksena ”kyllä”',
            'date_of_entry': 'Säädöksen tms. virallinen voimaantulopvm.',
            'link': 'Linkki säädökseen tai säädöskokoelmaan',
        }


class ProtectionForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'reported_area': 'Suojelupäätöksessä oleva kokonaispinta-ala',
            'land_area': 'Maapinta-ala',
            'water_area': 'Vesipinta-ala',
            'hiking': 'Liikkumisrajoitukset',
            'regulations': 'Muut määräykset',
            'additional_info': 'Lisätieto'
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'register_id': 'Asiakirjojen diaarinro',
            'description': 'Tapahtuman kuvaus',
            'transaction_type': 'tapahtumatyyppi-taulun id, vierasavain. Kertoo onko tapahtuma esim. päätös tai '
                                'tutkimus',
            'last_modified_by': 'Tapahtumaan liittyvien tietojen päivittäjä',
            'date': 'Tapahtuman päivämäärä',
            'person': 'Henkilo-taulun id, vierasavain. Tapahtuman tekija, jos henkilö',
            'link': 'Linkki tapahtumaa koskevaan dokumenttiin',
            'protection_level': 'Suojaustaso 3: saa näyttää netissä, 2: vain ylläpitäjät ja virkakäyttäjät, 1: vain '
                                'ylläpitäjät. Oletusarvo 3.',
        }
