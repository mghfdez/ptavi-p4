#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
sys.argv

# Cliente UDP simple.
if len(sys.argv) != 6:
    print "Usage: client.py ip puerto register sip_address expires_value"
    raise SystemExit

# Dirección IP del servidor.
SERVER = sys.argv[1]
# Por si el usuario introduce un valor no-numérico en "PORT"
try:
    PORT = int(sys.argv[2])
except ValueError:
    print "Usage: client.py ip puerto register sip_address expires_value"
    raise SystemExit

# Contenido que vamos a enviar
REGISTER = sys.argv[3]
DIRECTION = sys.argv[4]
TIEMPO = sys.argv[5]

LINE = 'REGISTER sip:' + DIRECTION + ' SIP/2.0\r\n'
LINE1 = 'Expires: ' + TIEMPO + '\r\n\r\n'
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))
print "Enviando: " + LINE
my_socket.send(LINE + '\r\n' + LINE1 + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
