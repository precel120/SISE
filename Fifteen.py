from collections import OrderedDict
import time
from queue import PriorityQueue
import FileManager


class Fifteen:
    def __init__(self, algorithm, parameter, startFileName, solFileName, statsFileName):
        self.recursionLevel = 0
        self.solutionLength = 0
        self.statesVisited = 0
        self.statesProcessed = 0
        self.maxAquiredLevel = 0
        self.elapsedTime = 0.0
        self.lastMove = ['']
        self.allMoves = []
        self.board = [[0 for x in range(4)] for y in range(4)]
        FileManager.readBoard(startFileName, self.board)

        self.algorithm = algorithm
        if self.algorithm == "BFS" or self.algorithm == "DFS":
            # defining search order
            self.searchOrder = parameter.upper()
            if "BFS":
                self.bfs()
            else:
                self.dfs()
        else:
            self.heuristic = parameter.lower()
            self.AStar()
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
            if options["L"] != 0 and self.lastMove[-1] != "R":
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] - 1])
                self.lastMove.append("L")
                self.recursionLevel += 1
                self.updateStats("L")
                return True
            else:
                return False
        elif char == "U":
            if options["U"] != 0 and self.lastMove[-1] != "D":
                self.swapPosition(zeroPos, [zeroPos[0] - 1, zeroPos[1]])
                self.lastMove.append("U")
                self.recursionLevel += 1
                self.updateStats("U")
                return True
            else:
                return False
        elif char == "D":
            if options["D"] != 0 and self.lastMove[-1] != "U":
                self.swapPosition(zeroPos, [zeroPos[0] + 1, zeroPos[1]])
                self.lastMove.append("D")
                self.recursionLevel += 1
                self.updateStats("D")
                return True
            else:
                return False
        elif char == "R":
            if options["R"] != 0 and self.lastMove[-1] != "L":
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] + 1])
                self.lastMove.append("R")
                self.recursionLevel += 1
                self.updateStats("R")
                return True
            else:
                return False
    
    def updateStats(self, char):
        self.solutionLength += 1
        self.allMoves.append(char)
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
                self.allMoves.append("L")
                return True
            elif self.lastMove[-1] == "R":
                self.lastMove.pop(-1)
                self.swapPosition(zeroPos, [zeroPos[0], zeroPos[1] - 1])
                self.recursionLevel -= 1
                self.solutionLength +=1
                self.allMoves.append("R")
                return True
            elif self.lastMove[-1] == "U":
                self.lastMove.pop(-1)
                self.swapPosition(zeroPos, [zeroPos[0] + 1, zeroPos[1]])
                self.recursionLevel -= 1
                self.solutionLength +=1
                self.allMoves.append("U")
                return True
            elif self.lastMove[-1] == "D":
                self.lastMove.pop(-1)
                self.swapPosition(zeroPos, [zeroPos[0] - 1, zeroPos[1]])
                self.recursionLevel -= 1
                self.solutionLength +=1
                self.allMoves.append("D")
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
        self.elapsedTime = (end - start) * 1000.0

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
                        return
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
        self.elapsedTime = (end - start) * 1000.0
        
    def AStar(self):
        start = time.time()
        priorityQueue = PriorityQueue()
        self.searchOrder = "LURD"
        movementCost = 0

        while not self.checkBoard():
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

        end = time.time()
        self.elapsedTime = (end - start) * 1000.0

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


fif = Fifteen("bfs", "LURD", "4x4_01_00001.txt", "4x4_01_00001_bfs_rdul_sol.txt", "4x4_01_00001_bfs_rdul_stats.txt")
fif.printBoard()