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
    


serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((ports[1], int(ports[0])))
print("The server is ready to receive")
PlayerList = {}
Lobby = {}
GameList = {}
GameCount = 0
list = ''
#recieveCommand(serverName, serverPort)
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode()
    splitMessage = modifiedMessage.split()
    if clientAddress not in PlayerList.keys():
        PlayerList[clientAddress] = message.decode()
        print('Added: ', PlayerList[clientAddress], " to the database")
        print(PlayerList)
        Lobby[PlayerList[clientAddress]] = False
        print('Added: ', PlayerList[clientAddress], 'as: ', Lobby[PlayerList[clientAddress]])
    print(PlayerList[clientAddress])
    print('Recieved code: ', splitMessage[0])
    if(splitMessage[0] == '2'):
        print('Recieved Start Game Command')
        msg = "22"
        serverSocket.sendto(msg.encode(), clientAddress)
    if(splitMessage[0] == "23"):
        players = ''
        playerCount = splitMessage[1]
        foundPlayers = 0
        
        for i in range(int(playerCount)):
            for x in PlayerList:
                if Lobby[PlayerList[x]] == False and foundPlayers < int(playerCount):
                    GameList[str(PlayerList[x])] = str(x)
                    list = list + str(PlayerList[x][0])+ ' '+str(PlayerList[x][1])+':'
                    
                    players = players+str(x[0])+'!'+str(x[1])+':'
                    print('Playerlist[x]: is ' + str(PlayerList[x])+ 'x is: ' + str(x))
                    foundPlayers += 1
                    print('Added: ', str(PlayerList[x]), ':', str(x), 'to the list')
                    print('Player count: ', playerCount, 'Found players: ', foundPlayers)
                    Lobby[PlayerList[x]] = True
                    Lobby[PlayerList[clientAddress]] = True
        serverSocket.sendto(players.encode(), clientAddress)
        print(players)
        GameList[clientAddress] = PlayerList[clientAddress]
        GameCount += 1
    if (splitMessage[0] == '0'):
        print("Recieved Query Players Command")
        list = 'Players currently Registered Are: '
        for x in PlayerList:
            list = list + str(PlayerList[x])+' : '+str(x)+ '\n'
        print(list)
        modifiedMessage = list
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        print("sent: ", modifiedMessage.encode().decode())
    if (splitMessage[0] == '1'):
        print("Recieved Query Games Command")
        answer = str(GameCount)+':'+ str(GameList)
        serverSocket.sendto(answer.encode(), clientAddress)
    if(splitMessage[0] == '4'):
        if (Lobby[PlayerList[clientAddress]] == True):
            modifiedMessage = '41'
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        else:
            modifiedMessage = '40'
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            Lobby.pop(PlayerList[clientAddress])
            PlayerList.pop(clientAddress)
    if(splitMessage[0] == '3'):
        if(GameList.__contains__(clientAddress) == True):
            modifiedMessage = '30'
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        else:
            modifiedMessage = '31'
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
     
     
     
    