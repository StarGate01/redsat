from sys import argv
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

class FakeServer(BaseHTTPRequestHandler):
    def _set_response(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request, Path: %s\n", str(self.path))
        
        code = 404
        reponse = '{}'
        if self.path == "/session":
        	code = 200
        	response = '{"session":"15700771d1262b8e"}'
        
        self._set_response(code=code)
        self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        logging.info("POST request, Path: %s\nBody:\n%s\n",
                str(self.path), post_data.decode('utf-8'))

        code = 404
        response = '{}'

        if self.path == '/nanolink':
        	data = json.loads(post_data.decode('utf-8'))
        	logging.info("DATA: " + data['nanolink_frame'])
        	global frames
        	frames.write(data['nanolink_frame'] + '\n')
        	frames.flush()
        	code = 200

        self._set_response(code=code)
        self.wfile.write(response.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=FakeServer, port=8000):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
	file = 'frames.txt'
	if len(argv) > 1:
		file = argv[1]

	with open(file, "a") as frames:
		frames.write('\n')
		run()