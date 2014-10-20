#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

datos_user = sys.argv
if len(datos_user) < 3:
    print "Uso: $python client.py ip puerto linea-de-texto"
    raise SystemExit

# Dirección IP del servidor.
SERVER = datos_user[1]
PORT = int(datos_user[2])
METODO = datos_user[3]
if METODO == 'register':
    metod = "REGISTER"
else:
    metod = "unknown"
LINE = SERVER + " " + str(PORT) + " " + metod

# Contenido que vamos a enviar
addr = datos_user[4]
LINE = LINE + " " + "sip:" + addr
VER = "SIP/1.0"
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando petición SIP..."
LINE = LINE + " " + VER + "\r\n"
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
