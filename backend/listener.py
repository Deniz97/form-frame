from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import socket
import MySQLdb

PORT_NUMBER = 8888

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("Hello World !")
		return
	def do_POST(self):
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		#Go to database


		db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		                     user="ada",         # your username
		                     passwd="ada123",  # your password
		                     db="ada_db")        # name of the data base

		# you must create a Cursor object. It will let
		#  you execute all the queries you need
		cur = db.cursor()
		http_data = self.rfile.read()

		# Use all the SQL you like
		cur.execute("SELECT p.info FROM policeler p WHERE p.tip="+ http_data)

		# print all the first cell of all the rows
		retval = "["
		for row in cur.fetchall():
		    retval += row[0]

		retval += "]"
		db.close()


		# Send the html message
		self.wfile.write(retval)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()