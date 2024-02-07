import sqlite3

conn = sqlite3.connect('guests.db')
print("Opened database successfully")

# Create a table
conn.execute(
    '''
    CREATE TABLE guests
    (id INTEGER PRIMARY KEY, name TEXT, firstname TEXT, number_guests INTEGER, is_present BOOLEAN, message TEXT)
'''
)
print("Table created successfully")

# Close the connection
conn.close()
