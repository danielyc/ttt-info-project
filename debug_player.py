from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from ipaddress import ip_address
import os
import sys
import socket


def clearS():                                           #maakt het scherm schoon
    if sys.platform.startswith("Linux"):
        os.system("clear")
    elif sys.platform.startswith("Win32"):
        os.system("cls")

Lport = 5000
Cport = 6000

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


def setIp():                                            #regelt de ip confiuratie
    global raddress
    global listen
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


def startGame():                          #wat wordt uitgevoerd aan het begin van het programma, ip van de game en naam
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


def reset():
    global layout
    layout = [" ", " ", " ",
              " ", " ", " ",
              " ", " ", " "]


def gameEnded(msg):
    if msg == "winner: X":
        if player == "X":
            print("You won!!!")
        else:
            print("You lost")
    elif msg == "winner: O":
        if player == "O":
            print("You wonn!!!")
        else:
            print("You lost")
    elif msg == "draw":
        print("Draw")
    clearS()
    reset()


def sendMove():                            #stuurt de zet naar de game en ontvangt zet geldigheid
    pos = input("Position: ")
    cconn = Client(caddress, authkey=b'tttinfo')
    cconn.send([int(pos), player])
    msg = cconn.recv()
    if msg == "InvalidMove":
        cconn.close()
        error("Invalid move", True)
    elif msg == "Valid":
        cconn.close()


def receive():                       #ontvant het bord
    global layout

    rconn = listen.accept()
    msg = rconn.recv()
    if 'winner' in str(msg):
        gameEnded(msg)
        return False
    elif str(msg) == "draw":
        gameEnded(msg)
        return False
    elif str(msg) == "end":
        print("Game stopped. Exiting")
        exit()
    layout = msg
    rconn.close()
    printBoard()
    return True


def main():                               #volgorde van wat uitgevoerd wordt
    setIp()
    startGame()
    while receive():
        sendMove()


if __name__ == "__main__":                  # checkt of game als module wordt uitgevoerd
    try:                                    # onderbreekt programma zonder errors
        main()
    except KeyboardInterrupt:
        error("Exiting program", True)
else:
    error("Game should not be running as an api", True)