import socket
from _thread import *
import pickle
from Tichugame import Game

server = "26.186.60.195"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Waiting for a connection...")

connected = set()
games = {}
gameReady = False
idCount = 0
gameId = 0
p = 0



def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        data = pickle.loads(conn.recv(2048*8*2))
        try:
            if gameId in games:
                game = games[gameId]
                #print(data)
                if not data:
                    break
                else:
                    if data == "Get Hand":
                        reply = game.hands[p]
                    elif data[0] == "Name":
                        game.playerNames[p] = data[1]
                    elif data == "Begin" and game.ready:
                        reply = "Start"
                    elif game.phase != "Receiving" and data == "Get Hands":
                        reply = [len(game.hands[0]), len(game.hands[1]), len(game.hands[2]), len(game.hands[3])]
                    elif game.phase == "Receiving" and data == "Get Hands":
                        reply = []
                        for i in range(4):
                            if game.readyToPlay[i]:
                                reply.append(len(game.hands[i]))
                            else:
                                reply.append(len(game.hands[i]) - 3)
                    elif data == "Get Phase":
                        reply = game.phase
                    elif game.phase == "Giving" and data == "Not Ready To Send":
                        game.pReady[p] = False
                    elif game.phase == "Giving" and data == "Ready To Send":
                        game.pReady[p] = True
                        if game.pReady[0] and game.pReady[1] and game.pReady[2] and game.pReady[3]:
                            reply = "Get Cards"
                    elif game.phase == "Giving" and data[0] == "Sent Cards" and p not in game.cardsToGive:
                        game.cardsToGive[p] = data[1]
                    elif game.phase == "Giving" and data == "Server Receive Status":
                        if len(game.cardsToGive) == 4:
                            reply = "Server Ready"
                    elif game.phase == "Giving" and data == "Give Cards":
                        game.play(p)
                    elif game.phase == "Giving" and data == "Ready To Receive":
                        if game.cardsGiven[0] and game.cardsGiven[1] and game.cardsGiven[2] and game.cardsGiven[3]:
                            reply = ([game.cardsToReceive[p], game.hands[p], "Cards Sent"])
                    elif game.phase == "Receiving" and data == "Ready To Play":
                        game.readyToPlay[p] = True
                        if game.readyToPlay[0] and game.readyToPlay[1] and game.readyToPlay[2] and game.readyToPlay[3]:
                            game.phase = "Playing"
                            game.play(p)
                    elif game.phase == "Giving" and data == "Cards Received":
                        game.cardsReceived[p] = True
                        if game.cardsReceived[0] and game.cardsReceived[1] and game.cardsReceived[2] and game.cardsReceived[3]:
                            game.phase = "Receiving"
                    elif game.phase == "Playing" and data == "Turn":
                        if game.pTurn == p:
                            reply = True
                        else:
                            reply = False
                    else:
                        reply = "Waiting"
                    #print(reply)
                    if data[0] == "Select":
                        for card in game.hands[p]:
                            if card.id == data[1]:
                                card.selected = True
                        reply = game.hands[p]
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    print("Lost connection")
    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connection address:", addr)
    if idCount % 4 == 0:
        gameId = idCount//4
    idCount += 1
    if idCount % 4 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    if p == 0:
        for hand in games[gameId].shuffle(games[gameId].deck):
            games[gameId].hands.append(hand)
    elif p == 3: #Na kanw 3
        games[gameId].ready = True
    start_new_thread(threaded_client, (conn, p, gameId))
    if p == 3:
        p = 0
    else:
        p+=1
