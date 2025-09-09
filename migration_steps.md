## Step 1: Create new database.
```
CREATE DATABASE mooringbooking_dev;
CREATE USER mooringbooking_dev WITH PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE "mooringbooking_dev" to mooringbooking_dev;
\c mooringbooking_dev
create extension postgis;
GRANT ALL ON ALL TABLES IN SCHEMA public TO mooringbooking_dev;
GRANT ALL ON SCHEMA public TO mooringbooking_dev;
```

## Step 2: Dump from ledger_prod
```
pg_dump -U <username> -W -t 'mooring_*' -t 'django_*' -t 'taggit_*' -t 'auth_group' -t 'auth_permission' ledger_prod -h <host> > mooring_prod_YYYY_MM_DD.sql
```


## Step 3: Import database
```
psql -U <username> <database> -W -h <host> < mooring_prod_YYYY_MM_DD.sql
```


## Step 4: Fix migrations
```
Run on migrated database
CREATE TABLE django_migrations_temp AS SELECT * from django_migrations;
```


## Step 5: Delete migrations
```
delete from django_migrations where id > 11;
```


## Step 6: Run Migrations
```
./manage_mo.py migrate ledger_api_client
```

## Step 7 Reinsert the migrations that were deleted in Step5
```
insert into django_migrations (id,app,name,applied) select * from  django_migrations_temp  where id > 11;
```


## Step 8: Delete django cron migrations so they can be created form initial migration
```
delete from django_migrations where app = 'django_cron';
```

## Step 9: Drop the django_cron table
```
drop table django_cron_cronjoblog;
```


## Step 10: Run Migrations for admin and django_cron
```
./manage_mo.py migrate admin
./manage_mo.py migrate django_cron
```


## Step 11: Run Migrations on mooring
```
./manage_mo.py migrate mooring
```

## Step 12: Run remianing migrations
```
./manage_mo.py migrate
```
