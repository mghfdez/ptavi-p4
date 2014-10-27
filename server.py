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
FICH = open(FILE, 'w')
FICH.write("User \t IP \t Expires\r\n")
FICH.close()


def calc_sec(expire):
    seg = expire + time.time()
    return seg

def register2file(fichero, usuario, host, seg):
    #Apunta en un txt cada vez que un usuario se registra o se da de baja
    fich = open(fichero, 'a')
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(seg))
    texto = usuario + '\t' + host + '\t' + str_time + '\r\n'
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
                time_now = time.time()
                list_words = cadena.split()
                if list_words[0] == 'REGISTER':
                    correo = list_words[1]
                    exp_time = int(list_words[4])
                    exp_sec = calc_sec(exp_time)
                    dir_ip = self.client_address[0]
                    DICC_CLIENT[correo] = [dir_ip, exp_sec]
                    for user in DICC_CLIENT.keys():
                        if DICC_CLIENT[user][1] < time_now: 
                            del DICC_CLIENT[user]
                            print "Cliente borrado por plazo expirado"
                            
                    register2file(FILE, correo, dir_ip, exp_sec)
                    print "Cliente añadido - " + list_words[1]                    
                    print "Tiempo de expiración: " + str(exp_time)
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    if exp_time == 0:
                        register2file(FILE, correo, dir_ip, exp_sec)
                        del DICC_CLIENT[correo]
                        print "Borrado " + correo + '\n'
                        self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                else:
                    self.wfile.write("SIP/2.0 400 BAD REQUEST\r\n\r\n")
            else:
                break
     
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("",  PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
