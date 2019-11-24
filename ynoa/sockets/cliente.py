import socket, pickle
import sys, os
import random
from ast import literal_eval

HOST = '127.0.0.1'
PORT = 5000
ENCODE = "UTF-8"
MAX_BYTES = 65535

menu_actions = {}

def showBoard(matrix, l):
    print("")
    for i in range(l):
        print(matrix[i])

def sortBombs(matrix, matrixRows, matrixCols, qtdBombs):
    waiter = ["SB", matrixRows, matrixCols, qtdBombs, matrix]
    data = pickle.dumps(waiter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST, PORT)
    sock.sendto(data, destiny)
    data, address = sock.recvfrom(MAX_BYTES)
    waiter = pickle.loads(data)
    return waiter

def nearBOmbs(row,col,posBombs):
    waiter = ["BR", row, col, posBombs]
    data = pickle.dumps(waiter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST, PORT)
    sock.sendto(data, destiny)
    data, address = sock.recvfrom(MAX_BYTES)
    waiter = pickle.loads(data)
    return waiter

def save(history):
    waiter = ["SV", history]
    data = pickle.dumps(waiter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST, PORT)
    sock.sendto(data, destiny)

def main_menu():

    if (os.path.exists('log_game.txt') == True):
        waiter = ["VF",'log_game.txt']
        data = pickle.dumps(waiter)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destiny = (HOST, PORT)
        sock.sendto(data, destiny)
        data, address = sock.recvfrom(MAX_BYTES)
        waiter = literal_eval(str(pickle.loads(data)))
        dict = waiter

        if (dict.get('without') == "-1"):
            print("==================================================")
            print("                  MINESWEEPER \U0001F4A3")
            print("==================================================\n")
            print("Choose \n")
            print("1. Start Game")
            print("0. Quit")
            choice = input(" >> ")
            exec_menu(choice)
            return
        else:
            restartGame()
    else:
        print("==================================================")
        print("                  MINESWEEPER \U0001F4A3")
        print("==================================================\n")
        print("Choose \n")
        print("1. Start Game")
        print("0. Quit")
        choice = input(" >> ")
        exec_menu(choice)
        return

def exec_menu(choice):
    os.system("cls")
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid move \n")
            os.system("pause")
            menu_actions['main_menu']()
    return

def newGame():
    os.system("cls")
    print("==================================================")
    print("                   MINESWEEPER \U0001F4A3")
    print("==================================================\n")
    lose = False
    moves = 0
    matrixRows = int(input("How many rows? >> "))
    matrixCols = int(input("How many columns >> "))
    qtdBombs = int(input("And how many bombs?? >> "))
    waiter = ["GM", matrixRows, matrixCols, qtdBombs]
    data = pickle.dumps(waiter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST,PORT)
    sock.sendto(data, destiny)
    print("Requesting server",sock.getsockname())
    data, address = sock.recvfrom(MAX_BYTES)
    waiter = pickle.loads(data)
    matrix = waiter
    showBoard(matrix,matrixRows)
    posBombs = sortBombs(waiter, int(matrixRows), int(matrixCols), int(qtdBombs))
    qtdMoves = ((matrixRows * matrixCols)-len(posBombs))
    while (lose==False):
        print("\nMoves: %d | Moves Remaining: %d" %(moves,qtdMoves ))
        row = int(input("Which row?>> "))-1
        col = int(input("Which col?>> "))-1
        os.system("cls")
        if ([row,col] in posBombs):
            print("\n\n. . . . . . . . . . . . . . . . . . . . . . . .")
            print(". . . . . . . . . . . . . . . . . . . . . . . .")
            print(". . . . . . . \U0001F4A5 \U0001F92F you lose . . . . . . .")
            print(". . . . . . . . . . . . . . . . . . . . . . . .")
            print(". . . . . . . . . . . . . . . . . . . . . . . .\n\n")
            history = {"matrix": 0, "posBombs": 0, "moves": 0,"qtdMoves":0, "matrixRows": 0, "matrixCols": 0, "without": "-1"}
            save(history)
            waiter = ["GO"]
            data = pickle.dumps(waiter)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            destiny = (HOST, PORT)
            sock.sendto(data, destiny)
            os.system("pause")
            os.system("cls")
            menu_actions['main_menu']()
        else:
            matrix[row][col] = str(nearBOmbs(row,col,posBombs))
            showBoard(matrix,matrixRows)
            moves += 1
            qtdMoves -= 1
            history = {"matrix": matrix, "posBombs":posBombs, "moves": moves,"qtdMoves":qtdMoves,"matrixRows": matrixRows, "matrixCols": matrixCols, "without": 0}
            if (((matrixRows*matrixCols)-moves)==len(posBombs)):
                print("Congratulations!!! You won the challenge\n\n Here's a simley cat for you \U0001F63A")
                history = {"matrix": 0, "posBombs": 0, "moves": 0,"qtdMoves":0, "matrixRows": 0, "matrixCols": 0,
                             "without": "-1"}
                save(history)
                waiter = ["WI"]
                data = pickle.dumps(waiter)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                destiny = (HOST, PORT)
                sock.sendto(data, destiny)
                os.system("pause")
                os.system("cls")
                menu_actions['main_menu']()
            save(history)
    return


def restartGame():
    os.system("cls")
    print("==================================================")
    print("                   MINESWEEPER \U0001F4A3")
    print("==================================================\n")
    print("\nOn going game, you wish to continue?\n1: yes\n2: no\n")
    choice = int(input(" >> "))
    if(choice == 2):
        os.system("cls")
        history = {"matrix": 0, "posBombs": 0, "moves": 0,"qtdMoves":0, "matrixRows": 0, "matrixCols": 0, "without": "-1"}
        save(history)
        newGame()
    else:
        waiter = ["JS", 'log_game.txt']
        data = pickle.dumps(waiter)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destiny = (HOST, PORT)
        sock.sendto(data, destiny)

        data, address = sock.recvfrom(MAX_BYTES)
        waiter = literal_eval(str(pickle.loads(data)))
        dict = waiter
        if (dict.get('without') == "-1"):
            print("\nThere's no saved game \U0001F622\n\nDo you wanna start a new game?\n1: yes \n2: np")
            answer = int(input("\n >> "))
            if (answer == 1):
                os.system("cls")
                newGame()
            else:
                os.system("pause")
                menu_actions['main_menu']()
        else:
            matrix = dict.get('matrix')
            posBombs = dict.get('posBombs')
            moves = dict.get('moves')
            matrixRows = dict.get('matrixRows')
            matrixCols = dict.get('matrixCols')
            qtdMoves = dict.get('qtdMoves')
            lose = False
            showBoard(matrix, matrixRows)
            while (lose == False):
                print("\nMoves: %d | Moves Remaining: %d" % (moves, qtdMoves))
                row = int(input("Which row?>> ")) - 1
                col = int(input("Which col?>> ")) - 1
                os.system("cls")
                if ([row, col] in posBombs):
                    print("\n\n. . . . . . . . . . . . . . . . . . . . . . . .")
                    print(". . . . . . . . . . . . . . . . . . . . . . . .")
                    print(". . . . . . . \U0001F4A5 \U0001F92F you lose . . . . . . .")
                    print(". . . . . . . . . . . . . . . . . . . . . . . .")
                    print(". . . . . . . . . . . . . . . . . . . . . . . .\n\n")
                    history = {"matrix": 0, "posBombs": 0, "moves": 0,"qtdMoves":0, "matrixRows": 0, "matrixCols": 0,"without": "-1"}
                    save(history)
                    waiter = ["GO"]
                    data = pickle.dumps(waiter)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    destiny = (HOST, PORT)
                    sock.sendto(data, destiny)
                    os.system("pause")
                    os.system("cls")
                    menu_actions['main_menu']()
                else:
                    matrix[row][col] = str(nearBOmbs(row, col, posBombs))
                    showBoard(matrix, matrixRows)
                    moves += 1
                    qtdMoves -= 1
                    history = {"matrix": matrix, "posBombs": posBombs, "moves": moves,"qtdMoves":qtdMoves, "matrixRows": matrixRows}
                    if (((matrixRows * matrixCols) - moves) == len(posBombs)):
                        print("Congratulations!!! You won the challenge\n\n Here's a simley cat for you \U0001F63A")
                        history = {"matrix": 0, "posBombs": 0, "moves": 0, "matrixRows": 0, "matrixCols": 0,
                                     "without": "-1"}
                        save(history)
                        waiter = ["WI"]
                        data = pickle.dumps(waiter)
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        destiny = (HOST, PORT)
                        sock.sendto(data, destiny)
                        os.system("cls")
                        os.system("pause")
                        menu_actions['main_menu']()
                    save(history)
            return

# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
    os.system("cls")
    print("==================================================")
    print("                   MINESWEEPER \U0001F4A3")
    print("==================================================\n")

    waiter = ["EX"]
    data = pickle.dumps(waiter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destiny = (HOST, PORT)
    sock.sendto(data, destiny)

    sys.exit()

menu_actions = {
    'main_menu': main_menu,
    '1': newGame,
    '2': restartGame,
    '9': back,
    '0': exit,
}

#Menu_Principal
if __name__ == "__main__":
    main_menu()