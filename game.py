import os
import random
import socket
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
os.system("cls")


# TO DO
# Altijd Response op bericht (dit fixt probleem met timing response player)


# stappen
# game check of al players bekend           &
# game deelt player toe, in api             &
# game cleart speelbord                     &
# game ontvangt zet player x
# game stuurt bord naar o
# game ontvangt zet o
# game stuurt bord naar x
# game ontvangt zet x
# game test voor winst                      &
# game reset bord                           &
# game houd bij welke bot vaakst wint

# client stuurt naam en ontvangt x of o     &
# client x ontvangt bord                    &
# client x stuurt zet
# client o ontvangt bord
# client o stuurt zet
# client ontvangt winst of verlies en bord

# client naar game 6000
# game naar client 5000

players = [" ", " ", " ",
           " ", " ", " "]

layout = [" ", " ", " ",
          " ", " ", " ",
          " ", " ", " "]

lastPlayer = " "

winners = []

gameNr = 1
gameNrTarget = 0
gameNrMax = 100

disable_player_check = False

raddress = ('127.0.0.1', 6000)

listen = Listener(raddress, authkey=b'tttinfo')


def Board(position, player):
    global layout
    layout[int(position)] = player.upper()


def printBoard():
    os.system("clear")
    print("-------------------------")
    print("|   " + layout[0] + "   |   " + layout[1] + "   |   " + layout[2] + "   |")
    print("-------------------------")
    print("|   " + layout[3] + "   |   " + layout[4] + "   |   " + layout[5] + "   |")
    print("-------------------------")
    print("|   " + layout[6] + "   |   " + layout[7] + "   |   " + layout[8] + "   |")
    print("-------------------------")


def checkWin(lay):
    if lay[0] and lay[1] and lay[2] == ("X" or "O"):
        print("winner: " + lay[0])
        return True
    elif lay[3] and lay[4] and lay[5] == ("X" or "O"):
        print("winner: " + lay[3])
        return True
    elif lay[6] and lay[7] and lay[8] == ("X" or "O"):
        print("winner: " + lay[6])
        return True
    elif lay[0] and lay[4] and lay[8] == ("X" or "O"):
        print("winner: " + lay[0])
        return True
    elif lay[2] and lay[4] and lay[6] == ("X" or "O"):
        print("winner: " + lay[2])
        return True
    elif lay[0] and lay[3] and lay[6] == ("X" or "O"):
        print("winner: " + lay[0])
        return True
    elif lay[1] and lay[4] and lay[7] == ("X" or "O"):
        print("winner: " + lay[1])
        return True
    elif lay[2] and lay[5] and lay[8] == ("X" or "O"):
        print("winner: " + lay[2])
        return True
    else:
        return False


def inputMove(pos, player):
        if layout[pos] == " ":
            Board(pos, player)
            checkWin(layout)
            return True
        else:
            return False


def receiveMove():
    rconn = listen.accept()
    msg = rconn.recv()
    if not inputMove(msg[0], msg[1]):
        print("Invalid move")
        rconn.send("InvalidMove")
    listen.close()


def initGame():
    print("Game starting")
    global players
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


def reset():
    global layout
    layout = [" ", " ", " ",
              " ", " ", " ",
              " ", " ", " "]


def sendBoard(player):
    if players[1] == player:
        addr = (players[2], 5000)
        conn = Client(addr, authkey=b'tttinfo')
        conn.send(layout)
        conn.close()
    else:
        addr = (players[5], 5000)
        conn = Client(addr, authkey=b'tttinfo')
        conn.send(layout)
        conn.close()


def printIp():
    if socket.gethostbyname(socket.gethostname()) == "127.0.1.1":
        print("[ERROR] not able to get correct Local IP")
    else:
        print("Game IP: " + socket.gethostbyname(socket.gethostname()))


def checkPlayersEmpty():
    for i in range(6):
        if players[i] != " ":
            return False
    return True


def checkPlayers():
    global players
    global disable_player_check
    if not disable_player_check:
        inp = input("Do you want to disable player check? (y/n): ")
        if inp.upper() == "Y":
            disable_player_check = True
            return None
        if not checkPlayersEmpty():
            inp = input("Players not empty, do you want to reset? (y/n): ")
            if inp.upper() == "Y":
                players = [" ", " ", " ",
                           " ", " ", " "]
                print(players)  # DEBUG


def gameCount():
    global gameNrTarget
    nr = int(input("How manny times do you want to play sequential? (max " + str(gameNrMax) + ") "))
    if isinstance(nr, int):
        if nr > gameNrMax:
            print("Exceeded maximum of '" + str(gameNrMax) + "' games")
        gameNrTarget = nr
    else:
        print("input not int")
        exit()

def game():
    printIp()
#    inputMove(4,"O")
#    printBoard()
    initGame()
    print(players)
    sendBoard("X")
    receiveMove()
    printBoard()

    checkPlayers()


def main():
    global gameNr
    gameCount()
    while gameNr <= gameNrTarget:
        game()
        gameNr += 1


if __name__ == "__main__":
    main()
