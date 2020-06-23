-- New table for service metadata
CREATE TABLE IF NOT EXISTS ltj.jakelumetadata (
    id integer NOT NULL PRIMARY KEY,
    datanomistaja character varying(25),
    paivitetty_tietopalveluun date
);

ALTER TABLE ltj.jakelumetadata OWNER TO ltj;

GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE ltj.jakelumetadata TO ltj_yllapito;

GRANT SELECT ON TABLE ltj.jakelumetadata TO ltj_katselu;

GRANT ALL ON TABLE ltj.jakelumetadata TO ltj;

COMMENT ON COLUMN ltj.jakelumetadata.id
    IS 'Erillinen aineiston jakelun ylläpitämä metatietotaulu, jossa on yksi rivi id-arvolla 1.
        Taulu on liitetty aineistojakeluprosessin käyttämiin näkymiin';

INSERT INTO ltj.jakelumetadata
    VALUES (1, 'Helsinki/LTJ', now());

CREATE SCHEMA IF NOT EXISTS ltj_wfs_virka;

CREATE SCHEMA IF NOT EXISTS ltj_wfs_avoin;

-- Virkaversio kääpäkohteet:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvo_kaapakohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=163&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'KAAP'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.arvo_kaapakohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_kaapakohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_kaapakohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvo_kaapakohteet TO ltj;

-- Virkaversio liito-oravien elinalueet:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvo_liito_orava_elinalueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=296&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LIEL'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.arvo_liito_orava_elinalueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_liito_orava_elinalueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_liito_orava_elinalueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvo_liito_orava_elinalueet TO ltj;

-- Virkaversio liito-oravien ydinalueet:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvo_liito_orava_ydinalueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=296&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LIIT'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.arvo_liito_orava_ydinalueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_liito_orava_ydinalueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_liito_orava_ydinalueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvo_liito_orava_ydinalueet TO ltj;

-- Virkaversio metsäkohteet:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvo_metsakohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=164&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'METS'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.arvo_metsakohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_metsakohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_metsakohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvo_metsakohteet TO ltj;

-- Virkaversio tärkeät lepakkoalueet:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvo_tarkeat_lepakkoalueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=160&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LEPA'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.arvo_tarkeat_lepakkoalueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_tarkeat_lepakkoalueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_tarkeat_lepakkoalueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvo_tarkeat_lepakkoalueet TO ltj;

-- Virkaversio tärkeät matelija- ja sammakkoeläinkohteet:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvo_tarkeat_matelija_ja_sammakkoelainkohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=161&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'MASA'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.arvo_tarkeat_matelija_ja_sammakkoelainkohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_tarkeat_matelija_ja_sammakkoelainkohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvo_tarkeat_matelija_ja_sammakkoelainkohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvo_tarkeat_matelija_ja_sammakkoelainkohteet TO ltj;

-- Virkaversio arvokkaat geologiset kohteet aluemaiset:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvokkaat_geologiset_aluemaiset AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    array_to_string(array_agg(arvo.luokka), ', '::text) AS arvoluokka,
    array_to_string(array_agg(arvo.selite), ', '::text) AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=162&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'GK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1
    AND geometrytype (kohde.geometry1) ~~ '%POLYGON'::text
GROUP BY
    kohde.id,
    luokka.nimi,
    jakelumetadata.id;

ALTER TABLE ltj_wfs_virka.arvokkaat_geologiset_aluemaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvokkaat_geologiset_aluemaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvokkaat_geologiset_aluemaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvokkaat_geologiset_aluemaiset TO ltj;

-- Virkaversio arvokkaat geologiset kohteet viivamaiset:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvokkaat_geologiset_viivamaiset AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    array_to_string(array_agg(arvo.luokka), ', '::text) AS arvoluokka,
    array_to_string(array_agg(arvo.selite), ', '::text) AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=162&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'GK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1
    AND geometrytype (kohde.geometry1) ~~ '%LINE%'::text
GROUP BY
    kohde.id,
    luokka.nimi,
    jakelumetadata.id;

ALTER TABLE ltj_wfs_virka.arvokkaat_geologiset_viivamaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvokkaat_geologiset_viivamaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvokkaat_geologiset_viivamaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvokkaat_geologiset_viivamaiset TO ltj;

-- Virkaversio arvokkaat kasvikohteet:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvokkaat_kasvikohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=153&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'KK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.arvokkaat_kasvikohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvokkaat_kasvikohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvokkaat_kasvikohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvokkaat_kasvikohteet TO ltj;

-- Virkaversio arvokkaat lintukohteet:
CREATE OR REPLACE VIEW ltj_wfs_virka.arvokkaat_lintukohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=159&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.arvokkaat_lintukohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.arvokkaat_lintukohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.arvokkaat_lintukohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.arvokkaat_lintukohteet TO ltj;

-- Virkaversio ekologisten yhteyksien verkosto:
CREATE OR REPLACE VIEW ltj_wfs_virka.ekologiset_yhteydet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'VYHT'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.ekologiset_yhteydet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.ekologiset_yhteydet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.ekologiset_yhteydet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.ekologiset_yhteydet TO ltj;

-- Virkaversio lahokaviosammalen elinympäristöt:
CREATE OR REPLACE VIEW ltj_wfs_virka.lahokaviosammal_elinymparistot AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=327&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LKSE'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.lahokaviosammal_elinymparistot OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.lahokaviosammal_elinymparistot TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.lahokaviosammal_elinymparistot TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.lahokaviosammal_elinymparistot TO ltj;

-- Virkaversio lahokaviosammalen tukialueet:
CREATE OR REPLACE VIEW ltj_wfs_virka.lahokaviosammal_tukialueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=327&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LKST'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.lahokaviosammal_tukialueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.lahokaviosammal_tukialueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.lahokaviosammal_tukialueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.lahokaviosammal_tukialueet TO ltj;

-- Virkaversio luontoselvityksiä:
CREATE OR REPLACE VIEW ltj_wfs_virka.luontoselvityksia AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'SELV'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.luontoselvityksia OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.luontoselvityksia TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.luontoselvityksia TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.luontoselvityksia TO ltj;

-- Virkaversio biotoopit:
CREATE OR REPLACE VIEW ltj_wfs_virka.luontotyypit_biotooppiaineisto AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=180&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'BK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.luontotyypit_biotooppiaineisto OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.luontotyypit_biotooppiaineisto TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.luontotyypit_biotooppiaineisto TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.luontotyypit_biotooppiaineisto TO ltj;

-- Virkaversio luontotyypit:
CREATE OR REPLACE VIEW ltj_wfs_virka.luontotyypit_uhanalaiset AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=345&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'UHLT'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.luontotyypit_uhanalaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.luontotyypit_uhanalaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.luontotyypit_uhanalaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.luontotyypit_uhanalaiset TO ltj;

-- Virkaversio metsäverkosto:
CREATE OR REPLACE VIEW ltj_wfs_virka.metsaverkosto AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE (kohde.luokkatunnus::text = 'MVER'::text
    OR kohde.luokkatunnus::text = 'MLAA'::text
    OR kohde.luokkatunnus::text = 'MYHD'::text)
AND kohde.voimassa = TRUE
AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.metsaverkosto OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.metsaverkosto TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.metsaverkosto TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.metsaverkosto TO ltj;

-- Virkaversio eläinhavainnot:
CREATE OR REPLACE VIEW ltj_wfs_virka.muu_elainhavaintoja AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    lajirekisteri.nimi_suomi1 AS lajinimi,
    lajihavainto.pvm AS havainnon_paivamaara,
    havaintosarja.nimi AS havaintosarjan_nimi,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=168&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN lajihavainto ON kohde.id = lajihavainto.kohdeid
    JOIN lajirekisteri ON lajirekisteri.id = lajihavainto.lajid
    JOIN havaintosarja ON lajihavainto.hsaid = havaintosarja.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'EK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.muu_elainhavaintoja OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.muu_elainhavaintoja TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.muu_elainhavaintoja TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.muu_elainhavaintoja TO ltj;

-- Virkaversio perinnemaisemat:
-- huom avoimen datan puolella ei perinnemaisemia, koska aineisto ei ole kokonaan Helsingin omistuksessa

CREATE OR REPLACE VIEW ltj_wfs_virka.muu_perinnemaisemat AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    array_to_string(array_agg(arvo.luokka), ', '::text) AS arvoluokka,
    array_to_string(array_agg(arvo.selite), ', '::text) AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=169&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'PM'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1
GROUP BY
    kohde.id,
    luokka.nimi,
    jakelumetadata.id;

ALTER TABLE ltj_wfs_virka.muu_perinnemaisemat OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.muu_perinnemaisemat TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.muu_perinnemaisemat TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.muu_perinnemaisemat TO ltj;

-- Virkaversio muut luontokohteet:
CREATE OR REPLACE VIEW ltj_wfs_virka.muut_luontokohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=170&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'MUU'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.muut_luontokohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.muut_luontokohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.muut_luontokohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.muut_luontokohteet TO ltj;

-- Virkaversio rauhoitetut luonnonmuistomerkit:
CREATE OR REPLACE VIEW ltj_wfs_virka.rauh_luonnonmuistomerkit AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=157&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Lmm'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.rauh_luonnonmuistomerkit OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_luonnonmuistomerkit TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_luonnonmuistomerkit TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.rauh_luonnonmuistomerkit TO ltj;

-- Virkaversio rauhoitetut luonnonsuojelualueet:
CREATE OR REPLACE VIEW ltj_wfs_virka.rauh_luonnonsuojelualueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=154&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Lsa'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.rauh_luonnonsuojelualueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_luonnonsuojelualueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_luonnonsuojelualueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.rauh_luonnonsuojelualueet TO ltj;

-- Virkaversio rauhoitettavat luonnonsuojeluohjelma:
CREATE OR REPLACE VIEW ltj_wfs_virka.rauh_luonnonsuojeluohjelma AS
SELECT
    kohde.id,
    kohde.tunnus,
    'LSO'::character varying(10) AS luokkatunnus,
    'Luonnonsuojeluohjelman kohde'::character varying(50) AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=158&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LSO'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.rauh_luonnonsuojeluohjelma OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_luonnonsuojeluohjelma TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_luonnonsuojeluohjelma TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.rauh_luonnonsuojeluohjelma TO ltj;

-- Virkaversio rauhoitetut Natura aluemaiset:
CREATE OR REPLACE VIEW ltj_wfs_virka.rauh_natura_aluemaiset AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=155&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Natur'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1
    AND geometrytype (kohde.geometry1) ~~ '%POLYGON'::text;

ALTER TABLE ltj_wfs_virka.rauh_natura_aluemaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_natura_aluemaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_natura_aluemaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.rauh_natura_aluemaiset TO ltj;

-- Virkaversio rauhoitetut Natura viivamaiset:
CREATE OR REPLACE VIEW ltj_wfs_virka.rauh_natura_viivamaiset AS
SELECT
    kohde.id,
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
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=155&l=fi'::text AS metadata,
    'https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Natur'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3
    AND geometrytype (kohde.geometry1) ~~ '%LINE%'::text;

ALTER TABLE ltj_wfs_virka.rauh_natura_viivamaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_natura_viivamaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_natura_viivamaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.rauh_natura_viivamaiset TO ltj;

-- Virkaversio suojellut luontotyypit:
CREATE OR REPLACE VIEW ltj_wfs_virka.rauh_suojellut_luontotyypit AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    suoperuste.peruste,
    suoperuste.tarkperuste,
    suoperuste.alaperuste,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=156&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN suojelu ON kohde.id = suojelu.id
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN suo_peruste ON suojelu.id = suo_peruste.suoid
    LEFT JOIN suoperuste ON suo_peruste.perusteid = suoperuste.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LslLt'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.rauh_suojellut_luontotyypit OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_suojellut_luontotyypit TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.rauh_suojellut_luontotyypit TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.rauh_suojellut_luontotyypit TO ltj;

-- Virkaversio suojellut lajikohteet:
CREATE OR REPLACE VIEW ltj_wfs_virka.suojellut_lajikohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=174&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN suojelu ON kohde.id = suojelu.id
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Slaji'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.suojellut_lajikohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.suojellut_lajikohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.suojellut_lajikohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.suojellut_lajikohteet TO ltj;

-- Virkaversio tärkeät lintualueet:
CREATE OR REPLACE VIEW ltj_wfs_virka.tarkeat_lintualueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=340&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LK2'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.tarkeat_lintualueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.tarkeat_lintualueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.tarkeat_lintualueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.tarkeat_lintualueet TO ltj;

-- Virkaversio vesi - kunnostetut purokohdat:
CREATE OR REPLACE VIEW ltj_wfs_virka.vesi_kunnostetut_purokohdat AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=308&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'KUNN'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.vesi_kunnostetut_purokohdat OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_kunnostetut_purokohdat TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_kunnostetut_purokohdat TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.vesi_kunnostetut_purokohdat TO ltj;

-- Virkaversio vesi - lähteet:
CREATE OR REPLACE VIEW ltj_wfs_virka.vesi_lahteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=167&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LAH'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.vesi_lahteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_lahteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_lahteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.vesi_lahteet TO ltj;

-- Virkaversio vesi - lammet:
CREATE OR REPLACE VIEW ltj_wfs_virka.vesi_lammet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=165&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LAM'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.vesi_lammet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_lammet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_lammet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.vesi_lammet TO ltj;

-- Virkaversio vesi - purojen ja lampien valuma-alueet:
CREATE OR REPLACE VIEW ltj_wfs_virka.vesi_purojen_ja_lampien_valuma_alueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=166&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'PPV'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.vesi_purojen_ja_lampien_valuma_alueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_purojen_ja_lampien_valuma_alueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_purojen_ja_lampien_valuma_alueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.vesi_purojen_ja_lampien_valuma_alueet TO ltj;

-- Virkaversio vesi - purojen putkitetut osuudet:
CREATE OR REPLACE VIEW ltj_wfs_virka.vesi_purojen_putkitetut_osuudet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=269&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'PPUT'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.vesi_purojen_putkitetut_osuudet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_purojen_putkitetut_osuudet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_purojen_putkitetut_osuudet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.vesi_purojen_putkitetut_osuudet TO ltj;

-- Virkaversio vesi - purot:
CREATE OR REPLACE VIEW ltj_wfs_virka.vesi_purot AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=165&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'PPO'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.vesi_purot OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_purot TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_purot TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.vesi_purot TO ltj;

-- Virkaversio vedenlainen roskaantuminen:
CREATE OR REPLACE VIEW ltj_wfs_virka.vesi_vedenalainen_roskaantuminen AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=291&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'ROSK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.vesi_vedenalainen_roskaantuminen OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_vedenalainen_roskaantuminen TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_vedenalainen_roskaantuminen TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.vesi_vedenalainen_roskaantuminen TO ltj;

-- Virkaversio vesikasvilinjat:
CREATE OR REPLACE VIEW ltj_wfs_virka.vesi_vesikasvilinjat AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=289&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LITO'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid <> 1;

ALTER TABLE ltj_wfs_virka.vesi_vesikasvilinjat OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_vesikasvilinjat TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_virka.vesi_vesikasvilinjat TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_virka.vesi_vesikasvilinjat TO ltj;

-- Avoin data arvokkaat kääpäkohteet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvo_kaapakohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=163&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'KAAP'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.arvo_kaapakohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_kaapakohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_kaapakohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvo_kaapakohteet TO ltj;

-- Avoin data liito-oravien elinalueet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvo_liito_orava_elinalueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=296&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LIEL'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.arvo_liito_orava_elinalueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_liito_orava_elinalueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_liito_orava_elinalueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvo_liito_orava_elinalueet TO ltj;

-- Avoin data liito-oravien ydinalueet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvo_liito_orava_ydinalueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=296&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LIIT'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.arvo_liito_orava_ydinalueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_liito_orava_ydinalueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_liito_orava_ydinalueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvo_liito_orava_ydinalueet TO ltj;

-- Avoin data metsäkohteet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvo_metsakohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=164&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'METS'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.arvo_metsakohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_metsakohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_metsakohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvo_metsakohteet TO ltj;

-- Avoin data tärkeät lepakkoalueet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvo_tarkeat_lepakkoalueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=160&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LEPA'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.arvo_tarkeat_lepakkoalueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_tarkeat_lepakkoalueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_tarkeat_lepakkoalueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvo_tarkeat_lepakkoalueet TO ltj;

-- Avoin data tärkeät matelija ja sammakkoeläinkohteet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvo_tarkeat_matelija_ja_sammakkoelainkohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=161&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'MASA'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.arvo_tarkeat_matelija_ja_sammakkoelainkohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_tarkeat_matelija_ja_sammakkoelainkohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvo_tarkeat_matelija_ja_sammakkoelainkohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvo_tarkeat_matelija_ja_sammakkoelainkohteet TO ltj;

-- Avoin data arvokkaat geologiset kohteet aluemaiset:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvokkaat_geologiset_aluemaiset AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    array_to_string(array_agg(arvo.luokka), ', '::text) AS arvoluokka,
    array_to_string(array_agg(arvo.selite), ', '::text) AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=162&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'GK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3
    AND geometrytype (kohde.geometry1) ~~ '%POLYGON'::text
GROUP BY
    kohde.id,
    luokka.nimi,
    jakelumetadata.id;

ALTER TABLE ltj_wfs_avoin.arvokkaat_geologiset_aluemaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvokkaat_geologiset_aluemaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvokkaat_geologiset_aluemaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvokkaat_geologiset_aluemaiset TO ltj;

-- Avoin data arvokkaat geologiset kohteet viivamaiset:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvokkaat_geologiset_viivamaiset AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    array_to_string(array_agg(arvo.luokka), ', '::text) AS arvoluokka,
    array_to_string(array_agg(arvo.selite), ', '::text) AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=162&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'GK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3
    AND geometrytype (kohde.geometry1) ~~ '%LINE%'::text
GROUP BY
    kohde.id,
    luokka.nimi,
    jakelumetadata.id;

ALTER TABLE ltj_wfs_avoin.arvokkaat_geologiset_viivamaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvokkaat_geologiset_viivamaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvokkaat_geologiset_viivamaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvokkaat_geologiset_viivamaiset TO ltj;

-- Avoin data arvokkaat kasvikohteet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvokkaat_kasvikohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=153&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'KK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.arvokkaat_kasvikohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvokkaat_kasvikohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvokkaat_kasvikohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvokkaat_kasvikohteet TO ltj;

-- Avoin data arvokkaat lintukohteet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.arvokkaat_lintukohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    arvo.luokka AS arvoluokka,
    arvo.selite AS arvoluokan_selite,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=159&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN arvo_kohde ON kohde.id = arvo_kohde.kohdeid
    LEFT JOIN arvo ON arvo_kohde.arvoid = arvo.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.arvokkaat_lintukohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvokkaat_lintukohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.arvokkaat_lintukohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.arvokkaat_lintukohteet TO ltj;

-- Avoin data ekologisten yhteyksien verkosto:
CREATE OR REPLACE VIEW ltj_wfs_avoin.ekologiset_yhteydet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'VYHT'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.ekologiset_yhteydet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.ekologiset_yhteydet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.ekologiset_yhteydet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.ekologiset_yhteydet TO ltj;

-- Avoin data lahokaviosammalen elinympäristöt:
CREATE OR REPLACE VIEW ltj_wfs_avoin.lahokaviosammal_elinymparistot AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=327&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LKSE'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.lahokaviosammal_elinymparistot OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.lahokaviosammal_elinymparistot TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.lahokaviosammal_elinymparistot TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.lahokaviosammal_elinymparistot TO ltj;

-- Avoin data lahokaviosammalen tukialueet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.lahokaviosammal_tukialueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=327&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LKST'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.lahokaviosammal_tukialueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.lahokaviosammal_tukialueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.lahokaviosammal_tukialueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.lahokaviosammal_tukialueet TO ltj;

-- Avoin data biotooppikohteet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.luontotyypit_biotooppiaineisto AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=180&l=fi'::text AS metadata,
    'https://kartta.hel.fi/applications/ltj/reports/kohderaportti.aspx?id='::text || kohde.id AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'BK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.luontotyypit_biotooppiaineisto OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.luontotyypit_biotooppiaineisto TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.luontotyypit_biotooppiaineisto TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.luontotyypit_biotooppiaineisto TO ltj;

-- Avoin data metsäverkosto:
CREATE OR REPLACE VIEW ltj_wfs_avoin.metsaverkosto AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=322&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE (kohde.luokkatunnus::text = 'MVER'::text
    OR kohde.luokkatunnus::text = 'MLAA'::text
    OR kohde.luokkatunnus::text = 'MYHD'::text)
AND kohde.voimassa = TRUE
AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.metsaverkosto OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.metsaverkosto TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.metsaverkosto TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.metsaverkosto TO ltj;

-- Avoin data muut eläinhavainnot:
CREATE OR REPLACE VIEW ltj_wfs_avoin.muu_elainhavaintoja AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    lajirekisteri.nimi_suomi1 AS lajinimi,
    lajihavainto.pvm AS havainnon_paivamaara,
    havaintosarja.nimi AS havaintosarjan_nimi,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=168&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN lajihavainto ON kohde.id = lajihavainto.kohdeid
    JOIN lajirekisteri ON lajirekisteri.id = lajihavainto.lajid
    JOIN havaintosarja ON lajihavainto.hsaid = havaintosarja.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'EK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.muu_elainhavaintoja OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.muu_elainhavaintoja TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.muu_elainhavaintoja TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.muu_elainhavaintoja TO ltj;

-- Avoin data muut luontokohteet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.muut_luontokohteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=170&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'MUU'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.muut_luontokohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.muut_luontokohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.muut_luontokohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.muut_luontokohteet TO ltj;

-- Avoin data rauhoitetut luonnonmuistomerkit:
CREATE OR REPLACE VIEW ltj_wfs_avoin.rauh_luonnonmuistomerkit AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=157&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Lmm'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.rauh_luonnonmuistomerkit OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_luonnonmuistomerkit TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_luonnonmuistomerkit TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.rauh_luonnonmuistomerkit TO ltj;

-- Avoin data luonnonsuojelualueet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.rauh_luonnonsuojelualueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=154&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Lsa'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.rauh_luonnonsuojelualueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_luonnonsuojelualueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_luonnonsuojelualueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.rauh_luonnonsuojelualueet TO ltj;

-- Avoin data rauhoitettavat luonnonsuojeluohjelma:
CREATE OR REPLACE VIEW ltj_wfs_avoin.rauh_luonnonsuojeluohjelma AS
SELECT
    kohde.id,
    kohde.tunnus,
    'LSO'::character varying(10) AS luokkatunnus,
    'Luonnonsuojeluohjelman kohde'::character varying(50) AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=158&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LSO'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.rauh_luonnonsuojeluohjelma OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_luonnonsuojeluohjelma TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_luonnonsuojeluohjelma TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.rauh_luonnonsuojeluohjelma TO ltj;

-- Avoin data rauhoitetut naturat aluemaiset:
CREATE OR REPLACE VIEW ltj_wfs_avoin.rauh_natura_aluemaiset AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=155&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Natur'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3
    AND geometrytype (kohde.geometry1) ~~ '%POLYGON'::text;

ALTER TABLE ltj_wfs_avoin.rauh_natura_aluemaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_natura_aluemaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_natura_aluemaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.rauh_natura_aluemaiset TO ltj;

-- Avoin data rauhoitetut natura viivamaiset:
CREATE OR REPLACE VIEW ltj_wfs_avoin.rauh_natura_viivamaiset AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=155&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'Natur'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3
    AND geometrytype (kohde.geometry1) ~~ '%LINE%'::text;

ALTER TABLE ltj_wfs_avoin.rauh_natura_viivamaiset OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_natura_viivamaiset TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_natura_viivamaiset TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.rauh_natura_viivamaiset TO ltj;

-- Avoin data suojellut luontotyypit:
CREATE OR REPLACE VIEW ltj_wfs_avoin.rauh_suojellut_luontotyypit AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    suoperuste.peruste,
    suoperuste.tarkperuste,
    suoperuste.alaperuste,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=156&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN suojelu ON kohde.id = suojelu.id
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    LEFT JOIN suo_peruste ON suojelu.id = suo_peruste.suoid
    LEFT JOIN suoperuste ON suo_peruste.perusteid = suoperuste.id
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LslLt'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.rauh_suojellut_luontotyypit OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_suojellut_luontotyypit TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.rauh_suojellut_luontotyypit TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.rauh_suojellut_luontotyypit TO ltj;

-- Avoin data tärkeät lintualueet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.tarkeat_lintualueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=340&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LK2'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.tarkeat_lintualueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.tarkeat_lintualueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.tarkeat_lintualueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.tarkeat_lintualueet TO ltj;

-- Avoin data vesi - lähteet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.vesi_lahteet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=167&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LAH'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.vesi_lahteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_lahteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_lahteet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.vesi_lahteet TO ltj;

-- Avoin data vesi - lammet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.vesi_lammet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=165&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LAM'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.vesi_lammet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_lammet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_lammet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.vesi_lammet TO ltj;

-- Avoin data vesi - purojen ja lampien valuma-alueet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.vesi_purojen_ja_lampien_valuma_alueet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=166&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'PPV'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.vesi_purojen_ja_lampien_valuma_alueet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_purojen_ja_lampien_valuma_alueet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_purojen_ja_lampien_valuma_alueet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.vesi_purojen_ja_lampien_valuma_alueet TO ltj;

-- Avoin data vesi - purojen putkitetut osuudet:
CREATE OR REPLACE VIEW ltj_wfs_avoin.vesi_purojen_putkitetut_osuudet AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=269&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'PPUT'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.vesi_purojen_putkitetut_osuudet OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_purojen_putkitetut_osuudet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_purojen_putkitetut_osuudet TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.vesi_purojen_putkitetut_osuudet TO ltj;

-- Avoin data vesi - purot:
CREATE OR REPLACE VIEW ltj_wfs_avoin.vesi_purot AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=165&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'PPO'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.vesi_purot OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_purot TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_purot TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.vesi_purot TO ltj;

-- Avoin data vedenalainen roskaantuminen:
CREATE OR REPLACE VIEW ltj_wfs_avoin.vesi_vedenalainen_roskaantuminen AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.suojaustasoid,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    kohde.teksti AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=291&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'ROSK'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.vesi_vedenalainen_roskaantuminen OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_vedenalainen_roskaantuminen TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_vedenalainen_roskaantuminen TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.vesi_vedenalainen_roskaantuminen TO ltj;

-- Avoin data vesikasvilinjat:
CREATE OR REPLACE VIEW ltj_wfs_avoin.vesi_vesikasvilinjat AS
SELECT
    kohde.id,
    kohde.tunnus,
    kohde.luokkatunnus,
    luokka.nimi AS luokan_nimi,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.pinta_ala AS pinta_ala_ha,
    kohde.geometry1,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS kohdeteksti,
    'https://kartta.hel.fi/paikkatietohakemisto/metadata/?id=289&l=fi'::text AS metadata,
    ('https://kartta.hel.fi/ltj/feature-report/'::text || kohde.id) || '/'::text AS kohderaportti,
    jakelumetadata.datanomistaja,
    jakelumetadata.paivitetty_tietopalveluun
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN jakelumetadata ON jakelumetadata.id = 1
WHERE
    kohde.luokkatunnus::text = 'LITO'::text
    AND kohde.voimassa = TRUE
    AND kohde.suojaustasoid = 3;

ALTER TABLE ltj_wfs_avoin.vesi_vesikasvilinjat OWNER TO ltj;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_vesikasvilinjat TO ltj_yllapito;

GRANT SELECT ON TABLE ltj_wfs_avoin.vesi_vesikasvilinjat TO ltj_katselu;

GRANT ALL ON TABLE ltj_wfs_avoin.vesi_vesikasvilinjat TO ltj;

-- ltj_kohteet-view for SpatialWeb
CREATE OR REPLACE VIEW ltj.ltj_kohteet AS
SELECT
    kohde.id,
    st_force2d (kohde.geometry1)::geometry(Geometry, 3879) AS geometry1,
    COALESCE(kohde.tunnus, kohde.id::character varying(10)) AS tunnus,
    kohde.luokkatunnus,
    kohde.nimi,
    kohde.kuvaus,
    kohde.huom,
    kohde.voimassa,
    kohde.numero,
    kohde.pinta_ala,
    kohde.suojaustasoid AS suojaustasokohde,
    kohde.teksti AS tieto,
    CASE WHEN NOT kohde.teksti_www::text = ''::text THEN
        kohde.teksti_www
    ELSE
        kohde.teksti
    END AS tieto_www,
    array_to_string(array_agg(arvo.luokka), ', '::text) AS suojelu_arvo_luokka,
    array_to_string(array_agg(arvo.selite), ', '::text) AS suojelu_arvo_selite
FROM
    kohde
    LEFT JOIN arvo_kohde ON arvo_kohde.kohdeid = kohde.id
    LEFT JOIN arvo ON arvo.id = arvo_kohde.arvoid
WHERE
    kohde.voimassa
    AND st_isvalid (kohde.geometry1)
GROUP BY
    kohde.id;

ALTER TABLE ltj.ltj_kohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj.ltj_kohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj.ltj_kohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj.ltj_kohteet TO ltj;

-- ltj_lajikohteet-view for SpatialWeb
CREATE OR REPLACE VIEW ltj.ltj_lajikohteet AS
SELECT
    kohde.id,
    kohde.luokkatunnus,
    kohde.tunnus,
    kohde.nimi,
    st_force2d (kohde.geometry1)::geometry(Geometry, 3879) AS geometry1,
    kohde.suojaustasoid AS suojaustasokohde,
    lajihavainto.suojaustasoid AS suojaustasohavainto,
    lajirekisteri.suojaustasoid AS suojaustasolaji,
    luokka.nimi AS luokka,
    luokka.www AS luokka_www,
    lajihavainto.lajid
FROM
    kohde
    JOIN luokka ON luokka.tunnus::text = kohde.luokkatunnus::text
    JOIN lajihavainto ON kohde.id = lajihavainto.kohdeid
    JOIN lajirekisteri ON lajihavainto.lajid = lajirekisteri.id
WHERE
    kohde.voimassa
    AND st_isvalid (kohde.geometry1);

ALTER TABLE ltj.ltj_lajikohteet OWNER TO ltj;

GRANT SELECT ON TABLE ltj.ltj_lajikohteet TO ltj_yllapito;

GRANT SELECT ON TABLE ltj.ltj_lajikohteet TO ltj_katselu;

GRANT ALL ON TABLE ltj.ltj_lajikohteet TO ltj;
