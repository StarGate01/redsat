import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 8000
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

with open("/app/fakeserver/response.html") as f:
	html = f.read()

while 1: 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	print 'MOVE2-Fakeserver: Connection: ' + addr

	try:
		while 1:
			conn.send(html)
			data = conn.recv(BUFFER_SIZE)
			if not data: break
			else: print "MOVE2-Fakeserver: Data: " + data
	except:
		pass

	conn.close()