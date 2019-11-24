from socket import socket, AF_INET, SOCK_DGRAM
import sys
import re
import zmq
import random

ENCODE = "UTF-8"
MAX_BYTES = 65535
PORT = 5559
HOST = '127.0.0.1'

u"""Esse módulo possui a implementação de um cliente UDP. """

CREATED_GAME = "createdGame"
REINITIALIZEDGAME = "reinitializedGame"
MOVEMADE = "moveMade"
WRONGMOVE = "wrongMove"
HITMINE = "hitMine"
FINISH = "finish"

def menu():
    print("****************************************")
    print("*             Minesweeper              *")
    print("****************************************")
    print("   1 - Play                            *")
    print("   2 - Continue                        *")
    print("   9 - Sair                            *")
    print("****************************************\n")
    
def inicio(sock):
    menu()
    command = input(': ')
    
    if (command == '1'):
        sock.send(command.encode(ENCODE))
    elif (command == '2'):
        sock.send(command.encode(ENCODE))
    elif (command == '9'):
        sys.exit(0)
    else:
        print('command inválido.')
        inicio(sock)

    data = sock.recv()
    text = data.decode(ENCODE)
    response = text.split("$")
    
    if response[0] == CREATED_GAME or response[0]==REINITIALIZEDGAME:
        qtdRows = int(response[1])
        qtdClosebyMines = eval(response[2])
        movesRemaing = int(response[3])
        printBoard(qtdRows,qtdClosebyMines)
        print('You have ',movesRemaing,' moves.')
        print()
        iniciar_Jogo(sock)

def printBoard(qtdRows,qtdMines):
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
    
def iniciar_Jogo(sock):
    while (True): 
        a = input('Inset rows and cols: ')
        
        if a == "quit" or a == "quitSave":
            sock.send(a.encode(ENCODE))
            sock.close()
            sys.exit(0)
        
        pattern = re.match("^[0-9]$",a)
        
        if (pattern == None):
            print('Bad move')
            print()
            continue
        
        sock.send(a.encode(ENCODE))
        data = sock.recv()
        response = data.decode(ENCODE)
        response = response.split("$")
        
        if response[0] == WRONGMOVE:
            print("Bad move")
            print()
            continue
        elif response[0] == MOVEMADE:
            qtdRows = int(response[1])
            qtdClosebyMines = eval(response[2])
            movesRemaing = int(response[3])
        elif response[0] == HITMINE:
            print("I guess you're dead\n")
            inicio(sock)
        elif response[0] == FINISH:
            print('*** Congrats you won, not so bad ***')
            inicio(sock)
            
        printBoard(qtdRows,qtdClosebyMines)
        print('you have ',movesRemaing,' moves.')
        print()

if __name__ == "__main__":
    context = zmq.Context()
    print("Connecting to the server")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % PORT)
    client_id = random.randrange(1, 10005)
    inicio(socket)