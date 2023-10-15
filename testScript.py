import psycopg2
import sys

# Before running this script, make sure you've started the database server on your computer

# check that the user is inputted
if len(sys.argv) != 2:
    print('Please provide your user as an argument to the script.')
    exit(1)

# Establish a connection to the Database
connection = psycopg2.connect(database="inventory", host="/tmp", user=sys.argv[1], password="", port="8888")

# Create a cursor for interacting with the database
cursor = connection.cursor()

# Attempt a test query, and retrieve the output of the query
# cursor.execute("SELECT * FROM PART")
# print(cursor.fetchmany(size=3))

# Close the connection
cursor.close()
connection.close()
print("Program terminated normally.")