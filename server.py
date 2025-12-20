import socket
from _thread import *
import pickle
from Tichugame import Game

server = "192.168.1.176"
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
        data = pickle.loads(conn.recv(2048*8))
        try:
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "Get Hand":
                        reply = game.hands[p]
                    elif data == "Begin" and game.ready:
                        reply = "Start"
                    elif data == "Get Hands":
                        reply = [len(game.hands[0]), len(game.hands[1]), len(game.hands[2]), len(game.hands[3])]

                    else:
                        reply = "Waiting"

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
        gameId = idCount/4
    idCount += 1
    if idCount % 4 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    if p == 0:
        for hand in games[gameId].shuffle(games[gameId].deck):
            print(hand)
            games[gameId].hands.append(hand)
    elif p == 1: #Na kanw 3
        games[gameId].ready = True
    start_new_thread(threaded_client, (conn, p, gameId))
    if p == 3:
        p = 0
    else:
        p+=1