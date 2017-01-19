from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import os
from time import sleep

os.system("clear")

player = " "

layout = [" ", " ", " ",
          " ", " ", " ",
          " ", " ", " "]

caddress = ('10.0.1.34', 6000)
raddress = ('10.0.1.34', 5000)
listen = Listener(raddress, authkey=b'tttinfo')

def printBoard():
    print("-------------------------")
    print("|   " + layout[0] + "   |   " + layout[1] + "   |   " + layout[2] + "   |")
    print("-------------------------")
    print("|   " + layout[3] + "   |   " + layout[4] + "   |   " + layout[5] + "   |")
    print("-------------------------")
    print("|   " + layout[6] + "   |   " + layout[7] + "   |   " + layout[8] + "   |")
    print("-------------------------")

def startGame():
    global player
    name = input("Name: ")


    cconn = Client(caddress, authkey=b'tttinfo')
    cconn.send(name)

    player = cconn.recv()
    cconn.close()
    print("You are player: " + player)

    if player == "O":
        print("waiting for board")


def timeout(time):
    sleep(time)
    return True


def sendMove():
    pos = input("Position: ")
    cconn = Client(caddress, authkey=b'tttinfo')
    cconn.send([int(pos),player])
    try:
        if not timeout(0.2) or cconn.recv():
            if cconn.recv() == "InvalidMove":
               print("Invalid move")
    except:
        pass
    cconn.close()


def receiveBoard():
    global layout

    rconn = listen.accept()
    layout = rconn.recv()
    rconn.close()
    printBoard()


def main():
    startGame()
    receiveBoard()
    sendMove()


if __name__ == "__main__":
    main()
