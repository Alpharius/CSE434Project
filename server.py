from socket import *
import sys
    
     
ports = []
i= len(sys.argv)-1
print(i)
for x in sys.argv:
    print(sys.argv[1])
j = 0
while(i >= 1):
    ports.append(sys.argv[i])
    print('added: ', sys.argv[i], " to ports")
    i = i-1
    


serverPort = 31510
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((ports[1], int(ports[0])))
print("The server is ready to receive")
serverName = '10.1.48.73'
PlayerList = {}
#recieveCommand(serverName, serverPort)
while True:
 message, clientAddress = serverSocket.recvfrom(2048)
 modifiedMessage = message.decode()
 serverSocket.sendto(modifiedMessage.encode(), clientAddress)
 if clientAddress not in PlayerList.keys():
     PlayerList[clientAddress] = message.decode()
     print('Added: ', PlayerList[clientAddress], " to the database")
 print(PlayerList[clientAddress])
 if (modifiedMessage == 'P') or (modifiedMessage == 'p'):
     print("Recieved Query Players Command")
     list = 'Players currently Registered Are: '
     for x in PlayerList:
         list = list + str(PlayerList[x])+' : '+str(x)+ '\n'
     print(list)
     modifiedMessage = list
     serverSocket.sendto(modifiedMessage.encode(), clientAddress)
     print("sent: ", modifiedMessage.encode().decode())
 if (modifiedMessage == 'Q') or (modifiedMessage == 'q'):
     print("Recieved Query Games Command")
     answer = 'Games currently running are: '
     serverSocket.sendto(answer.encode(), clientAddress)
     
     
 
 