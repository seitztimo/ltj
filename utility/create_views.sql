-- Sisäiset kääpäkohteet

CREATE OR REPLACE VIEW ltj.arvo_kaapakohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=163&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'KAAP'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));
                                                                                      
-- Sisäiset arvoliito-oravat:

CREATE OR REPLACE VIEW ltj.arvo_liito_orava AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=296&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LIIT'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset arvo-metsäkohteet:

CREATE OR REPLACE VIEW ltj.arvo_metsakohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=164&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'METS'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset tärkeät lepakkoalueet:

CREATE OR REPLACE VIEW ltj.arvo_tarkeat_lepakkoalueet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=160&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'LEPA'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset matelija ja sammakkoeläinkohteet:

CREATE OR REPLACE VIEW ltj.arvo_tarkeat_matelija_ja_sammakkoelainkohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=161&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'MASA'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset arvokkaat geologiset:

CREATE OR REPLACE VIEW ltj.arvokkaat_geologiset AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=162&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'GK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset arvokkaat kasvit:

CREATE OR REPLACE VIEW ltj.arvokkaat_kasvikohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=153&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'KK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset arvokkaat linnut:

CREATE OR REPLACE VIEW ltj.arvokkaat_lintukohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=159&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'LK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset muut eläinhavainnot:

CREATE OR REPLACE VIEW ltj.muu_elainhavaintoja AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    lajirekisteri.nimi_suomi1 AS lajinimi,
    lajihavainto.pvm AS havainnon_paivamaara,
    havaintosarja.nimi AS havaintosarjan_nimi,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=168&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM ((((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     JOIN public.lajihavainto ON ((kohde.id = lajihavainto.kohdeid)))
     JOIN public.lajirekisteri ON ((lajirekisteri.id = lajihavainto.lajid)))
     JOIN public.havaintosarja ON ((lajihavainto.hsaid = havaintosarja.id)))
  WHERE (((kohde.luokkatunnus)::text = 'EK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset muut perinnemaisemat:

CREATE OR REPLACE VIEW ltj.muu_perinnemaisemia AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=169&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'PM'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset muut luontokohteet:

CREATE OR REPLACE VIEW ltj.muut_luontokohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=170&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'MUU'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset rauhoitetut luonnonmuistomerkit:

CREATE OR REPLACE VIEW ltj.rauh_luonnonmuistomerkit AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=157&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Lmm'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset rauhoitetut luonnonsuojelualueet:

CREATE OR REPLACE VIEW ltj.rauh_luonnonsuojelualueet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=154&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Lsa'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset rauhoitetut luonnonsuojeluohjelmat:

CREATE OR REPLACE VIEW ltj.rauh_luonnonsuojeluohjelma AS
 SELECT kohde.id,
    kohde.tunnus,
    'LSO'::character varying(10) AS luokkatunnus,
    'Luonnonsuojeluohjelman kohde'::character varying(50) AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=158&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Kaava'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset rauhoitetut naturat:

CREATE OR REPLACE VIEW ltj.rauh_natura AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=155&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Natur'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset suojellut luontotyypit:

CREATE OR REPLACE VIEW ltj.rauh_suojellut_luontotyypit AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    suoperuste.peruste,
    suoperuste.tarkperuste,
    suoperuste.alaperuste,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=156&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM ((((public.kohde
     JOIN public.suojelu ON ((kohde.id = suojelu.id)))
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.suo_peruste ON ((suojelu.id = suo_peruste.suoid)))
     LEFT JOIN public.suoperuste ON ((suo_peruste.perusteid = suoperuste.id)))
  WHERE (((kohde.luokkatunnus)::text = 'LslLt'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

  -- Sisäiset suojellut lajikohteet:

  CREATE OR REPLACE VIEW ltj.suojellut_lajikohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=174&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM ((public.kohde
     JOIN public.suojelu ON ((kohde.id = suojelu.id)))
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Slaji'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset vesi-lähteet:

CREATE OR REPLACE VIEW ltj.vesi_lahteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=167&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LAH'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

  -- Sisäiset purojen ja lampien valuma-alueet:

  CREATE OR REPLACE VIEW ltj.vesi_purojen_ja_lampien_valuma_alueet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=166&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'PPV'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset vesi-purojen putkitetut osuudet:

CREATE OR REPLACE VIEW ltj.vesi_purojen_putkitetut_osuudet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=269&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'PPUT'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset vesi-purot ja vesi-lammet:

CREATE OR REPLACE VIEW ltj.vesi_purot_ja_lammet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=165&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'PPO'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäinen vedenlainen roskaantuminen:

CREATE OR REPLACE VIEW ltj.vesi_vedenalainen_roskaantuminen AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=291&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'ROSK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));

-- Sisäiset vesikasvilinjat:

CREATE OR REPLACE VIEW ltj.vesi_vesikasvilinjat AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=289&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LITO'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));
                                                                                      
-- Sisäiset uhanalaiset luontotyypit:

CREATE OR REPLACE VIEW ltj.uhanal_luontotyypit AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=345&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'UHLT'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));
                                                                                      
 -- Sisäiset lahokaviosammalen elinympäristöt
                                                                                      
 CREATE OR REPLACE VIEW ltj.lahokaviosammal_elinymparistot AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=327&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LKSE'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));
                                                                                      
  -- Sisäiset tärkeät lintualueet 2017:

CREATE OR REPLACE VIEW ltj.tarkeat_lintualueet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=340&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LK2'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));     
                                                                                     
-- Sisäiset biotooppikohteet

CREATE OR REPLACE VIEW ltj.biotoopit AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=180&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'BK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));
                                                                                    
-- Sisäiset kunnostetut purokohdat

CREATE OR REPLACE VIEW ltj.kunnostetut_purokohdat AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=308&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'KUNN'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));
                                                                                      
-- Sisäiset ekologisten yhteyksien verkosto

CREATE OR REPLACE VIEW ltj.ekologiset_yhteydet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'VYHT'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));
                                                                                      
 -- Sisäiset metsäverkosto

CREATE OR REPLACE VIEW ltj.metsaverkosto AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'MVER'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid <> 1));
                                                                                      
-- Julkiset arvokääpäkohteet:

CREATE OR REPLACE VIEW ltj_avoin.arvo_kaapakohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=163&l=fi'::text AS metadata
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'KAAP'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset arvoliito-oravat:

CREATE OR REPLACE VIEW ltj_avoin.arvo_liito_orava AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=296&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LIIT'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset arvo-metsäkohteet:

CREATE OR REPLACE VIEW ltj_avoin.arvo_metsakohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=164&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'METS'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset tärkeät lepakkoalueet:

CREATE OR REPLACE VIEW ltj_avoin.arvo_tarkeat_lepakkoalueet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=160&l=fi'::text AS metadata
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'LEPA'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset tärkeät matelija ja sammakkoeläinkohteet:

CREATE OR REPLACE VIEW ltj_avoin.arvo_tarkeat_matelija_ja_sammakkoelainkohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=161&l=fi'::text AS metadata
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'MASA'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset arvokkaat geologiset kohteet:

CREATE OR REPLACE VIEW ltj_avoin.arvokkaat_geologiset AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=162&l=fi'::text AS metadata
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'GK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset arvokkaat kasvikohteet:

CREATE OR REPLACE VIEW ltj_avoin.arvokkaat_kasvikohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=153&l=fi'::text AS metadata
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'KK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset arvokkaat lintukohteet:

CREATE OR REPLACE VIEW ltj_avoin.arvokkaat_lintukohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=159&l=fi'::text AS metadata
   FROM (((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.arvo_kohde ON ((kohde.id = arvo_kohde.kohdeid)))
     LEFT JOIN public.arvo ON ((arvo_kohde.arvoid = arvo.id)))
  WHERE (((kohde.luokkatunnus)::text = 'LK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset muut eläinhavainnot:

CREATE OR REPLACE VIEW ltj_avoin.muu_elainhavaintoja AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    lajirekisteri.nimi_suomi1 AS lajinimi,
    lajihavainto.pvm AS havainnon_paivamaara,
    havaintosarja.nimi AS havaintosarjan_nimi,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=168&l=fi'::text AS metadata
   FROM ((((public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     JOIN public.lajihavainto ON ((kohde.id = lajihavainto.kohdeid)))
     JOIN public.lajirekisteri ON ((lajirekisteri.id = lajihavainto.lajid)))
     JOIN public.havaintosarja ON ((lajihavainto.hsaid = havaintosarja.id)))
  WHERE (((kohde.luokkatunnus)::text = 'EK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset muut luontokohteet:

CREATE OR REPLACE VIEW ltj_avoin.muut_luontokohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=170&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'MUU'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset rauhoitetut luonnonmuistomerkit:

CREATE OR REPLACE VIEW ltj_avoin.rauh_luonnonmuistomerkit AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=157&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Lmm'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset luonnonsuojelualueet:

CREATE OR REPLACE VIEW ltj_avoin.rauh_luonnonsuojelualueet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=154&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Lsa'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset rauhoitetut luonnonsuojeluohjelmat:

CREATE OR REPLACE VIEW ltj_avoin.rauh_luonnonsuojeluohjelma AS
 SELECT kohde.id,
    kohde.tunnus,
    'LSO'::character varying(10) AS luokkatunnus,
    'Luonnonsuojeluohjelman kohde'::character varying(50) AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=158&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Kaava'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset rauhoitetut naturat:

CREATE OR REPLACE VIEW ltj_avoin.rauh_natura AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=155&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Natur'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset suojellut luontotyypit:

CREATE OR REPLACE VIEW ltj_avoin.rauh_suojellut_luontotyypit AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    suoperuste.peruste,
    suoperuste.tarkperuste,
    suoperuste.alaperuste,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=156&l=fi'::text AS metadata
   FROM ((((public.kohde
     JOIN public.suojelu ON ((kohde.id = suojelu.id)))
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
     LEFT JOIN public.suo_peruste ON ((suojelu.id = suo_peruste.suoid)))
     LEFT JOIN public.suoperuste ON ((suo_peruste.perusteid = suoperuste.id)))
  WHERE (((kohde.luokkatunnus)::text = 'LslLt'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset suojellut lajikohteet:

CREATE OR REPLACE VIEW ltj_avoin.suojellut_lajikohteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=174&l=fi'::text AS metadata
   FROM ((public.kohde
     JOIN public.suojelu ON ((kohde.id = suojelu.id)))
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'Slaji'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset vesi-lähteet:

CREATE OR REPLACE VIEW ltj_avoin.vesi_lahteet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=167&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LAH'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset vesi-purojen ja vesi-lampien valuma-alueet:

CREATE OR REPLACE VIEW ltj_avoin.vesi_purojen_ja_lampien_valuma_alueet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=166&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'PPV'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset vesi-purojen putkitetut osuudet:

CREATE OR REPLACE VIEW ltj_avoin.vesi_purojen_putkitetut_osuudet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=269&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'PPUT'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset vesi-purot ja vesi-lammet:

CREATE OR REPLACE VIEW ltj_avoin.vesi_purot_ja_lammet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=165&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'PPO'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkinen vedenalainen roskaantuminen:

CREATE OR REPLACE VIEW ltj_avoin.vesi_vedenalainen_roskaantuminen AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=291&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'ROSK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));

-- Julkiset vesikasvilinjat:

CREATE OR REPLACE VIEW ltj_avoin.vesi_vesikasvilinjat AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=289&l=fi'::text AS metadata
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LITO'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));
                                                                                      
-- Julkiset uhanalaiset luontotyypit:

CREATE OR REPLACE VIEW ltj_avoin.uhanal_luontotyypit AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
        CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=345&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'UHLT'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));   
                                                                                      
 -- Julkiset lahokaviosammalen elinympäristöt
                                                                                      
 CREATE OR REPLACE VIEW ltj_avoin.lahokaviosammal_elinymparistot AS
  SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
     CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=327&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LKSE'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));
                                                                                      
   -- Julkiset tärkeät lintualueet 2017:

CREATE OR REPLACE VIEW ltj_avoin.tarkeat_lintualueet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
      CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=340&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'LK2'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));  
                                                                                     
  
 -- Julkiset biotooppikohteet

CREATE OR REPLACE VIEW ltj_avoin.biotoopit AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
      CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=180&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'BK'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));
                                                                                    
-- Julkiset ekologisten yhteyksien verkosto

CREATE OR REPLACE VIEW ltj_avoin.ekologiset_yhteydet AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
       CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'VYHT'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));
                                                                                      
-- Julkiset metsäverkosto

CREATE OR REPLACE VIEW ltj_avoin.metsaverkosto AS
 SELECT kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.digipvm,
    kohde.pvm_editoitu,
    kohde.digitoija,
    kohde.muokkaaja,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
       CASE
            WHEN (NOT ((kohde.teksti_www)::text = ''::text)) THEN kohde.teksti_www
            ELSE kohde.teksti
        END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id) AS kohderaportti
   FROM (public.kohde
     JOIN public.luokka ON (((luokka.tunnus)::text = (kohde.luokkatunnus)::text)))
  WHERE (((kohde.luokkatunnus)::text = 'MVER'::text) AND (kohde.voimassa = true) AND (kohde.suojaustasoid = 3));
