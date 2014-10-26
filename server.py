#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    diccio = {}

    def handle(self):
        hactual = time.time()
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
            texpires = lista[4]
            if regis == 'REGISTER':
                user = lista[1].split(':')[-1]

                if int(texpires) == 0:
                    #miro si hay usuarios en el dicc
                    encontrado = self.diccio.in(user)
                    if encontrado == 1:
                        #borro al usuario del dicc
                        del self.diccio[user]
                        self.register2file()
                else:
                    self.diccio[str(user)] = IP + ',' + \
                        str(float(texpires) + hactual)
                    self.register2file()

            if not line or '[""]':
                break
        """
        Caducidad de los usuarios registrados
        """
        for Usuario, Val in self.diccio.items():
            Texp = Val.split(',')[-1]
            if hactual > float(Texp):  # si se caduca borro el usuario
                del self.diccio[Usuario]
                self.register2file()

        """
        Manipulacion de fichero
        """

    def register2file(self):
        dic = self.diccio
        fichero = open("registered.txt", "w")
        fichero.write('User' + '\t' + 'IP' + '\t' + 'Expires' + '\n')
        for Usuario, Valor in dic.items():
            hora = Valor.split(',')[-1]  # me quedo con lo que esta despues de,
            ip = Valor.split(',')[0]
            # me devuelve un strig de texpires+hactual
            tactual = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.gmtime(float(hora)))
            #voy escribiendo en el fichero la inf de los usuarios
            fichero.write(Usuario + '\t' + ip + '\t' + tactual + '\n')


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer((sys.argv[1], int(sys.argv[2])),
                                  SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
