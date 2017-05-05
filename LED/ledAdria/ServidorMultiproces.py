# -*- coding: utf-8 -*-
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
import BaseHTTPServer
import serial
import sys

PORT = "/dev/ttyACM0"
BR = 9600
serialport = serial.Serial(PORT, BR, timeout=0.5)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""
	Handler requests in a separate thread
	"""
	pass

class BondiaHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def _head_html(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _head_error_404(self):
        self.send_error(404, "Error")

    def _led_on(self):
        self._head_html()
        serialport.write("E\n")
        resposta = """<html>
        <head>
        <title>g7 | Led_on</title>
        </head>
        <body>
        <h1> Ets curios eh!, El led s'encendra aviat.</h1>
        </body>
        </html>
        """
        self.wfile.write(resposta)
    def _led_off(self):
        self._head_html()
        serialport.write("A\n")
        resposta = """<html>
        <head>
        <title>g7 | Led_off</title>
        </head>
        <body>
        <h1> Ets curios eh!, El led s'apagara aviat.</h1>
        </body>
        </html>
        """
        self.wfile.write(resposta)

    def _respon(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        serialport.write("S\n")
        s=serialport.read(10)
        self.wfile.write(s)


    def do_GET(self):
        path = self.path
        host = self.headers['Host']
        print "URL: {0} al servidor {1}".format(path,host)
        if path == "/led_on":
            self._led_on()
            print "ences"
	elif path == "/led_off":
	    self._led_off()
            print "apagat"
	elif path =="/estat":
            self._respon()
            print "estat"
        else:
            self._head_error_404()


PORT = 8000
Handler = BondiaHTTPRequestHandler

httpd = ThreadedHTTPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
