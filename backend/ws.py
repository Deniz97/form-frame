import json
import socket, struct, hashlib, threading, base64
from email.utils import formatdate
import array


clients = []

def adaWebServer():
	GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
	def httpDateHand(dt):
		
		"""Return a string representation of a date according to RFC 1123
		(HTTP/1.1).
		The supplied date must be in UTC.
		"""
		weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
		month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
			"Oct", "Nov", "Dec"][dt.month - 1]
		return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
			dt.year, dt.hour, dt.minute, dt.second)
	def httpDate():
		return formatdate(timeval=None, localtime=False, usegmt=True)

	def alertAdaServer(data, sock):		
		print "Sending to ada server=",
		print str(data["infos"])
		sock.send(str(data["infos"]))

	def getOfferCount():
		pass

	def getOffer(sock):
		return sock.recv(1024)

	def deliverToClient(reply,conn):
		print "Reply Data=",
		print str(reply)
		sendData(conn,str(reply))

	def readData(conn):
		try:
			data = conn.recv(2)
			print "reading data"
			
			head1, head2 = struct.unpack('!BB', data)
			fin = bool(head1 & 0b10000000)
			opcode = head1 & 0b00001111
			if opcode == 1:
				length = head2 & 0b01111111
				if length == 126:
					data = conn.recv(2)
					length, = struct.unpack('!H', data)
				elif length == 127:
					data = conn.recv(8)
					length, = struct.unpack('!Q', data)

				mask_bits = conn.recv(4)
				mask_bits = bytearray(mask_bits)
				data = conn.recv(length)
				data = bytearray(data)
				DECODED = []
				for i in range(0, len(data)):
					DECODED.append(data[i] ^ mask_bits[i % 4])
				DECODED = array.array('B', DECODED).tostring()
				if fin:
					return DECODED
		except Exception, e:
			err = e.args[0]
			# this next if/else is a bit redundant, but illustrates how the
			# timeout exception is setup
			if err == 'timed out':
				pass
			elif err == 10053:
				return None
			else:
				print(e)
				exit()

	def sendData(conn, data, fin=True, opcode=1, masking_key=False):
		if fin > 0x1:
			raise ValueError('FIN bit parameter must be 0 or 1')
		if 0x3 <= opcode <= 0x7 or 0xB <= opcode:
			raise ValueError('Opcode cannot be a reserved opcode')
		try:
			header = struct.pack('!B', ((fin << 7)
				| (0 << 6)
				| (0 << 5)
				| (0 << 4)
				| opcode))
			if masking_key:
				mask_bit = 1 << 7
			else:
				mask_bit = 0

			length = len(data)
			if length < 126:
				header += struct.pack('!B', (mask_bit | length))
			elif length < (1 << 16):
				header += struct.pack('!B', (mask_bit | 126)) + struct.pack('!H', length)
			elif length < (1 << 63):
				header += struct.pack('!B', (mask_bit | 127)) + struct.pack('!Q', length)

			body = data
			for i in [conn]:
				client = conn
				try:
					client.send(bytes(header + body))
					print("Sending= ",header+body)
				except IOError, e:
					print('error writing - %s' % data)
		except Exception, e:
			print(format())
			print(e)

	def create_hash (key):
		reply = key + GUID
		sh1 = hashlib.sha1(reply)
		return sh1.digest()

	def parse_headers (data):
		headers = {}
		lines = data.splitlines()
		for l in lines:
			parts = l.split(": ", 1)
			if len(parts) == 2:
				headers[parts[0]] = parts[1]
		headers['code'] = lines[len(lines) - 1]
		return headers


	def httpGetHandshake(conn):
		#stackoverflow.com/questions/10114224/how-to-properly-send-http-response-with-python-using-socket-library-only
		#https://gist.github.com/geoffb/616117
		print('Handshaking...')
		data = conn.recv(1024)
		headers = parse_headers(data)
		digest = create_hash(
			headers['Sec-WebSocket-Key']

		)
		encoded_data = base64.b64encode(digest)
		shake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
		shake += "Upgrade: WebSocket\r\n" 
		shake += "Connection: Upgrade\r\n"
		shake += "Sec-WebSocket-Origin: %s\r\n" % (headers['Origin'])
		shake += "Sec-WebSocket-Location: ws://%s\r\n" % (headers['Host'])
		shake += "Sec-WebSocket-Accept: %s\r\n\r\n" %encoded_data
		conn.send(shake)
		print("handshake succesfull")


	def handle(conn, addr):
		conn.settimeout(20)
		httpGetHandshake(conn)
		
		#lock = threading.Lock()
		try:
			data = readData(conn)
			data =json.loads(data)
			print "DATA=", data
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(("127.0.0.1", 5005))
			curr_offer=0
			max_offer =500
			alertAdaServer(data,s)
			while curr_offer<max_offer:

				reply = getOffer(s)
				print "From ada server= ",
				print reply
				reply = json.loads(reply)
				max_offer = reply["count"]
				reply.pop("count")
				curr_offer += len(reply)
				if len(reply)>0:
					print "delivering"
					deliverToClient(reply,conn)
			print "finished transaction, qutting"
			s.close()
			conn.close()
				
		
		except Exception, e:
			print e
			


	def start_server():
		s=socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		s.bind(('',8899))
		s.listen(10)
		print("listening on 8899")
		while 1:
			conn, addr=s.accept()
			print('Connection from:', addr)
			clients.append(conn)
			threading.Thread(target=handle, args=[conn,addr]).start()
	start_server()

if __name__ == "__main__":
    adaWebServer()




