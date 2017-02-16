import socket
import time

cevap = []
cevap1 = '{"count":"6"}'
cevap2='{"count":"6","anadolu":"50","ege":"70"}'
cevap3='{"count":"6","axa":"89","boma":"34","lala":"42"}'
cevap4='{"count":"6","final":"84"}'

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data: break
	print "received data:", data
	time.sleep(1)
	conn.send(cevap1)
	time.sleep(3)
	conn.send(cevap2)
	time.sleep(4)
	conn.send(cevap3)
	time.sleep(5)
	conn.send(cevap4)

conn.close()