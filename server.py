#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    diccio = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print self.client_address
        IP = self.client_address[0]
        PUERTO = self.client_address[1]
        self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda " + line
            lista = line.split()
            regis = lista[0]
            if regis == 'REGISTER':
                user = lista[1].split(':')[-1]
                self.diccio[str(user)] = IP
            if not line or '[""]':
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos

    serv = SocketServer.UDPServer((sys.argv[1], int(sys.argv[2])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
