import BaseHTTPServer 
import socket
import mysql.connector
import sys
import SocketServer
import json
from pprint import pprint



PORT_NUMBER = 8888

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	
	def do_OPTIONS(self):           
		print "Catched a OPTIONS request"
		self.send_response(200)       
		self.send_header('Access-Control-Allow-Origin', '*')                
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header("Access-Control-Allow-Headers","origin, x-requested-with, content-type")
		self.send_header('Content-Length', '0')
		self.send_header('Connection', 'Keep-Alive')
	    	self.end_headers()
	    	print "Finished OPTION headers"
	    	return

	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("Hello World !")
		return
	def do_POST(self):
		def queryByTable(table, police_type):
			db = mysql.connector.connect(   
			                     user="ada",         # your username
			                     passwd="ada123", 
			                     host="localhost",
			                     db="ada_db")        # name of the data base

			# you must create a Cursor object. It will let
			#  you execute all the queries you need
			cur = db.cursor()
			# Use all the SQL you like
			query = "SELECT info FROM %s WHERE type=\'%s\'" % (table, police_type)
			cur.execute(query)

			retval=""
			for row in cur.fetchall():
			    retval += row[0]+","
			retval=retval[:-1]
			db.close()
			return retval

		def sellformRequest(http_data):
			self.send_response(200,"OK")
			self.send_header('Content-Type','text/plain')
			self.send_header('Access-Control-Allow-Origin', '*')             
			
			table = "sellform"
			police_type = http_data["police_type"]
			retval = queryByTable( table, police_type )	

			# Send the html message
			#content_length = sys.getsizeof(retval)
			content_length = len(retval)
			self.send_header("Content-Length",str(content_length) )
			self.end_headers()
			self.wfile.write(retval)
			return
		
		def fiyatformRequest(http_data):
			pass
		def policeformRequest(http_data):
			pass

		length = int(self.headers['content-length'])
		http_data = self.rfile.read(length)
		http_data = json.loads(http_data)
		print http_data
		if http_data["request_type"] == "sellform":
			sellformRequest(http_data)
		if http_data["request_type"] == "fiyatform":
			fiyatformRequest(http_data)
		if http_data["request_type"] == "policeform":
			policeformRequest(http_data)

class ForkingHTTPServer(SocketServer.ForkingMixIn, BaseHTTPServer.HTTPServer):
    def finish_request(self, request, client_address):
        request.settimeout(30)
        # "super" can not be used because BaseServer is not created from object
        BaseHTTPServer.HTTPServer.finish_request(self, request, client_address)


def httpd(handler_class=myHandler, server_address=('localhost', 8888)):
    try:
        print 'Started httpserver on port 8888' 
        srvr = ForkingHTTPServer(server_address, handler_class)
        srvr.serve_forever()  # serve_forever
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        srvr.socket.close()




if __name__ == "__main__":
    httpd()

