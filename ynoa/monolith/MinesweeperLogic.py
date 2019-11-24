from random import randint
from os.path import isfile
from os import remove
import json

class MineSweeper:

    def new_game(self, row, col):
        self.__row = int(row)
        self.__col = int(col)
        self.moves_remainings = self.calculate_total_moves(row, col)
        self.board = self.calc_board(row, col)
        self.bombs = self.generate_bombs(row,col)
        self.died = "Alive"

    def print_board(self):
        for pos in self.board:
            print(str(pos))
    
    def incomplet_game(self):
        return False

    def calc_board(self, row, col):
        return [[str('\u2b1c') for x in range(col)] for j in range(row)]

    def generate_bombs(self, row, col):
        bombs_coordinates = [(randint(0, row - 1), randint(0, col - 1)) for x in range(self.total_bombs())]
        return bombs_coordinates

    def total_bombs(self):
        return int((self.__row*self.__col)/3)
    
    def calculate_total_moves(self,row, col):
        return (row*col) - self.total_bombs()

    def validate_move(self, row, col):
        if row not in range(0, self.__row) and col not in range(0, self.__col):
            print("Ops invalid move")
            return False
        else:
            return True
    
    def check_for_bomb(self, coordenada):
        return coordenada in self.bombs

    def count_near_bombs(self, row, col):
        return len([(row + x, col + y) for x in (-1,0,1) for y in (-1,0,1) if self.check_for_bomb((row + x, col + y))])

    def death(self):
        return self.died

    def end_game(self):
        print("__________________________________\n")
        print("\U0001F4A5 BOOM you're done!\n")
        print("__________________________________\n\n")
        self.died = "Died"


    def save_game(self):
        game = {
            'row': self.__row,
            'col': self.__col,
            'movesRemaining': self.moves_remainings,
            'board': self.board,
            'bombsCoordinates': self.bombs
        }
        file = open("game.json", 'w')

        file.write(json.dumps(game))
        file.close()

    def restore(self, game):
        self.__row = game['row']
        self.__col = game['col']
        self.moves_remainings = game['movesRemaining']
        self.board = game['board']
        self.bombs = game['bombsCoordinates']
        self.died = "Alive"
    
    def move(self, row, col):
        row = int(row)
        col = int(col)

        if not self.validate_move(row, col):
            return "Invalid move"
        
        if  (row, col) in self.bombs:
            self.end_game()
        
        self.board[row][col] = str(self.count_near_bombs(row, col))
        self.moves_remainings -=1
        self.save_game()
        return "Good move"