import rpyc
import sys
from rpyc.utils.server import ThreadedServer
import re


CREATED_GAME = "createdGame"
RESTARTED_GAME = "restartedGame"
MOVE_MADE = "moveMade"
WRONG_MOVE = "wrongMove"
HIT_MINE = "hitMine"
OVER = "over"

def menu():
    print("****************************************")
    print("*             Minesweeper              *")
    print("****************************************")
    print("   1 - Play                            *")
    print("   2 - Continue                        *")
    print("   9 - Sair                            *")
    print("****************************************\n")
    
def start(proxy):
    menu()
    command = input(': ')
    
    if (command == '1'):
        game = proxy.root.new_game()
        print(game)
    elif (command == '2'):
        game = proxy.root.restore_game()
    elif (command == '9'):
        sys.exit(0)
    else:
        print('command invalid.')
    
    if game[0] == CREATED_GAME or game[0]==RESTARTED_GAME:
        qtdRows = int(game[1])
        qtdNearbyMines = eval(game[2])
        jogadas_Restantes = int(game[3])
        print_board(qtdRows,qtdNearbyMines)
        print('You have ',jogadas_Restantes,' moves left.')
        print()
        start_game(proxy)

    
def print_board(qtdRows,qtdMines):
    print()
    print('   0   1   2   3   4')
    row = 0
    for y in range(qtdRows):
        print(str(row) + ' ',end='')
        for x in range(qtdRows):
            if [y,x] in [a[0] for a in qtdMines]:
                for a in qtdMines:
                    if a[0] == [y,x]:
                        print('(' + str(a[1]) + ') ',end='')
                        break
            else:
                print('(X) ',end='')
        print()
        row += 1            
    
def start_game(proxy):
    while (True):
        a = input('Informe a row e col: ')
        
        if a == "quit": 
            sys.exit(0)
        elif a == "quitSave":
            proxy.salvar_Jogo()
            sys.exit(0)
        
        padrao = re.match("^[0-9]$",a)
        if (padrao == None):
            print('Bad move')
            print()
            continue
        
        game = proxy.root.start_game(a)
        
                
        if game[0] == WRONG_MOVE:
            print("Bad move")
            print()
            continue
        elif game[0] == MOVE_MADE:
            qtdRows = game[1]
            qtdNearbyMines = game[2]
            jogadas_Restantes = game[3]
        elif game[0] == HIT_MINE:
            print("yup, you're dead bro\n")
            start(proxy)
        elif game[0] == OVER:
            print('*** yay you won! ***')
            start(proxy)
            
        print_board(qtdRows,qtdNearbyMines)
        print('You have ',jogadas_Restantes,' moves left.')
        print()

if __name__ == "__main__":
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    start(proxy)