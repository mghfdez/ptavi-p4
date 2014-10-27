#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente de UDP sencillo que abre un socket a un servidor
"""

import socket
import sys


# CAMPOS => ip | puerto | register | luke@polismassa.com
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    PETICIONES = sys.argv[3]
    DIRECCION_SIP = sys.argv[4]
    EXPIRES = sys.argv[5]
except IndexError:
    print "Usage: client.py ip puerto register sip_address expires_value"
# Concatenamos un conjunto de dos elementos. Es lo que manda el cliente
LINE = PETICIONES.upper() + " " + "sip:" + DIRECCION_SIP + " SIP/2.0\r\n"
LINE = LINE + "Expires: " + EXPIRES + "\r\n\r\n"
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print ""
print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."
# Cerramos todo
my_socket.close()
print "Fin."
