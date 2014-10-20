#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer

SERVER_PORT = 6001
DIC_USER = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):
        address = self.client_address[0]
        port = self.client_address[1]
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print "Cliente con IP", str(address), "y puerto:", str(port)
        Contenido = list(self.client_address)
        #print Contenido

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
                
                if line[0] == "REGISTER":
                    reply = " SIP/1.0 200 OK\r\n\r\n"
                    self.wfile.write(reply)

                    if line[-1] <= '0':
                        if DIC_USER.has_key(address) == False:
                            reply = "SIP/1.0 200 OK\r\n\r\n"
                            self.wfile.write(reply)                            
                        else:
                            del DIC_USER[address]
                            reply = "SIP/1.0 200 OK\r\n\r\n"
                            self.wfile.write(reply)
                    else:
                        #Guardamos en un diccionario:
                        DIC_USER[address] = port
                        print "\r\n"
                        print "Usuarios Registrados: ", DIC_USER
                else: 
                    print "PETICION INCORRECTA"

# ===================== PROGRAMA PRINCIPAL ==============================
if __name__ == "__main__":
    serv = SocketServer.UDPServer(("", SERVER_PORT), SIPRegisterHandler)
    print "========== Servidor conectado ==========="
    serv.serve_forever()
