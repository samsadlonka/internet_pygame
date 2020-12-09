import socket
from _thread import *
import sys
from player import Player
import pickle
from game_rock_paper_scissors import Game

server = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print('Waiting for connection, Server Started')

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    replay = ''
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset_went()

                    elif data != 'get':
                        game.play(p, data)

                    replay = game
                    conn.sendall(pickle.dumps(replay))
            else:
                break
        except:
            break

    print('Lost Connection')

    try:
        del games[gameId]
        print('Closing Game', gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print('Connected to:', addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print('Creating a new game...')
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))