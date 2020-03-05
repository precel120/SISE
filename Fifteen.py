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

    def findZero(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return [i, j]

    def findOptions(self):
        zeroPos = self.findZero()
        options = {"U": 0, "R":0, "D":0, "L":0}
        if  zeroPos[0] > 0 and any(self.board[zeroPos[0]-1][zeroPos[1]] in sublist for sublist in self.board):
            options["U"] = [zeroPos[0]-1, zeroPos[1]]
        if  zeroPos[0] < 3 and any(self.board[zeroPos[0]+1][zeroPos[1]] in sublist for sublist in self.board):
            options["R"] = [zeroPos[0]+1, zeroPos[1]]
        if  zeroPos[1] > 0 and any(self.board[zeroPos[0]][zeroPos[1]-1] in sublist for sublist in self.board):
            options["D"] = [zeroPos[0], zeroPos[1]-1]
        if  zeroPos[1] < 3 and any(self.board[zeroPos[0]][zeroPos[1]+1] in sublist for sublist in self.board):
            options["L"] = [zeroPos[0], zeroPos[1]+1]
        return options

    def move(self, direction):
        pass

    def printBoard(self):
        print(self.board)

fif = Fifteen()
fif.printBoard()

up = fif.findOptions()
print(up)