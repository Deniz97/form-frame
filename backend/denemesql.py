import mysql.connector

db = mysql.connector.connect(   
                     user="ada",         # your username
                     passwd="ada123", 
                     host="localhost",
                     db="ada_db")        # name of the data base
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
http_data = "'kasko'"
	# Use all the SQL you like
cur.execute("SELECT info FROM sellform WHERE type="+ http_data)
	# print all the first cell of all the rows
retval = "["
for row in cur.fetchall():
    retval += row[0]+","
retval += "]"
print retval
db.close()