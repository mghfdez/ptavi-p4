#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# ip | puerto | register | luke@polismassa.com
try:
	SERVER = sys.argv[1]
	PORT = int(sys.argv[2])
	PETICIONES = sys.argv[3] 
	DIRECCION_SIP = sys.argv[4]
	EXPIRES = sys.argv[5]
except IndexError:
	print "Usage: client.py ip puerto register sip_address expires_value"
# Lo que manda el cliente es un conjunto de dos elementos, lo creamos concatenando:
LINE = PETICIONES.upper() + " " + "sip:" + DIRECCION_SIP + " SIP/1.0\r\n"
LINE = LINE + "Expires: " + EXPIRES + "\r\n\r\n"
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Lista que no puedes modificar.
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
### \r\n por convencion, retorno de carro - nueva linea.
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024) #1024 => Tamaño del buffer.

print 'Recibido -- ', data
print "Terminando socket..."
# Cerramos todo
my_socket.close()
print "Fin."
