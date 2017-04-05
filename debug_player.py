from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from time import sleep
import os
import sys
import socket
import random


def clearS():                                           # maakt het scherm schoon
    if sys.platform.startswith("Linux"):
        os.system("clear")
    elif sys.platform.startswith("Win32"):
        os.system("cls")

Lport = 5000
Cport = 6000
local = False

player = " "
IP = " "

layout = [" ", " ", " ",
          " ", " ", " ",
          " ", " ", " "]

raddress = ""
caddress = ""


def error(msg, ext=False):                              # error afdrukken
    if ext:
        print("[ERROR] " + msg)
        exit()                                          # stop game
    else:
        print("[ERROR] " + msg)


def pcConfig():                                         # vraag of de game lokaal of via netwerk wordt gespeeld
    global local
    global Lport
    inp = input("Do you want to play on one PC? (y/n): ")
    if inp.upper() == "Y":
        local = True
        Lport = random.randint(5000, 5999)
        print("Listen port is: " + str(Lport))
    elif inp.upper() == "N":
        local = False
    else:
        error("Invalid input", True)


def setIp():                                            # regelt de ip confiuratie
    global raddress
    global listen
    global IP
    IP = socket.gethostbyname(socket.gethostname())
    if IP == '127.0.1.1':
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
        inp = input("Is '" + IP + "' The correct IP? (y/n): ")
        if inp.upper() == "Y":
            raddress = (IP, Lport)
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


def startGame():                          # wat wordt uitgevoerd aan het begin van het programma, ip van de game en naam
    global player
    global caddress
    global Lport
    name = input("Name: ")
    if not local:
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
            conn = Client(caddress, authkey=b'tttinfo')
            conn.send(name)
            player = conn.recv()
            conn.close()
        except ConnectionRefusedError:
            error("Game not functioning or listening", True)
    else:
        print("Using local IP")
        try:
            caddress = (IP, Cport)
            msg = ([name, str(Lport)])
            cconn = Client(caddress, authkey=b'tttinfo')
            cconn.send(msg)
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


def gameEnded(msg):                                              # wat wordt uitgevoerd als een game is afgelopen
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


def specialmsg(msg):                                            # hanteerd speciale berichten
    if 'winner' in str(msg):
        gameEnded(msg)
        return True
    elif str(msg) == "draw":
        gameEnded(msg)
        return True


def sendMove():                            # stuurt de zet naar de game en ontvangt zet geldigheid
    pos = input("Position: ")
    cconn = Client(caddress, authkey=b'tttinfo')
    cconn.send([int(pos), player])
    msg = cconn.recv()
    if msg == "InvalidMove":
        cconn.close()
        error("Invalid move")
        sendMove()
    elif msg == "Valid":
        cconn.close()
    elif "winner" in msg or msg == "draw" or msg == "end":
        cconn.close()
        specialmsg(msg)
        return True


def receive():                       # ontvant het bord/ bericht
    global layout
    rconn = listen.accept()
    msg = rconn.recv()
    rconn.close()
    if str(msg) == "end":
        print("Game stopped. Exiting")
        exit()
    if specialmsg(msg):
        receive()
        return False
    layout = msg
    printBoard()
    return True


def game():
    while True:
        receive()
        if sendMove():
            break


def main():                               # volgorde van wat uitgevoerd wordt
    pcConfig()
    setIp()
    startGame()
    game()


if __name__ == "__main__":                  # checkt of game als module wordt uitgevoerd
    try:                                    # onderbreekt programma zonder errors
        if sys.version_info[0] < 3:
            error("Must be running python version 3")
            sleep(3)
        else:
            from ipaddress import ip_address
            main()
    except KeyboardInterrupt:
        error("Exiting program", True)
else:
    error("Game should not be running as an api", True)