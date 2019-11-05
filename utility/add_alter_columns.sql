--
-- The database seems to have multiple schemas, and the tables
-- are created in ltj schema.
--
SET search_path=ltj;

--
-- The version of database we have are missing following changes that are needed
--

ALTER TABLE lajihavainto ADD COLUMN hav_koodi VARCHAR(100);
ALTER TABLE lajirekisteri ALTER COLUMN koodi TYPE VARCHAR(100);
