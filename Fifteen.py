from collections import OrderedDict
import time
from queue import PriorityQueue
import FileManager
from copy import deepcopy
import sys

class Fifteen:
    def __init__(self, algorithm, parameter, startFileName, solFileName, statsFileName):
        self.maxTime = 1
        self.recursionLevel = 0
        self.solutionLength = 0
        self.statesVisited = 0
        self.statesProcessed = 0
        self.statesList = []
        self.maxAquiredLevel = 0
        self.elapsedTime = 0.0
        self.lastMove = ['']
        self.allMoves = []
        self.board = [[0 for x in range(4)] for y in range(4)]
        FileManager.readBoard(startFileName, self.board)

        self.algorithm = algorithm.upper()
        if self.algorithm == "BFS" or self.algorithm == "DFS":
            # defining search order
            self.searchOrder = parameter.upper()
            if self.algorithm == "BFS":
                start = time.time()
                self.bfs()
                end = time.time()
            else:
                start = time.time()
                self.dfs()
                end = time.time()
        else:
            self.heuristic = parameter.lower()
            start = time.time()
            self.AStar()
            end = time.time()
        self.elapsedTime = (end - start) * 1000.0


        ############## Statistics ##################
        self.statesVisited = self.statesList.__len__()
        tempList = [' '.join([str(x) for x in lst]) for lst in self.statesList]
        self.statesProcessed = list(OrderedDict.fromkeys(tempList)).__len__()
        if self.solutionLength != -1:
            self.solutionLength = len(self.allMoves)
        self.saveAll(solFileName, statsFileName)

    def swapPosition(self, pos1, pos2):
        self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = self.board[pos2[0]][pos2[1]], self.board[pos1[0]][
            pos1[1]]

    def findZero(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return [i, j]

    def checkLeft(self, zeroPos):
        if zeroPos[1] > 0 and any(self.board[zeroPos[0]][zeroPos[1] - 1] in sublist for sublist in self.board):
            return [zeroPos[0], zeroPos[1] - 1]

    def checkRight(self, zeroPos):
        if zeroPos[1] < 3 and any(self.board[zeroPos[0]][zeroPos[1] + 1] in sublist for sublist in self.board):
            return [zeroPos[0], zeroPos[1] + 1]

    def checkUp(self, zeroPos):
        if zeroPos[0] > 0 and any(self.board[zeroPos[0] - 1][zeroPos[1]] in sublist for sublist in self.board):
            return [zeroPos[0] - 1, zeroPos[1]]

    def checkDown(self, zeroPos):
        if zeroPos[0] < 3 and any(self.board[zeroPos[0] + 1][zeroPos[1]] in sublist for sublist in self.board):
            return [zeroPos[0] + 1, zeroPos[1]]

    def findOptions(self):
        temp = {self.searchOrder[0]: 0, self.searchOrder[1]: 0, self.searchOrder[2]: 0, self.searchOrder[3]: 0}
        options = OrderedDict(temp.items())
        zeroPos = self.findZero()

        if self.checkUp(zeroPos) is not None:
            options["U"] = self.checkUp(zeroPos)
        if self.checkDown(zeroPos) is not None:
            options["D"] = self.checkDown(zeroPos)
        if self.checkRight(zeroPos) is not None:
            options["R"] = self.checkRight(zeroPos)
        if self.checkLeft(zeroPos) is not None:
            options["L"] = self.checkLeft(zeroPos)
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
            if options["L"] != 0:
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] - 1])
                self.lastMove.append("L")
                self.recursionLevel += 1
                self.updateStats("L")
                return True
            else:
                return False
        elif char == "U":
            if options["U"] != 0:
                self.swapPosition(zeroPos, [zeroPos[0] - 1, zeroPos[1]])
                self.lastMove.append("U")
                self.recursionLevel += 1
                self.updateStats("U")
                return True
            else:
                return False
        elif char == "D":
            if options["D"] != 0:
                self.swapPosition(zeroPos, [zeroPos[0] + 1, zeroPos[1]])
                self.lastMove.append("D")
                self.recursionLevel += 1
                self.updateStats("D")
                return True
            else:
                return False
        elif char == "R":
            if options["R"] != 0:
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] + 1])
                self.lastMove.append("R")
                self.recursionLevel += 1
                self.updateStats("R")
                return True
            else:
                return False
    
    def updateStats(self, char):
        self.allMoves.append(char)
        if self.recursionLevel > self.maxAquiredLevel:
            self.maxAquiredLevel = self.recursionLevel

    def moveBackwards(self):
        zeroPos = self.findZero()
        if self.lastMove[-1] == "L":
            self.lastMove.pop(-1)
            self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] + 1])
            self.recursionLevel -= 1
            self.allMoves.append("L")
            return True
        elif self.lastMove[-1] == "R":
            self.lastMove.pop(-1)
            self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] - 1])
            self.recursionLevel -= 1
            self.allMoves.append("R")
            return True
        elif self.lastMove[-1] == "U":
            self.lastMove.pop(-1)
            self.swapPosition(zeroPos, [zeroPos[0] + 1, zeroPos[1]])
            self.recursionLevel -= 1
            self.allMoves.append("U")
            return True
        elif self.lastMove[-1] == "D":
            self.lastMove.pop(-1)
            self.swapPosition(zeroPos, [zeroPos[0] - 1, zeroPos[1]])
            self.recursionLevel -= 1
            self.allMoves.append("D")
            return True

    def printBoard(self):
        for i in range(len(self.board)):
            print(self.board[i])
        print()

    def addState(self):
        self.statesList.append(deepcopy(self.board))

    def bfs(self):
        depth = 1
        while not self.recursive_bfs(depth):
            depth += 1

    def recursive_bfs(self, depth):
        if depth == 0:
            return self.checkBoard()
        for char in self.searchOrder:
            if self.move(char):
                self.addState() # Statistic
                if self.recursive_bfs(depth - 1):
                    return True
                else:
                    self.moveBackwards()
        return False

    def dfs(self, maxDepth = 20):
        levels = [0 for x in range(maxDepth + 1)]
        solved = False
        while not solved:
            if self.recursionLevel < maxDepth:
                if levels[self.recursionLevel] < 4:
                    if self.move(self.searchOrder[levels[self.recursionLevel]]):
                        solved = self.checkBoard()
                        self.addState() # Statistic
                        levels[self.recursionLevel - 1] += 1
                    else:
                        levels[self.recursionLevel] += 1
                else:
                    levels[self.recursionLevel] = 0
                    self.moveBackwards()
            else:
                self.moveBackwards()

    def AStar(self):
        priorityQueue = PriorityQueue()
        self.searchOrder = "LURD"
        movementCost = 0
        start = time.time()
        end = 0

        while not self.checkBoard():
            if end - start > self.maxTime:
                self.solutionLength = -1
                return
            options = self.findOptions()
            for option in options:
                if self.move(option):
                    movementCost += 1
                    priorityQueue.put((movementCost + self.manhSum() if (self.heuristic == "manh") else self.hamm(), option))
                    self.moveBackwards()
                    movementCost -= 1
            temp = priorityQueue.get()
            priorityQueue.queue.clear()
            self.move(temp[1])
            self.addState()  # Statistic
            end = time.time()

    def manh(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def manhSum(self):
        manhatanSum = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    manhatanSum += self.manh([i, j], [(self.board[i][j] - 1) // 4, (self.board[i][j] - 1) % 4])
        return manhatanSum

    def hamm(self):
        tilesWrong = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != (i * 4 + j) + 1 and self.board[i][j] != 0:
                    tilesWrong += 1
        return tilesWrong

    def saveAll(self, solFileName, statsFileName):
        if self.algorithm == "DFS" or self.algorithm == "BFS":
            FileManager.saveStats(statsFileName, self.algorithm, self.searchOrder, self.solutionLength, self.statesVisited, self.statesProcessed, self.maxAquiredLevel, self.elapsedTime)
            FileManager.saveSolution(solFileName, self.solutionLength, self.allMoves)
        else:
            FileManager.saveStats(statsFileName, self.algorithm, self.heuristic, self.solutionLength, self.statesVisited, self.statesProcessed, self.maxAquiredLevel, self.elapsedTime)
            FileManager.saveSolution(solFileName, self.solutionLength, self.allMoves)


#fif = Fifteen("dfs", "LRDU", "4x4_06_00013.txt", "4x4_01_00001_bfs_rdul_sol.txt", "4x4_01_00001_bfs_rdul_stats.txt")
fif = Fifteen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])