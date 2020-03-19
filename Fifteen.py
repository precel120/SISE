import ast
from collections import OrderedDict
import time
from queue import PriorityQueue
import FileManager


class Fifteen:
    def __init__(self, algorithm):
        self.recursionLevel = 0
        self.solutionLength = 0
        self.statesVisited = 0
        self.statesProcessed = 0
        self.maxAquiredLevel = 0
        self.elapsedTime = 0
        self.lastMove = ['']
        self.board = [[0 for x in range(4)] for y in range(4)]
        temp = [[0 for x in range(4)] for y in range(4)]
        with open('Układ początkowy.txt', 'r') as file:
            for i in range(len(self.board)):
                temp[i] = file.readline().strip("\n")
                temp[i] = list(ast.literal_eval(temp[i]))
                self.board[i] = temp[i]

        self.algorithm = algorithm
        if self.algorithm == "BFS" or self.algorithm == "DFS":
            # defining search order
            self.searchOrder = input("Define search order\n").upper()
            if "BFS":
                self.bfs()
            else:
                self.dfs()
        else:
            self.heuristic = input("Choose heurisitc hamm or manh\n").lower()
            self.AStar()

    def swapPosition(self, pos1, pos2):
        self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = self.board[pos2[0]][pos2[1]], self.board[pos1[0]][
            pos1[1]]

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
        options = OrderedDict(temp.items())
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
                if self.board[i][j] != (i * 4 + j) + 1:
                    if i != 3 or j != 3:
                        return False
        return True

    def move(self, char):
        zeroPos = self.findZero()
        options = self.findOptions()
        if char == "L":
            if options["L"] != 0 and self.lastMove[-1] != "R":
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] - 1])
                self.lastMove.append("L")
                self.recursionLevel += 1
                self.solutionLength += 1
                self.updateMaxAquiredLevel()
                return True
            else:
                return False
        elif char == "U":
            if options["U"] != 0 and self.lastMove[-1] != "D":
                self.swapPosition(zeroPos, [zeroPos[0] - 1, zeroPos[1]])
                self.lastMove.append("U")
                self.recursionLevel += 1
                self.solutionLength += 1
                self.updateMaxAquiredLevel()
                return True
            else:
                return False
        elif char == "D":
            if options["D"] != 0 and self.lastMove[-1] != "U":
                self.swapPosition(zeroPos, [zeroPos[0] + 1, zeroPos[1]])
                self.lastMove.append("D")
                self.recursionLevel += 1
                self.solutionLength += 1
                self.updateMaxAquiredLevel()
                return True
            else:
                return False
        elif char == "R":
            if options["R"] != 0 and self.lastMove[-1] != "L":
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] + 1])
                self.lastMove.append("R")
                self.recursionLevel += 1
                self.solutionLength +=1
                self.updateMaxAquiredLevel()
                return True
            else:
                return False
    
    def updateMaxAquiredLevel(self):
        if self.recursionLevel > self.maxAquiredLevel:
            self.maxAquiredLevel = self.recursionLevel

    def moveBackwards(self, howMany = 1):
        zeroPos = self.findZero()
        for counter in range(howMany):
            if self.lastMove[-1] == "L":
                self.lastMove.pop(-1)
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] + 1])
                self.recursionLevel -= 1
                self.solutionLength +=1
                return True
            elif self.lastMove[-1] == "R":
                self.lastMove.pop(-1)
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] - 1])
                self.recursionLevel -= 1
                self.solutionLength +=1
                return True
            elif self.lastMove[-1] == "U":
                self.lastMove.pop(-1)
                self.swapPosition(zeroPos, [zeroPos[0] + 1, zeroPos[1]])
                self.recursionLevel -= 1
                self.solutionLength +=1
                return True
            elif self.lastMove[-1] == "D":
                self.lastMove.pop(-1)
                self.swapPosition(zeroPos, [zeroPos[0] - 1, zeroPos[1]])
                self.recursionLevel -= 1
                self.solutionLength +=1
                return True

    def printBoard(self):
        for i in range(len(self.board)):
            print(self.board[i])
        print()

    def bfs(self):
        start = time.time()
        depth = 1
        while not self.recursive_bfs(depth):
            depth += 1
        end = time.time()
        self.elapsed = end - start
        FileManager.saveStats(self.algorithm, self.searchOrder, self.solutionLength, self.statesVisited, self.statesProcessed, self.maxAquiredLevel, self.maxAquiredLevel)
        FileManager.saveBoard(self.algorithm, self.searchOrder, self.board)

    def recursive_bfs(self, depth):
        if depth == 0:
            return self.checkBoard()
        for char in self.searchOrder:
            if self.move(char):
                if self.recursive_bfs(depth - 1):
                    return True
                else:
                    self.moveBackwards()
        return False

    def dfs(self, maxDepth = 20):
        levels = [0 for x in range(maxDepth + 1)]
        start = time.time()
        while not self.checkBoard():
            for char in self.searchOrder:
                opt = self.findOptions()
                while opt[char] != 0 and levels[self.recursionLevel] != 4:
                    if self.checkBoard():
                        return True
                    levels[self.recursionLevel] += 1
                    if self.recursionLevel >= maxDepth:
                        self.moveBackwards()
                        break
                    if not self.move(char):
                        break
                    opt = self.findOptions()
                if levels[self.recursionLevel] == 4:
                    levels[self.recursionLevel] = 0
                    self.moveBackwards()
        end = time.time()
        self.elapsed = end - start
        FileManager.saveStats(self.algorithm, self.searchOrder, self.solutionLength, self.statesVisited, self.statesProcessed, self.maxAquiredLevel, self.maxAquiredLevel)
        FileManager.saveBoard(self.algorithm, self.searchOrder, self.board)
        
    def AStar(self):
        start = time.time()
        priorityQueue = PriorityQueue()
        print(self.hamm())
        end = time.time()
        self.elapsed = end - start
        FileManager.saveStats(self.algorithm, self.heuristic, self.solutionLength, self.statesVisited, self.statesProcessed, self.maxAquiredLevel, self.maxAquiredLevel)
        FileManager.saveBoard(self.algorithm, self.heuristic, self.board)

    def manh(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def hamm(self):
        tilesWrong = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != (i * 4 + j) + 1 and self.board[i][j] != 0:
                    tilesWrong += 1
        return tilesWrong


algorithm = input("Choose alogithm BFS, DFS, A*\n").upper()
fif = Fifteen(algorithm)
fif.printBoard()