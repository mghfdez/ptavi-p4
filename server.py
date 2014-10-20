#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

if len(sys.argv) != 2:
    print "Uso: $python server.py puerto"
    raise SystemExit

PORT = int(sys.argv[1])
DICC_CLIENT = {}
class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):    
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
        while 1:
            line = self.rfile.read()
            if line != "":
                datos = line.split()
                DICC_CLIENT[datos[3]] = self.client_address
            else: 
                break


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("",  PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
