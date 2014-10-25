#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

SERVER_PORT = int(sys.argv[1])
dic_user = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    """
    Borrar busca todos los usuarios con Expires = 0 y los apunta
    en una lista. Despues, se recorre esa lista y los borra a todos
    """

    def borrar(self):
        lista_borrar = []
        for usuario in dic_user:
            print "Tiempo de entrada del usuario: ", dic_user[usuario][-1]
            if time.time() >= float(dic_user[usuario][-1])  + float(dic_user[usuario][-2]):

                lista_borrar.append(usuario)

                print "==================================="
                print "Comprobando estado de Expires......" 
                print "==================================="

        print "LISTA DE USUARIOS A BORRAR ====> ", lista_borrar

        for a_borrar in lista_borrar:
            print "A BORRAR!!! => ", a_borrar
            del dic_user[a_borrar]
            print "Borrando a: " + a_borrar




    def register2file(self):
        fich = open("registered.txt", "w")
        fich.write("User\tIP\tExpires\n")

        for usuario in dic_user:
            salida = usuario + "\t"
            for elementos in dic_user[usuario]:
                    salida = salida + "\t" + str(elementos) + "\t"
            salida = salida + "\n"
            fich.write(salida)


        fich.close()

    def handle(self):
        address = self.client_address[0]
        print address
        port = self.client_address[1]
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print "Cliente con IP", str(address), "y puerto:", str(port)
        Contenido = list(self.client_address)

        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            else:
                print "Mensaje de entrada: " + line
                line = line.split()
                print line
                
                if line[0] == "REGISTER" and line[2] == "SIP/1.0":
                    reply = " SIP/1.0 200 OK\r\n\r\n"
                    self.wfile.write(reply)
                    if line[-1] == '0':
                        if dic_user.has_key(line[1]) == False:
                            self.wfile.write(reply)                            
                            print "Usuario con Expires = 0", dic_user
                        else:
                            del dic_user[line[1]]
                            self.wfile.write(reply)
                            print "Usuarios Registrados->", dic_user
                    else:
                        #Guardamos en un diccionario:
                        key = line[1]
                        value = [address, line[-1], time.time()]
                        dic_user[key] = value
                        #print dic_user[key][1]
                        print "\r\n"
                        print "LISTA DE USUARIOS ", dic_user

                        self.register2file()

                        self.borrar()
                else: 
                    print "PETICION INCORRECTA"
# ===================== PROGRAMA PRINCIPAL ==============================
if __name__ == "__main__":
    serv = SocketServer.UDPServer(("", SERVER_PORT), SIPRegisterHandler)
    print "========== Servidor conectado ==========="
    serv.serve_forever()
