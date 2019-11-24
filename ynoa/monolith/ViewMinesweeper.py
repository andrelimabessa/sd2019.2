from MinesweeperLogic import MineSweeper
from os.path import isfile
from os import remove
import json
import sys

new_game = MineSweeper()

def menu():
    print("****************************************")
    print("*             MineSweeper \U0001F431          *")
    print("****************************************")
    print("   1 - Play                            *")
    print("   2 - Continue                        *")
    print("   3 - Sair                            *")
    print("****************************************\n")
    option = int(input("Choose :"))
    if option == 1:
        play()
    elif option == 2:
        restoreGame()
    else:
        exitGame

def play():
    new_game.new_game(5, 5)
    startGame()

def startGame():
    count = 0    
    while new_game.death() != "Died":
        if new_game.moves_remainings > 0:
            if count != 0:
                print("Good Boy")
            new_game.print_board()
            row = int(input("Insert a row :"))
            col = int(input("Isert a column :"))
            new_game.move(row, col)  
            count += count              
    tryAgain()

def restoreGame():
    if isfile("game.json"):
        file = open("game.json")
        game = json.loads(file.read())
        new_game.restorar(game)
        file.close()
        startGame()
    else:
        print("There arent games saved!\n")

def tryAgain():
    print("   1 - New game  ")
    print("   2 - Quit       ")
    option = int(input("Choose : "))
    if option == 1:
        menu()
    else:
        exitGame()

def exitGame():
    sys.exit(0)

menu()