/*
SQL script to change the table owner to mooringbooking_dev

Target table: all the tables starting with the name django_ or mooring_ or auth_ or taggit.
Run the following command as a user: postgres
psql -d mooringbooking_dev -f path/to/this/sql/file
*/

DO $$ 
DECLARE 
    t_name text;
BEGIN 
    FOR t_name IN 
        SELECT tables.table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND (
            tables.table_name LIKE 'django_%' OR
            tables.table_name LIKE 'mooring_%' OR
            tables.table_name LIKE 'auth_%' OR
            tables.table_name LIKE 'taggit_%'
        )
    LOOP 
        EXECUTE format('ALTER TABLE %I OWNER TO mooringbooking_dev', t_name);
        RAISE NOTICE 'Changed owner of table % to mooringbooking_dev', t_name;
    END LOOP; 
END $$;