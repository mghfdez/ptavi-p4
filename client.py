#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

datos_user = sys.argv
if len(datos_user) != 6:
    print "Usage: client.py ip puerto register sip_address expires_value"
    raise SystemExit

SERVER = datos_user[1]    # Dirección IP del servidor.
PORT = int(datos_user[2])   # Puerto
METODO = datos_user[3]
addr = datos_user[4]   # Direccion SIP
EXPIRES = datos_user[5]   # Tiempo de expiración
VER = "SIP/2.0"   # Version de SIP

if METODO == 'register':
    metod = METODO.upper()
else:
    print "SIP/1.0 501 Not Implemented"
    raise SystemExit

# Contenido que vamos a enviar
LINE = metod + " sip:" + addr + " " + VER + "\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando petición SIP..."
LINE = LINE + "Expires: " + EXPIRES + "\r\n"
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
