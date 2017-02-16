from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from ipaddress import ip_address
import os
from time import sleep
import sys
import socket


def clearS():
    if sys.platform.startswith("Linux"):
        os.system("clear")
    elif sys.platform.startswith("Win32"):
        os.system("cls")

Lport = 5000
Cport = 80

player = " "

layout = [" ", " ", " ",
          " ", " ", " ",
          " ", " ", " "]

raddress = ""
caddress = ""


def error(msg, ext=False):
    if ext:
        print("[ERROR] " + msg)
        exit()
    else:
        print("[ERROR] " + msg)


def setIp():
    global raddress
    if socket.gethostbyname(socket.gethostname()) == '127.0.1.1':
        error("not able to get correct Local IP")
        inp = input("Enter IP manually: ")
        if len(inp) == 0:
            error("no IP provided", True)
        try:
            if ip_address(inp):
                raddress = (str(inp), Lport)
        except ValueError:
            error("Invalid ip", True)
    else:
        inp = input("Is '" + socket.gethostbyname(socket.gethostname()) + "' The correct IP? (y/n)")
        if inp.upper() == "Y":
            raddress = (socket.gethostbyname(socket.gethostname()), Lport)
        elif inp.upper() == "N":
            inp = input("Enter IP manually: ")
            if len(inp) == 0:
                error("no IP provided", True)
            try:
                if ip_address(inp):
                    raddress = (str(inp), Lport)
            except ValueError:
                error("Invalid ip", True)
        else:
            error("Not a valid input", True)

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
    global caddress
    name = input("Name: ")
    inp = input("Enter IP of the Game: ")
    if len(inp) == 0:
        error("IP empty", True)
    else:
        try:
            if ip_address(inp):
                print("Connecting to " + str(inp) + " on port " + str(Cport))
                caddress = (str(inp), Cport)
        except ValueError:
            error("Invalid IP", True)
    try:
        cconn = Client(caddress, authkey=b'tttinfo')
        cconn.send(name)

        player = cconn.recv()
        cconn.close()
    except ConnectionRefusedError:
        error("Game not functioning or listening", True)
    print("You are player: " + player)

    if player == "O":
        print("waiting for board")


def timeout(time):
    sleep(time)
    return True


def sendMove():
    pos = input("Position: ")
    cconn = Client(caddress, authkey=b'tttinfo')
    cconn.send([int(pos), player])
    if cconn.recv() == "InvalidMove":

        error("Invalid move", True)
    elif cconn.recv() == "Valid":
        cconn.close()


def receiveBoard():
    global layout

    rconn = listen.accept()
    layout = rconn.recv()
    rconn.close()
    printBoard()


def main():
    setIp()
    startGame()
    receiveBoard()
    sendMove()


if __name__ == "__main__":
    main()
