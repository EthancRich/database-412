# Drop the database, then create it
dropdb 'db'
createdb 'db'

# Add all the relations and data to the database
psql -d db -c "\i dbTables.sql"

