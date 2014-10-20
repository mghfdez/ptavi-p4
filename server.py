#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer

SERVER_PORT = 6001
### Hereda de otra clase que se encarga de llenar el buffer, etc...INFO II
class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print "Cliente con IP|Puerto: " + str(self.client_address)
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            ### rfile.read para leer ---- wfile.write para escribir
            line = self.rfile.read()
            if not line:
                break
            else:
                print "El cliente nos manda " + line
            ### self.wfile.write(line) CON ESTA LINEA SI ES UN SERVIDOR DE ECHO


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    ### Crea una instancia UPDServer. Si dejas "" es localhost y EchoHandler el manejador
    serv = SocketServer.UDPServer(("", SERVER_PORT), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    ### <<Quedate ahi por los tiempos de los tiempos escuchando>>
    serv.serve_forever()
