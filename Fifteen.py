from random import shuffle

class Fifteen:
    board = [[]]

    def __init__(self):
        self.board = [[0 for x in range(4)] for y in range(4)]
        temp = [*range(0,16)]
        shuffle(temp)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = temp[i*4+j]

    def swapPosition(self, pos1, pos2):
        self.board[pos1[0]][pos1[1]],  self.board[pos2[0]][pos2[1]] =  self.board[pos2[0]][pos2[1]],  self.board[pos1[0]][pos1[1]]

    def findZero():
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return zeroPos = [i, j]

    def findOptions(self):
        zeroPos = findZero()


    def move(self, direction):
        if direction == "U":

    
    def printBoard(self):
        print(self.board)

fif = Fifteen()
fif.printBoard()

fif.swapPosition([0,0],[1,1])

fif.printBoard()