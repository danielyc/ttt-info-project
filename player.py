from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import os
os.system("clear")

player = " "
name = "daniel"

layout = [" ", " ", " ",
          " ", " ", " ",
          " ", " ", " "]

caddress = ('10.0.1.34', 6000)
raddress = ('10.0.1.34', 5000)
listen = Listener(raddress, authkey=b'tttinfo')


def startGame():
    global player

    cconn = Client(caddress, authkey=b'tttinfo')
    cconn.send(name)

    player = cconn.recv()
    cconn.close()
    print(player)


def sendMove(pos):
    cconn = Client(caddress, authkey=b'tttinfo')
    cconn.send([pos, player])
    cconn.close()


def receiveBoard():
    global layout

    rconn = listen.accept()
    layout = rconn.recv()
    rconn.close()
    print(layout)


def main():
    startGame()
    receiveBoard()


if __name__ == "__main__":
    main()
