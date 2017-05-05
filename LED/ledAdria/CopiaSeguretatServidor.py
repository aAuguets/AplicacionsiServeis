# -*- coding: utf-8 -*-

import BaseHTTPServer
import serial
import sys

PORT = "/dev/ttyACM0"
BR = 9600
serialport = serial.Serial(PORT, BR, timeout=0.5)
estat=0
class BondiaHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def _head_html(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _head_error_404(self):
        self.send_error(404, "Error")

    def _led_on(self):
        global estat
        serialport.write("E\n")
        estat=1

    def _led_off(self):
	global estat
        serialport.write("A\n")
        estat=0

    def _respon(self):
        self._head_html()
        serialport.write("S\n")
        self.wfile.write(estat)

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

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
