dropdb 'inventory'
createdb 'inventory'
psql -d inventory -c "\i dbTables.sql"