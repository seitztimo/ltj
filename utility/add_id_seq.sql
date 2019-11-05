--
-- This script is to fix various issues in legacy database.
-- It should be run on the database before running any
-- nature migrations.
--

--
-- The database seems to have multiple schemas, and the tables
-- are created in ltj schema.
--
SET search_path=ltj;

--
-- Add sequences to id fields
--
-- The sequences for the id fields are missing in legacy database.
--

-- alkupera
CREATE SEQUENCE IF NOT EXISTS alkupera_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE alkupera_id_seq OWNED BY alkupera.id;

ALTER TABLE ONLY alkupera ALTER COLUMN id SET DEFAULT nextval('alkupera_id_seq'::regclass);

-- arvo
CREATE SEQUENCE IF NOT EXISTS arvo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE arvo_id_seq OWNED BY arvo.id;

ALTER TABLE ONLY arvo ALTER COLUMN id SET DEFAULT nextval('arvo_id_seq'::regclass);

-- esiintyma
CREATE SEQUENCE IF NOT EXISTS esiintyma_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE esiintyma_id_seq OWNED BY esiintyma.id;

ALTER TABLE ONLY esiintyma ALTER COLUMN id SET DEFAULT nextval('esiintyma_id_seq'::regclass);

-- havaintosarja
CREATE SEQUENCE IF NOT EXISTS havaintosarja_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE havaintosarja_id_seq OWNED BY havaintosarja.id;

ALTER TABLE ONLY havaintosarja ALTER COLUMN id SET DEFAULT nextval('havaintosarja_id_seq'::regclass);

-- henkilo
CREATE SEQUENCE IF NOT EXISTS henkilo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE henkilo_id_seq OWNED BY henkilo.id;

ALTER TABLE ONLY henkilo ALTER COLUMN id SET DEFAULT nextval('henkilo_id_seq'::regclass);

-- julkaisu
CREATE SEQUENCE IF NOT EXISTS julkaisu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE julkaisu_id_seq OWNED BY julkaisu.id;

ALTER TABLE ONLY julkaisu ALTER COLUMN id SET DEFAULT nextval('julkaisu_id_seq'::regclass);

-- julktyyppi
CREATE SEQUENCE IF NOT EXISTS julktyyppi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE julktyyppi_id_seq OWNED BY julktyyppi.id;

ALTER TABLE ONLY julktyyppi ALTER COLUMN id SET DEFAULT nextval('julktyyppi_id_seq'::regclass);

-- kohde
CREATE SEQUENCE IF NOT EXISTS kohde_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE kohde_id_seq OWNED BY kohde.id;

ALTER TABLE ONLY kohde ALTER COLUMN id SET DEFAULT nextval('kohde_id_seq'::regclass);

-- kohdelinkki
CREATE SEQUENCE IF NOT EXISTS kohdelinkki_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE kohdelinkki_id_seq OWNED BY kohdelinkki.id;

ALTER TABLE ONLY kohdelinkki ALTER COLUMN id SET DEFAULT nextval('kohdelinkki_id_seq'::regclass);

-- lajihavainto
CREATE SEQUENCE IF NOT EXISTS lajihavainto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE lajihavainto_id_seq OWNED BY lajihavainto.id;

ALTER TABLE ONLY lajihavainto ALTER COLUMN id SET DEFAULT nextval('lajihavainto_id_seq'::regclass);

-- lajirekisteri
CREATE SEQUENCE IF NOT EXISTS lajirekisteri_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE lajirekisteri_id_seq OWNED BY lajirekisteri.id;

ALTER TABLE ONLY lajirekisteri ALTER COLUMN id SET DEFAULT nextval('lajirekisteri_id_seq'::regclass);

-- liikkumislk
CREATE SEQUENCE IF NOT EXISTS liikkumislk_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE liikkumislk_id_seq OWNED BY liikkumislk.id;

ALTER TABLE ONLY liikkumislk ALTER COLUMN id SET DEFAULT nextval('liikkumislk_id_seq'::regclass);

-- linkkityyppi
CREATE SEQUENCE IF NOT EXISTS linkkityyppi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE linkkityyppi_id_seq OWNED BY linkkityyppi.id;

ALTER TABLE ONLY linkkityyppi ALTER COLUMN id SET DEFAULT nextval('linkkityyppi_id_seq'::regclass);

-- ltyyppihavainto
CREATE SEQUENCE IF NOT EXISTS ltyyppihavainto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ltyyppihavainto_id_seq OWNED BY ltyyppihavainto.id;

ALTER TABLE ONLY ltyyppihavainto ALTER COLUMN id SET DEFAULT nextval('ltyyppihavainto_id_seq'::regclass);

-- ltyyppirekisteri
CREATE SEQUENCE IF NOT EXISTS ltyyppirekisteri_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE ltyyppirekisteri_id_seq OWNED BY ltyyppirekisteri.id;

ALTER TABLE ONLY ltyyppirekisteri ALTER COLUMN id SET DEFAULT nextval('ltyyppirekisteri_id_seq'::regclass);

-- pesimisvarmuus
CREATE SEQUENCE IF NOT EXISTS pesimisvarmuus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE pesimisvarmuus_id_seq OWNED BY pesimisvarmuus.id;

ALTER TABLE ONLY pesimisvarmuus ALTER COLUMN id SET DEFAULT nextval('pesimisvarmuus_id_seq'::regclass);

-- runsaus
CREATE SEQUENCE IF NOT EXISTS runsaus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE runsaus_id_seq OWNED BY runsaus.id;

ALTER TABLE ONLY runsaus ALTER COLUMN id SET DEFAULT nextval('runsaus_id_seq'::regclass);

-- saados
CREATE SEQUENCE IF NOT EXISTS saados_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE saados_id_seq OWNED BY saados.id;

ALTER TABLE ONLY saados ALTER COLUMN id SET DEFAULT nextval('saados_id_seq'::regclass);

-- sohjelma
CREATE SEQUENCE IF NOT EXISTS sohjelma_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE sohjelma_id_seq OWNED BY sohjelma.id;

ALTER TABLE ONLY sohjelma ALTER COLUMN id SET DEFAULT nextval('sohjelma_id_seq'::regclass);

-- suojaustaso
CREATE SEQUENCE IF NOT EXISTS suojaustaso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE suojaustaso_id_seq OWNED BY suojaustaso.id;

ALTER TABLE ONLY suojaustaso ALTER COLUMN id SET DEFAULT nextval('suojaustaso_id_seq'::regclass);

-- suoperuste
CREATE SEQUENCE IF NOT EXISTS suoperuste_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE suoperuste_id_seq OWNED BY suoperuste.id;

ALTER TABLE ONLY suoperuste ALTER COLUMN id SET DEFAULT nextval('suoperuste_id_seq'::regclass);

-- tapahtuma
CREATE SEQUENCE IF NOT EXISTS tapahtuma_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE tapahtuma_id_seq OWNED BY tapahtuma.id;

ALTER TABLE ONLY tapahtuma ALTER COLUMN id SET DEFAULT nextval('tapahtuma_id_seq'::regclass);

-- tapahtumatyyppi
CREATE SEQUENCE IF NOT EXISTS tapahtumatyyppi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE tapahtumatyyppi_id_seq OWNED BY tapahtumatyyppi.id;

ALTER TABLE ONLY tapahtumatyyppi ALTER COLUMN id SET DEFAULT nextval('tapahtumatyyppi_id_seq'::regclass);

-- yleisyys
CREATE SEQUENCE IF NOT EXISTS yleisyys_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE yleisyys_id_seq OWNED BY yleisyys.id;

ALTER TABLE ONLY yleisyys ALTER COLUMN id SET DEFAULT nextval('yleisyys_id_seq'::regclass);

--
-- Add id field to m2m through table
--
-- The m2m through tables in legacy database have multi-column
-- primary keys, which is not supported by django. We need to
-- drop multi-column primary key and create an id field as new
-- primary key.
--

-- arvo_kohde
ALTER TABLE arvo_kohde DROP CONSTRAINT arvo_kohde_pkey;
ALTER TABLE arvo_kohde ADD COLUMN id SERIAL PRIMARY KEY;

-- kohde_julk
ALTER TABLE kohde_julk DROP CONSTRAINT kohde_julk_pkey;
ALTER TABLE kohde_julk ADD COLUMN id SERIAL PRIMARY KEY;

-- laj_saa
ALTER TABLE laj_saa DROP CONSTRAINT laj_saa_pkey;
ALTER TABLE laj_saa ADD COLUMN id SERIAL PRIMARY KEY;

-- ltyyppi_saados
ALTER TABLE ltyyppi_saados DROP CONSTRAINT ltyyppi_saados_pkey;
ALTER TABLE ltyyppi_saados ADD COLUMN id SERIAL PRIMARY KEY;

-- suo_peruste
ALTER TABLE suo_peruste DROP CONSTRAINT suo_peruste_pkey;
ALTER TABLE suo_peruste ADD COLUMN id SERIAL PRIMARY KEY;

-- suojelu_sohjelma
ALTER TABLE suojelu_sohjelma DROP CONSTRAINT suojelu_sohjelma_pkey;
ALTER TABLE suojelu_sohjelma ADD COLUMN id SERIAL PRIMARY KEY;

-- tap_saados
ALTER TABLE tap_saados DROP CONSTRAINT tap_saados_pkey;
ALTER TABLE tap_saados ADD COLUMN id SERIAL PRIMARY KEY;

-- tapahtuma_kohde
ALTER TABLE tapahtuma_kohde DROP CONSTRAINT tapahtuma_kohde_pkey;
ALTER TABLE tapahtuma_kohde ADD COLUMN id SERIAL PRIMARY KEY;

--
-- Reset the sequences for the id field.
--
-- This part of sql script is automatically generated by:
--   python manage.py sqlsequencereset
--

BEGIN;
SELECT setval(pg_get_serial_sequence('"alkupera"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "alkupera";
SELECT setval(pg_get_serial_sequence('"arvo"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "arvo";
SELECT setval(pg_get_serial_sequence('"arvo_kohde"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "arvo_kohde";
SELECT setval(pg_get_serial_sequence('"esiintyma"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "esiintyma";
SELECT setval(pg_get_serial_sequence('"havaintosarja"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "havaintosarja";
SELECT setval(pg_get_serial_sequence('"henkilo"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "henkilo";
SELECT setval(pg_get_serial_sequence('"julkaisu"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "julkaisu";
SELECT setval(pg_get_serial_sequence('"julktyyppi"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "julktyyppi";
SELECT setval(pg_get_serial_sequence('"kohde"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "kohde";
SELECT setval(pg_get_serial_sequence('"kohde_julk"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "kohde_julk";
SELECT setval(pg_get_serial_sequence('"kohdelinkki"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "kohdelinkki";
SELECT setval(pg_get_serial_sequence('"laj_saa"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "laj_saa";
SELECT setval(pg_get_serial_sequence('"lajihavainto"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "lajihavainto";
SELECT setval(pg_get_serial_sequence('"lajirekisteri"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "lajirekisteri";
SELECT setval(pg_get_serial_sequence('"liikkumislk"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "liikkumislk";
SELECT setval(pg_get_serial_sequence('"linkkityyppi"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "linkkityyppi";
SELECT setval(pg_get_serial_sequence('"ltyyppi_saados"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "ltyyppi_saados";
SELECT setval(pg_get_serial_sequence('"ltyyppihavainto"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "ltyyppihavainto";
SELECT setval(pg_get_serial_sequence('"ltyyppirekisteri"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "ltyyppirekisteri";
SELECT setval(pg_get_serial_sequence('"pesimisvarmuus"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "pesimisvarmuus";
SELECT setval(pg_get_serial_sequence('"runsaus"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "runsaus";
SELECT setval(pg_get_serial_sequence('"saados"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "saados";
SELECT setval(pg_get_serial_sequence('"sohjelma"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "sohjelma";
SELECT setval(pg_get_serial_sequence('"suo_peruste"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "suo_peruste";
SELECT setval(pg_get_serial_sequence('"suojaustaso"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "suojaustaso";
SELECT setval(pg_get_serial_sequence('"suojelu_sohjelma"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "suojelu_sohjelma";
SELECT setval(pg_get_serial_sequence('"suoperuste"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "suoperuste";
SELECT setval(pg_get_serial_sequence('"tap_saados"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tap_saados";
SELECT setval(pg_get_serial_sequence('"tapahtuma"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tapahtuma";
SELECT setval(pg_get_serial_sequence('"tapahtuma_kohde"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tapahtuma_kohde";
SELECT setval(pg_get_serial_sequence('"tapahtumatyyppi"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tapahtumatyyppi";
SELECT setval(pg_get_serial_sequence('"yleisyys"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "yleisyys";
COMMIT;
