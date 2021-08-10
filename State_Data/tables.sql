-- Create tables
begin transaction;
CREATE TABLE IF NOT EXISTS precinct (STATE TEXT collate nocase, PRECINCT TEXT collate nocase, DISTRICT TEXT collate nocase, PARTY TEXT collate nocase, VOTERS INT);
CREATE TABLE IF NOT EXISTS party (id TEXT collate nocase, name TEXT collate nocase);
commit;

-- create a party table to standardize the party values from multiple sources
begin transaction;
insert into party VALUES ("DEM", "Democratic");
insert into party VALUES ("REP", "Republican");
insert into party VALUES ("LBT", "Libertarian");
insert into party VALUES ("GRN", "Green");
insert into party VALUES ("OTH", "Other");
insert into party VALUES ("IND", "Independent");
insert into party VALUES ("AKI", "Alaska Independent");
insert into party VALUES ("CONST", "Constitution");
insert into party VALUES ("REFORM", "Reform");
insert into party VALUES ("SOCWK", "Socialist");
commit;
