--
-- This script adds comment that describes the values of
-- protection_level columns.
--
-- The main reason we add the comments is because the database
-- can be edited outside the django application (e.g. QGIS),
-- where user have no knowledge on the values.
--

SET search_path=public;


COMMENT ON COLUMN kohde.suojaustasoid IS '1: Vain ylläpitäjille. 2: Vain ylläpitäjille ja virkakatselijoille. 3. Saa näyttää Internetissä, oletusarvo';
COMMENT ON COLUMN kohdelinkki.suojaustasoid IS '1: Vain ylläpitäjille. 2: Vain ylläpitäjille ja virkakatselijoille. 3. Saa näyttää Internetissä, oletusarvo';
COMMENT ON COLUMN lajihavainto.suojaustasoid IS '1: Vain ylläpitäjille. 2: Vain ylläpitäjille ja virkakatselijoille. 3. Saa näyttää Internetissä, oletusarvo';
COMMENT ON COLUMN lajirekisteri.suojaustasoid IS '1: Vain ylläpitäjille. 2: Vain ylläpitäjille ja virkakatselijoille. 3. Saa näyttää Internetissä, oletusarvo';
COMMENT ON COLUMN tapahtuma.suojaustasoid IS '1: Vain ylläpitäjille. 2: Vain ylläpitäjille ja virkakatselijoille. 3. Saa näyttää Internetissä, oletusarvo';
