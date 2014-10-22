#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

if len(sys.argv) != 2:
    print "Usage: $python server.py puerto"
    raise SystemExit

PORT = int(sys.argv[1])
DICC_CLIENT = {}
FILE = 'registered.txt'
FICH = open(FILE, 'w')
FICH.write("User \t IP \t Expires\r\n")
FICH.close()

def register2file(fichero, modo, usuario, host):
    #Apunta en un txt cada vez que un usuario se registra o se da de baja
    fich = open(fichero, 'a')
    texto = usuario + '\t' + host + '\t' + "--fecha // hora-- " + modo + "\r\n"
    fich.write(texto)
    fich.close()

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):    
        # Escribe dirección y puerto del cliente (de tupla client_address)
        
        while 1:
            cadena = self.rfile.read()
            if cadena != "":
                list_words = cadena.split()
                if list_words[0] == 'REGISTER':
                    correo = list_words[1]
                    DICC_CLIENT[correo] = self.client_address
                    register2file(FILE, "Añadido", correo, self.client_address[0])
                    print "Cliente añadido - " + list_words[1]
                    if list_words[3] == 'Expires:':
                        exp_time = int(list_words[4])
                        print "Tiempo de expiración: " + str(exp_time)
                        if exp_time == 0:
                            register2file(FILE, "Borrado", correo, self.client_address[0])
                            del DICC_CLIENT[correo]
                            print "Borrado " + correo
                        print "\n", 
                        print DICC_CLIENT
                        self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    else:
                        self.wfile.write("SIP/2.0 400 BAD REQUEST -- != expires\r\n\r\n")
                else:
                    self.wfile.write("SIP/2.0 400 BAD REQUEST -- != register\r\n\r\n")
            else:
                break
     
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("",  PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
