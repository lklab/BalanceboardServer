#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM

serverSocket = socket(AF_INET, SOCK_STREAM)
clientSocket = None

ip = '0.0.0.0'
port = 3000

serverSocket.bind((ip, port))

serverSocket.listen(5)

try :
	while(True) :
		clientSocket, addr = serverSocket.accept()

		print("connected client from " + str(addr))

		message = clientSocket.recv(1024)
		if(len(message) == 5) :
			print("command: " + str(message[0]))
			print("start: " + str(message[1]))
			print("target: " + str(message[2]))
			print("exec: " + str(message[3]))
			print("level: " + str(message[4]))

		clientSocket.close()
		clientSocket = None

except KeyboardInterrupt :
	if(clientSocket is not None) :
		clientSocket.close()
	serverSocket.close()
	print("server is terminated.")

