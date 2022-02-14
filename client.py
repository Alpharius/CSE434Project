from socket import *
import sys
serverName = '10.1.48.73'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input client process name: ')
clientSocket.sendto(message.encode(),(sys.argv[1], int(sys.argv[2])))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
command = ''
while(command != 'o'):
    command = input("Please enter a command, P to query players, Q to query games: ")
    clientSocket.sendto(command.encode(), (sys.argv[1], int(sys.argv[2])))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
clientSocket.close()

    