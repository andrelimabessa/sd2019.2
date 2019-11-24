import socket, pickle
import sys, os, os.path
import threading, random
from ast import literal_eval

HOST = ''
PORT = 5000
ENCODE = "UTF-8"
MAX_BYTES = 65535

def thread_object():
    source = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(source)
    while True:
        data, address = sock.recvfrom(MAX_BYTES)

        tratador = ThreadTratador(sock, data, address)
        tratador.start()

def thread_procedure():
    source = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(source)
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        t = threading.Thread(target=connection, args=tuple([sock, data, address]))
        t.start()

def connection(sock, data, address):
    text = pickle.loads(data)
    cod, *info = text

    if cod == "GM":
        genetateBoard(sock, info, address)
    elif cod == "SB":
        sortBombs(sock, info, address)
    elif cod == "BR":
        nearBombs  (sock, info, address)
    elif cod == "SV":
        save(info,address)
    elif cod == "JS":
        openGame(sock, address)
    elif cod == "VF":
        verifyFile(sock, address)
    elif cod == "EX":
        exit(sock, address)
    elif cod == "GO":
        gameOver(sock, address)
    elif cod == "WI":
        win(sock, address)

def genetateBoard(sock, info, address):
    MatrixRows, MatrixCols, _ = info
    Matrix = [["\u2b1c" for x in range(MatrixRows)] for y in range(MatrixCols)]
    print("Client  : ", address, "Generate the board")
    data = pickle.dumps(Matrix)
    sock.sendto(data, address)

def sortBombs(sock, info, address):
    MatrixRows, MatrixCols, qtdBombs, Matrix = info
    vetor = []
    for i in range(qtdBombs):
        i = random.randint(0, MatrixRows - 1)  
        n = random.randint(0, MatrixCols - 1)  
        while ([i, n] in vetor):
            i = random.randint(0, MatrixRows - 1)
            n = random.randint(0, MatrixCols - 1)
        vetor.append([i, n])
    print("Client  : ", address, "Sorted out the bombs")
    data = pickle.dumps(vetor)
    sock.sendto(data, address)

def nearBombs  (sock, info, address):
    row, col, bombsPos = info
    count = 0
    if ([row + 1, col] in bombsPos):
        count += 1
    if ([row - 1, col] in bombsPos):
        count += 1
    if ([row, col - 1] in bombsPos):
        count += 1
    if ([row - 1, col - 1] in bombsPos):
        count += 1
    if ([row + 1, col - 1] in bombsPos):
        count += 1
    if ([row - 1, col + 1] in bombsPos):
        count += 1
    if ([row + 1, col + 1] in bombsPos):
        count += 1
    if ([row, col + 1] in bombsPos):
        count += 1
    print("Client  : ", address, "Made a move")
    print("Client  : ", address, "Check for near bombs")
    data = pickle.dumps(count)
    sock.sendto(data, address)

def save(info,address):
    historico = info
    hist = open('log_game.txt', 'w')
    hist.write(str(historico))
    print("Client  : ", address, "Saved the game")
    hist.close()


#log
def openGame(sock, address):
    arquivo = open("log_game.txt", 'r')
    info = literal_eval(arquivo.read())
    dict = info[0]
    arquivo.close()
    data = pickle.dumps(dict)
    sock.sendto(data, address)
    print("Client  : ", address, "Restart on going game")

def gameOver(sock, address):
    print("Client  : ", address, "Hit the bomb \U0001F4A3! Game Over! ")

def win(sock, address):
    print("Client  : ", address, "Yay you won \U0001F389")

def exit(sock, address):
    print("Client  : ", address, "End game '\U0001F9B8'")


def verifyFile(sock, address):
    arquivo = open("log_game.txt", 'r')
    info = literal_eval(arquivo.read())
    dict = info[0]
    arquivo.close()
    data = pickle.dumps(dict)
    sock.sendto(data, address)
    print("Client  : ", address, "Check for saved games")

class ThreadTratador(threading.Thread):
    def __init__(self, a, b, c):
        threading.Thread.__init__(self)
        self.sock = a
        self.data = b
        self.address = c

if __name__ == "__main__":
    thread_procedure()