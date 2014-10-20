#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Toma por la linea de comandos IP y Puerto donde esta el servidor
SERVER = sys.argv[1]
print SERVER
#'localhost' # 127.0.0.1 
PORT = int(sys.argv[2])
print PORT
#6001
# Contenido que vamos a enviar tomado por la linea de comandos tambien.
LINE = sys.argv[3]
print LINE
#'¡Hola mundo!'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
### -----------------------------------
### Crea un objeto tipo socket  y le pasamos 2 parametros 
### El primero un socket de internet y el segundo uno de datagramas (para UDP)
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
### Permite añadir mas opciones. Cuando se cierra el socket el OS cierra el puerto
### inmediatamente y lo libera. El socket involucra 2 puertos, el mio y el del server (6001)
### y el nuestro que lo abrimos nosotros. Con la linea le decimos: cuando cierres el socket
### libera el puerto. 
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Lista que no puedes modifica.
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
