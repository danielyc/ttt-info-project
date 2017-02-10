from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import os
from time import sleep

os.system("clear")

player = " "

layout = [" ", " ", " ",
          " ", " ", " ",
          " ", " ", " "]

caddress = ('172.16.8.96', 6000)
raddress = ('172.16.8.96', 5000)
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
    if cconn.recv() == "InvalidMove":
        print("Invalid move")
    elif cconn.recv() == "Valid":
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
