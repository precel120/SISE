import ast
from collections import OrderedDict


class Fifteen:
    def __init__(self):
        self.recursionLevel = 0
        self.lastMove = 0
        self.board = [[0 for x in range(4)] for y in range(4)]
        self.visited = [[False for i in range(len(self.board))] for j in range(len(self.board))]
        temp = [[0 for x in range(4)] for y in range(4)]
        with open('Plik z układem początkowym.txt', 'r') as file:
            for i in range(len(self.board)):
                temp[i] = file.readline().strip("\n")
                temp[i] = list(ast.literal_eval(temp[i]))
                self.board[i] = temp[i]
        # defining search order
        allowed_chars = {"L", "R", "D", "U"}
        self.searchOrder = input("Define search order\n").upper()
        while not set(self.searchOrder).issubset(allowed_chars):
            print("Wrong!")
            self.searchOrder = input("Define search order again\n").upper()

    def swapPosition(self, pos1, pos2):
        self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = self.board[pos2[0]][pos2[1]], self.board[pos1[0]][pos1[1]]

    def findZero(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return [i, j]

    def checkLeft(self):
        zeroPos = self.findZero()
        if zeroPos[1] > 0 and any(self.board[zeroPos[0]][zeroPos[1] - 1] in sublist for sublist in self.board):
            return [zeroPos[0], zeroPos[1] - 1]

    def checkRight(self):
        zeroPos = self.findZero()
        if zeroPos[1] < 3 and any(self.board[zeroPos[0]][zeroPos[1] + 1] in sublist for sublist in self.board):
            return [zeroPos[0], zeroPos[1] + 1]

    def checkUp(self):
        zeroPos = self.findZero()
        if zeroPos[0] > 0 and any(self.board[zeroPos[0] - 1][zeroPos[1]] in sublist for sublist in self.board):
            return [zeroPos[0] - 1, zeroPos[1]]

    def checkDown(self):
        zeroPos = self.findZero()
        if zeroPos[0] < 3 and any(self.board[zeroPos[0] + 1][zeroPos[1]] in sublist for sublist in self.board):
            return [zeroPos[0] + 1, zeroPos[1]]

    def findOptions(self):
        temp = {self.searchOrder[0]: 0, self.searchOrder[1]: 0, self.searchOrder[2]: 0, self.searchOrder[3]: 0}
        options  = OrderedDict(temp.items())
        if self.checkUp() is not None:
            options["U"] = self.checkUp()
        if self.checkDown() is not None:
            options["D"] = self.checkDown()
        if self.checkRight() is not None:
            options["R"] = self.checkRight()
        if self.checkLeft() is not None:
            options["L"] = self.checkLeft()
        return options

    def checkBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != (i * 4 + j) + 1 or self.board[3][3] != 0:
                    return False
        return True

    def move(self, char):
        zeroPos = self.findZero()
        options = self.findOptions()

        if char == "L" and self.lastMove != "R":
            if options["L"] != 0:
                if not self.visited[options["L"][0]][options["L"][1]]:
                    self.swapPosition(zeroPos, options["L"])
                    self.lastMove = "L"
                    zeroPos = self.findZero()
                    self.visited[zeroPos[0]][zeroPos[1]] = True
                    self.recursionLevel += 1
        elif char == "U" and self.lastMove != "D":
            if options["U"] != 0:
                if not self.visited[options["U"][0]][options["U"][1]]:
                    self.swapPosition(zeroPos, options["U"])
                    self.lastMove = "U"
                    zeroPos = self.findZero()
                    self.visited[zeroPos[0]][zeroPos[1]] = True
                    self.recursionLevel += 1
        elif char == "D" and self.lastMove != "U":
            if options["D"] != 0:
                if not self.visited[options["D"][0]][options["D"][1]]:
                    self.swapPosition(zeroPos, options["D"])
                    self.lastMove = "D"
                    zeroPos = self.findZero()
                    self.visited[zeroPos[0]][zeroPos[1]] = True
                    self.recursionLevel += 1
        elif char == "R" and self.lastMove != "L":
            if options["R"] != 0:
                if not self.visited[options["R"][0]][options["R"][1]]:
                    self.swapPosition(zeroPos, options["R"])
                    self.lastMove = "R"
                    zeroPos = self.findZero()
                    self.visited[zeroPos[0]][zeroPos[1]] = True
                    self.recursionLevel += 1

    def printBoard(self):
        for i in range(len(self.board)):
            print(self.board[i])
        print()

    def bfs(self):
        zeroPos = self.findZero()
        self.visited[zeroPos[0]][zeroPos[1]] = True
        i = 0

        while not self.checkBoard():
            print(i)
            print(self.checkBoard())
            for char in self.searchOrder:
                self.move(char)
                self.printBoard()

    def dfs(self, maxDepth = 20):
        zeroPos = self.findZero()
        self.visited[zeroPos[0]][zeroPos[1]] = True

        while not self.checkBoard():
            if self.recursionLevel >= maxDepth:
                break
            for char in self.searchOrder:
                opt = self.findOptions()
                print(self.lastMove)
                while opt[char] != 0:
                    if (self.lastMove == "U" and opt[char] == "D") or (self.lastMove == "L" and opt[char] == "R") or (self.lastMove == "R" and opt[char] == "L") or (self.lastMove == "D" and opt[char] == "U"):
                        continue
                    self.move(char)
                    opt = self.findOptions()
                    self.printBoard()
        self.visited = [[False for i in range(len(self.board))] for j in range(len(self.board))]
        self.visited[self.findZero()[0]][self.findZero()[1]] = True
                

fif = Fifteen()
fif.printBoard()
fif.dfs()