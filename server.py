#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

if len(sys.argv) != 2:
    print "Usage: $python server.py puerto"
    raise SystemExit

PORT = int(sys.argv[1])
DICC_CLIENT = {}
FILE = 'registered.txt'


def register2file(fichero, dicc):
    """
    Imprime ordenadamente un diccionario en un fichero
    """
    fich = open(fichero, 'w')
    fich.write("User \t IP \t Expires\r\n")
    for user in dicc.keys():
        host = dicc[user][0]
        seg = dicc[user][1]
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(seg))
        texto = user + '\t' + host + '\t' + str_time + '\r\n'
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
                time_now = time.time()
                for user in DICC_CLIENT.keys():  # Limpia el diccionario
                    if DICC_CLIENT[user][1] < time_now:
                        del DICC_CLIENT[user]
                        print "Cliente borrado por plazo expirado"
                correo = list_words[1]
                correo = correo.split(":")[1]
                exp_time = int(list_words[4])
                exp_sec = exp_time + time.time()
                dir_ip = self.client_address[0]
                DICC_CLIENT[correo] = [dir_ip, exp_sec]
                register2file(FILE, DICC_CLIENT)
                print "Cliente añadido - " + correo
                print "Expira en: " + str(exp_time) + " seg.\r\n"
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                if exp_time == 0:
                    del DICC_CLIENT[correo]
                    register2file(FILE, DICC_CLIENT)
                    print "Borrado " + correo + '\n'
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            else:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("",  PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
