#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor UDP con registro en fichero.
"""

import SocketServer
import sys
import time

SERVER_PORT = int(sys.argv[1])
dic_user = {}


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Clase que guarda en un fichero los usuarios registrados y comprueba
    si contiene alguno caducado (Expires = 0) y lo saca del registro.
    """
    def delete_expires(self):
        """
        Borrar busca todos los usuarios con Expires = 0 y los apunta
        en una lista. Despues, se recorre esa lista y los borra a todos.
        """
        lista_borrar = []
        for usuario in dic_user:
            if time.time() >= float(dic_user[usuario][-1]) + \
                    float(dic_user[usuario][-2]):
                lista_borrar.append(usuario)
        # Borra de la lista de "Expirados".
        for a_borrar in lista_borrar:
            del dic_user[a_borrar]
            print "- Borrando a: " + a_borrar

    def register2file(self):
        """
        Los elementos del diccionario son volcados a un fichero que
        contiene: Usuario - IP - Expires.
        """
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
        """
        Manejador que clasifica los mensajes de entrada en un
        diccionario por: Nombre  - IP - Puerto - Hora de entrada.
        """
        # Recoge el mensaje de entrada la IP y Puerto del cliente.
        address = self.client_address[0]
        port = self.client_address[1]
        # Escribe dirección y puerto del cliente.
        print "- Cliente con IP", str(address), "y puerto:", str(port)

        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente.
            line = self.rfile.read()
            if not line:
                break
            else:
                print "- Mensaje de entrada: " + line,
                line = line.split()
                line[1] = line[1].split(":")
                if line[0] == "REGISTER" and line[2] == "SIP/2.0":
                    reply = " SIP/2.0 200 OK\r\n\r\n"
                    self.wfile.write(reply)
                    # Si Expires es == 0:
                    if line[-1] == '0':
                        #self.wfile.write(reply)
                        if line[1][1] in dic_user:
                            self.wfile.write(reply)
                            del dic_user[line[1][1]]
                            print "Eliminando a: " + line[1][1]
                    else:
                        # Si Expires != 0 construimos el diccionario.
                        key = line[1][1]
                        value = [address, line[-1], time.time()]
                        dic_user[key] = value
                        print "LISTA DE USUARIOS: " + "\n", dic_user
                        print "------------------" + "\n"
                # Comprobamos que no hay usuarios con Expires = 0.
                self.delete_expires()
                # Registramos la entrada en el fichero.
                self.register2file()
#====================== PROGRAMA PRINCIPAL ==============================
if __name__ == "__main__":
    # Programa principal que lanza un servidor UDP hasta interrupcion.
    serv = SocketServer.UDPServer(("", SERVER_PORT), SIPRegisterHandler)
    print "========== Servidor conectado ==========="
    serv.serve_forever()
