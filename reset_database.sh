# Drop the database, then create it
dropdb 'inventory'
createdb 'inventory'

# Add all the relations and data to the database
psql -d inventory -c "\i dbTables.sql"

