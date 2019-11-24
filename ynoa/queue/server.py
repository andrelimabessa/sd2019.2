from socket import socket, AF_INET, SOCK_DGRAM
from random import randint
import re
import threading
from datetime import datetime
import zmq
import time
import sys
import random

class Server:
    ENCODE = "UTF-8"
    MAX_BYTES = 65535
    PORT = 5000
    HOST = ''
    
    qtdRows = 0
    qtdClosebyMines = []
    coordinatesMines = []
    movesRemaining = 0
    
    CREATED_GAME = "createdGame"
    REINITIALIZEDGAME= "reinitializedGame"
    MOVEMADE = "moveMade"
    WRONGMOVE = "wrongMove"
    HITMINE = "hitMine"
    FINISH = "finish"

    def serverFilas(self):      
        try:
            port = "5560"
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.connect("tcp://localhost:%s" % port)
            server_id = random.randrange(1,10005)
            while True:
                data = socket.recv()
                text = data.decode(self.ENCODE)
                self.server(socket, data)
        except:
            for val in sys.exc_info():
                print(val)

    def newGame(self):
        self.coordinatesMines = self.scrambleMines(self.qtdRows)
        self.qtdClosebyMines = []
        self.movesRemaining = self.qtdRows*self.qtdRows-len(self.coordinatesMines)
        print('Jogo criado',self.qtdRows,self.coordinatesMines,self.movesRemaining)
        
    def scrambleMines(self,qtdRows):
        mines = []
        qtdMines = randint(int((qtdRows*qtdRows)/5),int((qtdRows*qtdRows)/3))
        for i in range(qtdMines):
            row = randint(0,qtdRows-1)
            col = randint(0,qtdRows-1)
            if ([row,col] in mines):
                qtdMines += 1
            else:
                mines.append([row,col])
        return mines
    
    def validateCoordinates(self,tuple):
        if (tuple[0] < 0 or tuple[1] < 0) or (tuple[0] > self.qtdRows or tuple[1] > self.qtdRows):
            print("Invalid coordinate",tuple[0],tuple[1],self.qtdRows)
            return False, "Invalid coordinate"
        for qtd in self.qtdClosebyMines:
            if tuple == qtd[0]:
                print("You've made this move")
                return False,"You've made this move"
        return True, "ok"
    
    def startGame(self,tuple):
        print(tuple)
        print(self.coordinatesMines)
        if tuple in self.coordinatesMines:
            print("I guess you're dead\nn")
            return(self.HITMINE)
        qtdMines = 0
        for y in [-1,0,1]:
            for x in [-1,0,1]:
                if self.checkMines([tuple[0]+y,tuple[1]+x], self.coordinatesMines):
                    qtdMines += 1
        self.qtdClosebyMines.append([[tuple[0],tuple[1]],qtdMines])
        self.movesRemaining -= 1
        if self.movesRemaining == 0:
            return (self.FINISH)
        return(self.MOVEMADE)
        
    def checkMines(self,pos,mines):
        if (pos[0]>=0 and pos[1]>=0) and (pos[0]<self.qtdRows and pos[1]<self.qtdRows):
            if (pos in mines):
                return True
            else:
                return False
    
    def saveGame(self):
        arq = open("moves.txt",'w')
        arq.write(str(self.qtdRows)+"\n")
        arq.write(str(self.qtdClosebyMines)+"\n")
        arq.write(str(self.coordinatesMines)+"\n")
        arq.write(str(self.movesRemaining))
        arq.close()

    def restoreGame(self):
        arquivo = open('moves.txt', 'r')
        self.qtdRows = int(arquivo.readline())
        self.qtdClosebyMines  = eval(arquivo.readline())
        self.coordinatesMines = eval(arquivo.readline())
        self.movesRemaining = int(arquivo.readline())
        arquivo.close()
    
    def server(self, socket, data):
        text = data.decode(self.ENCODE)
        print("yay",text)
        
        if (text == '1'):
            self.newGame()
            print("Game created")
            ret = self.CREATED_GAME + "$" + str(self.qtdRows) + "$" + str(self.qtdClosebyMines) + "$" + str(self.movesRemaining)
            data = ret.encode(self.ENCODE)
            socket.send(data)
            
        elif (text == '2'):
            self.restoreGame()
            print("Game Restarted")
            ret = self.reinitializedGame + "$" + str(self.qtdRows) + "$" + str(self.qtdClosebyMines) + "$" + str(self.movesRemaining)
            data = ret.encode(self.ENCODE)
            socket.send(data)
            
        else:
            pattern = re.match("[0-9],[0-9]",text)
            
            if (pattern == None):
                if (text == "quit"):
                    print('Game restored')
                    ret = ""
                    data = text.encode(self.ENCODE)
                    socket.send(data)
                elif (text == "quitSave"):
                    self.saveGame()
                    print('Game saved')
                    ret = ""
                    data = text.encode(self.ENCODE)
                    socket.send(data)
                print('invalid commad')
            else:
                tuple = text.split(",")
                tuple[0] = int(tuple[0])
                tuple[1] = int(tuple[1])
                isValida, msg = self.validateCoordinates(tuple)
                
                if (isValida):
                    print('tuple valid',tuple)
                    jogo = self.startGame(tuple)
                    ret = jogo + "$" + str(self.qtdRows) + "$" + str(self.qtdClosebyMines) + "$" + str(self.movesRemaining)
                    data = ret.encode(self.ENCODE)
                    socket.send(data)
                else:
                    print('tuple invalid')
                    ret = self.WRONGMOVE + "$" + str(self.qtdRows) + "$" + str(self.qtdClosebyMines) + "$" + str(self.movesRemaining)
                    data = ret.encode(self.ENCODE)
                    socket.send(data)
    
    def __init__(self, rows):
        self.qtdRows = rows
        self.serverFilas()    
            
        
if __name__ == "__main__":
    Server(5)