from socket import *
import sys
import pickle

# 0 = ace, 1 = two, 2 = three, ... , 10 = jack, 11 = queen, 12 = king
# 0 = spades, 1 = clubs, 2 = diamonds, 3 = hearts
# 0 = not seen, 1 = seen
# Example card: 0 2 1 == "ace of diamonds - seen"

import random # needed for shuffle

def shuffleCards():
    deck = []
    for card in range(0,13):
        for suit in range(0,4):
            temp = str(card) + " " + str(suit) + " 0"
            deck.append(temp)
    random.shuffle(deck) 
    return deck

def dealHand(deck):
    hand = []
    for index in range(0,6): 
        hand.append(deck.pop(0))
    return hand

def calculateScore(allCards): 
    hand = []
    for card in allCards:
        list = card.split()
        hand.append(int(list[0]))

    score = [-3,-3,-3,-3,-3,-3]
    for card in range(0,6): 
        if hand[card] == 1: # 2s count as -2
            score[card] = -2
        elif hand[card] == 12: # kings count as 0
            score[card] = 0

    for card in range(0,3): # no points for duplicates in columns
        if hand[card] == hand[card+3]:
            score[card] = 0
            score[card+3] = 0

    for card in range(0,6): # everything else counts as its value...
        if score[card] == -3:
            if hand[card] > 9: # ...except for jacks and queens which still just count as 10
                score[card] = 10
            else:
                score[card] = hand[card] + 1 # +1 because aces start at 0
    returnScore = 0
    for index in range(0,6):
        returnScore += score[index]
    return returnScore

def getCardString(cardList):
    card = cardList.split()
    if int(card[2]) == 0:
        return "**"
        
    output = ""
    if int(card[0]) == 0:
        output += "A"
    elif int(card[0]) == 10:
        output += "J"
    elif int(card[0]) == 11:
        output += "Q"
    elif int(card[0]) == 12:
        output += "K"
    else:
        output += str(int(card[0])+1)
    
    if int(card[1]) == 0:
        output += "S"
    elif int(card[1]) == 1:
        output += "C"
    elif int(card[1]) == 2:
        output += "D"
    elif int(card[1]) == 3:
        output += "H"
    
    return output

def printHand(allCards):
    cardList = []
    for card in allCards:
        cardList.append(card)

    fullOutput = ""
    for index in range(0,6):
        if index == 3: 
            fullOutput += "\n"
        fullOutput += getCardString(cardList[index]) + "\t"
    print(fullOutput)

def flipCard(card):
    temp = card.split()
    output = str(temp[0]) + " " + str(temp[1]) + " " + "1"
    return output

def flipAll(hand):
    for index in range(0,6):
        hand[index] = flipCard(hand[index])
    return hand

deck = shuffleCards()
hand1 = dealHand(deck)

discardPile = []
discardPile.insert(0, flipCard(deck.pop(0))) # discard pile = top of deck, flipped over


clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Input client process name: ')

clientSocket.sendto(message.encode(),(sys.argv[1], int(sys.argv[2])))

PlayerList = {}



command = ''



while(command != 'o'):
    
    command = input("Please enter a command, 0 to Query Players, 1 to Query Games, 2 to start game, 3 to end your game, 4 to de-register, 9 to join a game : ")
    
    
    if(command == '2'):
        clientSocket.sendto(command.encode(), (sys.argv[1], int(sys.argv[2])))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print('Just send command 2, just recieved from server: ', modifiedMessage.decode())
        inputs = input('Please enter the number of players you want to create a game with')
        command = '23 '+inputs
        clientSocket.sendto(command.encode(), (sys.argv[1], int(sys.argv[2])))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print('Just send ', command, 'to server for number of players code, recieved : ', modifiedMessage.decode())
        ipaddresses = modifiedMessage.decode().split(':')
        print(ipaddresses)
        for x in ipaddresses:
            if (x == ''):
                break
            temp = x.split('!')
            PlayerList[temp[0]] = temp[1]
        print(PlayerList)
        
        conscript = '9'
        for x in PlayerList:
            hand = dealHand(deck)
            data = pickle.dumps(hand)
            print(x)
            print(PlayerList[x])
            print(hand)
            clientSocket.sendto(data, (x, int(PlayerList[x])))
            clientSocket.sendto('99'.encode(), (x, int(PlayerList[x])))
            handc= flipCard(deck.pop())
            hand = pickle.dumps(handc)
            clientSocket.sendto(hand, (x, int(PlayerList[x])))
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        
    if(command =='1'):
        clientSocket.sendto(command.encode(), (sys.argv[1], int(sys.argv[2])))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        splitm = modifiedMessage.decode()
        print(modifiedMessage.decode())
    if(command =='0'):
        clientSocket.sendto(command.encode(), (sys.argv[1], int(sys.argv[2])))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        splitm = modifiedMessage.decode()
        print(modifiedMessage.decode())
    if (command == '9'):
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        handplayer = pickle.loads(modifiedMessage)
        printHand(handplayer)
        print(calculateScore(handplayer))
        printHand(flipAll(handplayer))
        break
    if(command == '4'):
        clientSocket.sendto(command.encode(), (sys.argv[1], int(sys.argv[2])))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        if(modifiedMessage.decode()== '40'):
            print('Successfully De-registered yourself!')
            exit(0)
        else:
            print('Oh no! you are currently in a game and cannot de-register!')
    if(command == '3'):
        clientSocket.sendto(command.encode(), (sys.argv[1], int(sys.argv[2])))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        if(modifiedMessage.decode() == '30'):
            print('Successfully ended game!')
        else:
            print('Sorry, no game found!')
        
        
while True:
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage)
    if(modifiedMessage.decode() == '99'):
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        card = pickle.loads(modifiedMessage)
        print('Card on discard pile is: ', getCardString(card))
        choice = input('Press 1 to draw from the stock, press 2 to use the discard pile')
        if(choice == '1'):
            deck = shuffleCards()
            tempcard = getCardString(deck.pop())
            print('You drew a: ' , tempcard)
            choice = input('Press 1 - 6 to swap a card in your hand for this card, press 7 to discord')
            if(choice == '7'):
                print('Discarded Card')
                clientSocket.sendto('Discarded Card'.encode(), serverAddress)
            else:
                print('Card Swapped!')
                clientSocket.sendto('Swapped and discarded'.encode(), serverAddress)
        else:
            choice = input('Press 1 - 6 to swap a card in your hand for this card, press 7 to discord')
            if(choice == '7'):
                print('Discarded Card')
                clientSocket.sendto('Discarded Card'.encode(), serverAddress)
            else:
                print('Card Swapped!')
                clientSocket.sendto('Swapped and discarded'.encode(), serverAddress)
    
clientSocket.close()



    