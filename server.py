#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#Practica 4 - Miguel Angel Fernandez Sanchez
"""
Clase (y programa principal) para un servidor SIP-registrar
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


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Clase Registrar-SIP
    """

    def clean_dic(self):
        """
        Limpia el diccionario de usuarios con plazo expirado
        """
        time_now = time.time()
        for user in DICC_CLIENT.keys():
            if DICC_CLIENT[user][1] < time_now:
                print "BORRADO cliente " + user + " (Plazo expirado)"
                del DICC_CLIENT[user]

    def register2file(self):
        """
        Imprime con formato "User \t IP \t Expires"
        el diccionario de clientes en un fichero.
        """
        fich = open('registered.txt', 'w')
        fich.write("User \t IP \t Expires\r\n")
        for user in DICC_CLIENT.keys():
            host = DICC_CLIENT[user][0]
            seg = DICC_CLIENT[user][1]
            str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(seg))
            texto = user + '\t' + host + '\t' + str_time + '\r\n'
            fich.write(texto)
        fich.close()

    def handle(self):
        """
        Maneja peticiones SIP del cliente: si la petición es correcta,
        guarda los datos (en un diccionario y en un fichero) y responde un
        mensaje de confirmación al cliente. Si no, envía un mensaje de error.
        """
        while 1:
            cadena = self.rfile.read()
            if cadena != "":
                list_words = cadena.split()
                if list_words[0] == 'REGISTER':
                    self.clean_dic()
                    correo = list_words[1]
                    correo = correo.split(":")[1]
                    try:
                        exp_time = int(list_words[4])
                    except ValueError:
                        self.wfile.write("SIP/2.0 400 BAD REQUEST\r\n\r\n")
                        break
                    exp_sec = exp_time + time.time()
                    dir_ip = self.client_address[0]
                    DICC_CLIENT[correo] = [dir_ip, exp_sec]
                    self.register2file()
                    print "AÑADIDO cliente " + correo
                    print "Expira en: " + str(exp_time) + " seg.\r\n"
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    if exp_time == 0:  # Damos de baja al cliente
                        print "DADO DE BAJA cliente " + correo + '\n'
                        del DICC_CLIENT[correo]
                        self.register2file()
                        self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                else:
                    self.clean_dic()
                    self.wfile.write("SIP/2.0 400 BAD REQUEST\r\n\r\n")
            else:
                break

if __name__ == "__main__":
    # Creamos servidor SIP y escuchamos
    serv = SocketServer.UDPServer(("",  PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de SIP...\r\n"
    serv.serve_forever()
