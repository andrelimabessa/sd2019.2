import rpyc
import sys
import re
from rpyc.utils.server import ThreadedServer
from random import randint



class MineSweeper(rpyc.Service):
   
    qtdRows = 0
    qtdNearbyMines = []
    minesCoordinates = []
    movesRemaining = 0
    
    CREATED_GAME = "createdGame"
    RESTARTED_GAME = "restartedGame"
    MOVE_MADE = "moveMade"
    WRONG_MOVE = "wrongMove"
    HIT_MINE = "hitMine"
    OVER = "over"

    def exposed_new_game(self):
        self.minesCoordinates = self.scrramble_mines(self.qtdRows)
        self.qtdNearbyMines = []
        self.movesRemaining = self.qtdRows*self.qtdRows-len(self.minesCoordinates)
        print('Hello its a new game',self.qtdRows,self.minesCoordinates,self.movesRemaining)
        return [self.CREATED_GAME, str(self.qtdRows), str(self.qtdNearbyMines), str(self.movesRemaining)]
        
    def scrramble_mines(self,qtdRows):
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
    
    def validate_coordinates(self,tuple):
        if (tuple[0] < 0 or tuple[1] < 0) or (tuple[0] > self.qtdRows or tuple[1] > self.qtdRows):
            print("Invalid coordinate",tuple[0],tuple[1],self.qtdRows)
            return False, "Invalid coordinate"
        for qtd in self.qtdNearbyMines:
            if tuple == qtd[0]:
                print("you already made this move bro")
                return False,"you already made this move bro"
        return True, "ok"
    
    def exposed_start_game(self,tupleStr):
        tuple = eval(tupleStr)
        print(self.minesCoordinates)
        if tuple in self.minesCoordinates:
            print("yep, you're dead\n")
            return([self.HIT_MINE])
        qtdMines = 0
        a = int(tuple[0])
        b = int(tuple[1])
        for y in [-1,0,1]:
            for x in [-1,0,1]:
                if self.check_for_bombs([a+y,b+x], self.minesCoordinates):
                    qtdMines += 1
        self.qtdNearbyMines.append([[a,b],qtdMines])
        self.movesRemaining -= 1
        if self.movesRemaining == 0:
            return [self.OVER]
        return [self.MOVE_MADE,self.qtdRows,self.qtdNearbyMines,self.movesRemaining]
        
    def check_for_bombs(self,pos,mines):
        if (pos[0]>=0 and pos[1]>=0) and (pos[0]<self.qtdRows and pos[1]<self.qtdRows):
            if (pos in mines):
                return True
            else:
                return False
    
    def exposed_save_game(self):
        arq = open("game.txt",'w')
        arq.write(str(self.qtdRows)+"\n")
        arq.write(str(self.qtdNearbyMines)+"\n")
        arq.write(str(self.minesCoordinates)+"\n")
        arq.write(str(self.movesRemaining))
        arq.close()

    def exposed_restore_game(self):
        arquivo = open('game.txt', 'r')
        self.qtdRows = int(arquivo.readline())
        self.qtdNearbyMines  = eval(arquivo.readline())
        self.minesCoordinates = eval(arquivo.readline())
        self.movesRemaining = int(arquivo.readline())
        arquivo.close()
        return [self.RESTARTED_GAME, str(self.qtdRows), str(self.qtdNearbyMines), str(self.movesRemaining)]
    
    def server(self, socket, data):
        text = data.decode(self.ENCODE)
        print("Chegou",text)
        
        if (text == '1'):
            self.new_game()
            print("Jogo criado")
            ret = self.CREATED_GAME + "$" + str(self.qtdRows) + "$" + str(self.qtdNearbyMines) + "$" + str(self.movesRemaining)
            data = ret.encode(self.ENCODE)
            socket.send(data)
            
        elif (text == '2'):
            self.restore_game()
            print("Jogo reiniciado")
            ret = self.RESTARTED_GAME + "$" + str(self.qtdRows) + "$" + str(self.qtdNearbyMines) + "$" + str(self.movesRemaining)
            data = ret.encode(self.ENCODE)
            socket.send(data)
            
        else:
            padrao = re.match("[0-9],[0-9]",text)
            
            if (padrao == None):
                if (text == "quit"):
                    print('Jogo encerrado')
                    ret = ""
                    data = text.encode(self.ENCODE)
                    socket.send(data)
                elif (text == "quitSave"):
                    self.save_game()
                    print('Jogo encerrado e salvo')
                    ret = ""
                    data = text.encode(self.ENCODE)
                    socket.send(data)
                print('Comando inválido')
            else:
                tuple = text.split(",")
                tuple[0] = int(tuple[0])
                tuple[1] = int(tuple[1])
                validMove, msg = self.validate_coordinates(tuple)
                
                if (validMove):
                    print('tuple valida',tuple)
                    jogo = self.start_game(tuple)
                    ret = jogo + "$" + str(self.qtdRows) + "$" + str(self.qtdNearbyMines) + "$" + str(self.movesRemaining)
                    data = ret.encode(self.ENCODE)
                    socket.send(data)
                else:
                    print('tuple invalida')
                    ret = self.WRONG_MOVE + "$" + str(self.qtdRows) + "$" + str(self.qtdNearbyMines) + "$" + str(self.movesRemaining)
                    data = ret.encode(self.ENCODE)
                    socket.send(data)
    

if __name__ == "__main__":
    MineSweeper.qtdRows = 5
    try:
        thread = ThreadedServer(MineSweeper, port=18861)
        thread.start()
    except:
        for val in sys.exc_info():
            print(val)