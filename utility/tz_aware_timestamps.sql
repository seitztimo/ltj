--
-- Convert all timestamp without time zone columns to timestamp with time zones
-- If there are views depending on these columns, the views must be dropped and
-- re-created.
--

ALTER TABLE ltj.kohde_historia ALTER COLUMN pvm_editoitu TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.kohde_historia ALTER COLUMN pvm_editoitu TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.kohde_historia ALTER COLUMN historia_pvm TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.ltyyppihavainto ALTER COLUMN pvm_luotu TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.ltyyppihavainto ALTER COLUMN pvm_editoitu TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.lajirekisteri ALTER COLUMN rekisteripvm TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.lajihavainto ALTER COLUMN pvm_luotu TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.lajihavainto ALTER COLUMN pvm_editoitu TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.kohde ALTER COLUMN pvm_editoitu TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.saados ALTER COLUMN voimaantulo TYPE TIMESTAMP WITH TIME ZONE;
ALTER TABLE ltj.henkilo ALTER COLUMN lisaysaika TYPE TIMESTAMP WITH TIME ZONE;
