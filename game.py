import os
import random
import socket
import sys
from time import sleep
from multiprocessing.connection import Listener
from multiprocessing.connection import Client


def clearS():                                       # scherm schoon maken
    if sys.platform.startswith("Linux"):
        os.system("clear")
    elif sys.platform.startswith("Win32"):
        os.system("cls")


# TODO
# player randomizer

# VERSIE 1.6

# stappen
# game check of al players bekend           &
# game deelt player toe, in api             &
# game cleart speelbord                     &
# game ontvangt zet player x                &
# game stuurt bord naar o                   &
# game ontvangt zet o                       &
# game stuurt bord naar x                   &
# game ontvangt zet x                       &
# game test voor winst                      &
# game reset bord                           &
# game houd bij welke bot vaakst wint       $
# client stuurt naam en ontvangt x of o     &
# client x ontvangt bord                    &
# client x stuurt zet                       &
# client o ontvangt bord                    &
# client o stuurt zet                       &
# client ontvangt winst of verlies en bord  $

# client naar game 6000
# game naar client 5000

Lport = 6000                        # luister port
Cport = 5000                        # connectie port
IP = ''
local = False

players = [" ", " ", " ",           # naam, speler, ip/port
           " ", " ", " "]

layout = [" ", " ", " ",            # speelbord
          " ", " ", " ",
          " ", " ", " "]

winners = []
outputfile = "win-output.txt"
outputtofile = True
raddress = ""                       # (ip, port)

gameNr = 1                          # huidige game nummer
gameNrTarget = 0                    # hoeveel spellen er gespeeld worden
gameNrMax = 10

disable_player_check = False        # check of de spelers leeg zijn aan het einde van de ronden


def error(msg, ext=False):          # error afdrukken
    if ext:
        print("[ERROR] " + msg)
        exit()                      # stop het spel
    else:
        print("[ERROR] " + msg)


def send(player,msg):
    try:
        if len(players[2]) > 4:                             # als ip/port groter is dan 4 dan is het een ip
            if player == "ALL":
                addr = (players[2], Cport)
                conn = Client(addr, authkey=b'tttinfo')
                conn.send(msg)
                conn.close()
                addr = (players[5], Cport)
                conn = Client(addr, authkey=b'tttinfo')
                conn.send(msg)
                conn.close()
            elif players[1] == player:
                addr = (players[2], Cport)
                conn = Client(addr, authkey=b'tttinfo')
                conn.send(msg)
                conn.close()
            else:
                addr = (players[5], Cport)
                conn = Client(addr, authkey=b'tttinfo')
                conn.send(msg)
                conn.close()
        else:                                               # anders is het een port dus is het lokaal gespeeld
            if player == "ALL":
                addr = (IP, int(players[2]))
                conn = Client(addr, authkey=b'tttinfo')
                conn.send(msg)
                conn.close()
                addr = (IP, int(players[5]))
                conn = Client(addr, authkey=b'tttinfo')
                conn.send(msg)
                conn.close()
            elif players[1] == player:
                addr = (IP, int(players[2]))
                conn = Client(addr, authkey=b'tttinfo')
                conn.send(msg)
                conn.close()
            else:
                addr = (IP, int(players[5]))
                conn = Client(addr, authkey=b'tttinfo')
                conn.send(msg)
                conn.close()
    except ConnectionRefusedError:
        error("Player refused connection", True)


def pcConfig():                                            # vraag of game lokaal of via netwerk gespeelt wordt
    global players
    global local
    inp = input("Do you want to play on one PC? (y/n): ")
    if inp.upper() == "Y":
        local = True
        initGame()
    elif inp.upper() == "N":
        local = False
        initGame()
    else:
        error("Invalid input", True)


def setIp():
    global raddress
    global IP
    global listen
    IP = socket.gethostbyname(socket.gethostname())  # zoekt lokaal ip op
    if IP == "127.0.1.1":                            # kan lokaal ip niet vinden
        error("not able to get correct Local IP")
        inp = input("Enter IP manually: ")
        if len(inp) == 0:                           # is er input
            error("no IP provided", True)
        try:
            if ip_address(inp):                     # is het een echt ip
                raddress = (str(inp), Lport)
        except ValueError:
            error("Invalid ip", True)
    else:
        inp = input("Is '" + IP + "' The correct IP? (y/n): ")       # als het ip gevonden kan worden
        if inp.upper() == "Y":
            raddress = (IP, Lport)
            print(raddress)

        elif inp.upper() == "N":                                    # klopt het gehaalde ip niet
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


def Board(position, player):            # plaats zet
    global layout
    layout[int(position)] = player.upper()


def printBoard():
    clearS()
    print("-------------------------")
    print("|   " + layout[0] + "   |   " + layout[1] + "   |   " + layout[2] + "   |")
    print("-------------------------")
    print("|   " + layout[3] + "   |   " + layout[4] + "   |   " + layout[5] + "   |")
    print("-------------------------")
    print("|   " + layout[6] + "   |   " + layout[7] + "   |   " + layout[8] + "   |")
    print("-------------------------")


def Won(player):                            # wat wordt uitgevoed als iemand wint
    global winners
    msg = "winner: " + player
    print(msg)
    if outputtofile:
        file = open(outputfile, "a")
        file.write(player + "\n")
    winners.append(player)
    send("ALL", msg)


def checkWin():
    lay = layout
    if (lay[0] == "X" and lay[1] == "X" and lay[2] == "X") or (lay[0] == "O" and lay[1] == "O" and lay[2] == "O"):
        Won(lay[0])
        return True
    elif (lay[3] == "X" and lay[4] == "X" and lay[5] == "X") or (lay[3] == "O" and lay[4] == "O" and lay[5] == "O"):
        Won(lay[3])
        return True
    elif (lay[6] == "X" and lay[7] == "X" and lay[8] == "X") or (lay[6] == "O" and lay[7] == "O" and lay[8] == "O"):
        Won(lay[6])
        return True
    elif (lay[0] == "X" and lay[4] == "X" and lay[8] == "X") or (lay[0] == "O" and lay[4] == "O" and lay[8] == "O"):
        Won(lay[0])
        return True
    elif (lay[2] == "X" and lay[4] == "X" and lay[6] == "X") or (lay[2] == "O" and lay[4] == "O" and lay[6] == "O"):
        Won(lay[2])
        return True
    elif (lay[0] == "X" and lay[3] == "X" and lay[6] == "X") or (lay[0] == "O" and lay[3] == "O" and lay[6] == "O"):
        Won(lay[0])
        return True
    elif (lay[1] == "X" and lay[4] == "X" and lay[7] == "X") or (lay[1] == "O" and lay[4] == "O" and lay[7] == "O"):
        Won(lay[1])
        return True
    elif (lay[2] == "X" and lay[5] == "X" and lay[8] == "X") or (lay[2] == "O" and lay[5] == "O" and lay[8] == "O"):
        Won(lay[2])
        return True
    for i in lay:                       # als alle plekken vol zijn en er niet gewonnen is dus gelijkspel
        if i == " ":
            return None
    file = open(outputfile, 'a')
    file.write("draw")
    file.close()
    winners.append("draw")
    send("ALL","draw")
    return True


def inputMove(pos, player):                     # checkt gevraagde zet mogelijk
        if pos > 8 or pos < 0:
            return False
        elif layout[pos] == " ":
            Board(pos, player)
            return True
        else:
            return False


def receiveMove():                              # ontvangt zet en zet de zet
    rconn = listen.accept()
    msg = rconn.recv()
    if not inputMove(msg[0], msg[1]):
        print("Invalid move")
        rconn.send("InvalidMove")
        receiveMove()
    else:
        print("Valid")
        rconn.send("Valid")
    rconn.close()


def winoutput():                                   # configureren van output naar een file
    global outputtofile
    if os.path.isfile(outputfile):
        inp = input(outputfile + " exists, do you want to clear it? (y/n): ")
        if inp.upper() == "Y":
            open(outputfile, 'w').close()
            inp = input("do you want to create an output file? (y/n): ")
            if inp.upper() == "Y":
                outputtofile = True
            elif inp.upper() == "N":
                outputtofile = False
            else:
                error("invalid input", True)
        elif inp.upper() == "N":
            print(outputfile + " kept")
            inp = input("do you want to use an output file? (y/n): ")
            if inp.upper() == "Y":
                outputtofile = True
            elif inp.upper() == "N":
                outputtofile = False
            else:
                error("invalid input", True)
        else:
            error("invalid input", True)
    else:
        inp = input(outputfile + " doesn't exist, do you want to use an output file? (y/n): ")
        if inp.upper() == "Y":
            outputtofile = True
        elif inp.upper() == "N":
            outputtofile = False
        else:
            error("invalid input", True)


def initGame():
    print("Game starting on port: " + str(Lport))
    global players
    if not local:                                   # voor netwerk
        conn = listen.accept()
        players[0] = conn.recv()
        if bool(random.getrandbits(1)):
            players[1] = "X"
            players[4] = "O"
            players[2] = listen.last_accepted[0]
            conn.send("X")
            conn.close()
            rconn = listen.accept()
            players[3] = rconn.recv()
            players[5] = listen.last_accepted[0]
            rconn.send("O")
            rconn.close()
        else:
            players[1] = "O"
            players[4] = "X"
            players[2] = listen.last_accepted[0]
            conn.send("O")
            conn.close()
            rconn = listen.accept()
            players[3] = rconn.recv()
            players[5] = listen.last_accepted[0]
            rconn.send("X")
            rconn.close()
        reset()
    else:                                           # voor lokaal
        conn = listen.accept()
        msg = conn.recv()
        players[0] = msg[0]
        if bool(random.getrandbits(1)):
            players[1] = "X"
            players[4] = "O"
            players[2] = msg[1]
            conn.send("X")
            conn.close()
            conn = listen.accept()
            msg = conn.recv()
            players[3] = msg[0]
            players[5] = msg[1]
            conn.send("O")
            conn.close()
        else:
            players[1] = "O"
            players[4] = "X"
            players[2] = msg[1]
            conn.send("O")
            conn.close()
            conn = listen.accept()
            msg = conn.recv()
            players[3] = msg[0]
            players[5] = msg[1]
            conn.send("X")
            conn.close()
        reset()


def reset():                        # maak bord leeg
    global layout
    layout = [" ", " ", " ",
              " ", " ", " ",
              " ", " ", " "]


def sendBoard(player):
    send(player,layout)


def checkPlayersEmpty():
    for i in range(6):
        if players[i] != " ":
            return False
    return True


def checkPlayers(skip=False):                 # check of er spelers bekend zijn (voor mensen tegen elkaar)
    global players
    global disable_player_check
    if not disable_player_check:
        if not skip:
            inp = input("Do you want to disable player check? (y/n): ")
            if inp.upper() == "Y":                  # check niet of er spelers bekend zijn aan het begin van een spel
                disable_player_check = True
                return None
            elif inp.upper() == "N":
                disable_player_check = False
            else:
                error("Invalid input", True)
            if not checkPlayersEmpty():
                inp = input("Players not empty, do you want to reset? (y/n): ")
                if inp.upper() == "Y":
                    players = [" ", " ", " ",
                               " ", " ", " "]
                    initGame()
                elif inp.upper() == "N":
                    return None
                else:
                    error("Invalid input", True)
        else:
            if not checkPlayersEmpty():
                inp = input("Players not empty, do you want to reset? (y/n): ")
                if inp.upper() == "Y":
                    send("ALL", "end")
                    players = [" ", " ", " ",
                               " ", " ", " "]
                    initGame()

                elif inp.upper() == "N":
                    return None
                else:
                    error("Invalid input", True)


def gameCount():                                # hoeveel games worden er gespeeld
    global gameNrTarget
    nr = input("How manny times do you want to play sequential? (max " + str(gameNrMax) + "): ")
    try:
        nr = int(nr)
        if nr > gameNrMax:
            print("Exceeded maximum of '" + str(gameNrMax) + "' games")
        gameNrTarget = nr
    except ValueError:
        error("input not int", True)


def showScore():                                # presenteer de scores aan het einde
    x = 0
    o = 0
    d = 0
    for i in winners:
        if i == "X":
            x += 1
        elif i == "O":
            o += 1
        elif i == "draw":
            d += 1
    print("X won " + str(x) + " times")
    print("O won " + str(o) + " times")
    print("Draw " + str(d) + " times")


def game():
    print(players)
    reset()
    for i in range(5):
        sendBoard("X")
        receiveMove()
        clearS()
        printBoard()
        if checkWin():
            return
        sendBoard("O")
        receiveMove()
        clearS()
        printBoard()
        if checkWin():
            return
    return


def main():
    clearS()
    global gameNr
    setIp()
    gameCount()
    checkPlayers()
    winoutput()
    pcConfig()
    while gameNr <= gameNrTarget:
        game()
        gameNr += 1
        if gameNr != gameNrTarget:
            checkPlayers(True)
    showScore()
    print("Game ended")
    send("ALL","end")
    exit()


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
