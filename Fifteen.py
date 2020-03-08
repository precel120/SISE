import ast


class Fifteen:
    def __init__(self):
        self.board = [[0 for x in range(4)] for y in range(4)]
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
        options = {"U": 0, "D": 0, "R": 0, "L": 0}
        if self.checkUp() is not None:
            options["U"] = self.checkUp()
        if self.checkDown() is not None:
            options["D"] = self.checkDown()
        if self.checkRight() is not None:
            options["R"] = self.checkRight()
        if self.checkLeft() is not None:
            options["L"] = self.checkLeft()
        return options

    # def checkOrder(self):
    #     correct = [*range(1, 16), 0]
    #     wrongPos = []
    #     for i in range(len(self.board)):
    #         for j in range(len(self.board[i])):
    #             if self.board[i][j] != correct[i * 4 + j]:
    #                 wrongPos.append([i, j])
    #     return wrongPos

    def checkBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != (i * 4 + j) + 1 and self.board[3][3] != 0:
                    return False
        return True

    def move(self, direction):
        zeroPos = self.findZero()

        # self.swapPosition(zeroPos, direction)
        # if self.checkBoard():
        #     return True
        # else:
        #     zeroPos = self.findZero()
        #     self.visited[zeroPos[0]][zeroPos[1]] = True
        #     self.swapPosition(previousPos, zeroPos)

        options = self.findOptions()
        for char in self.searchOrder:
            if char == "L":
                if options["L"] != 0:
                    if not self.visited[options["L"][0]][options["L"][1]]:
                        self.swapPosition(zeroPos, options["L"])
                        zeroPos = self.findZero()
                        self.visited[zeroPos[0]][zeroPos[1]] = True
            elif char == "U":
                if options["U"] != 0:
                    if not self.visited[options["U"][0]][options["U"][1]]:
                        self.swapPosition(zeroPos, options["U"])
                        zeroPos = self.findZero()
                        self.visited[zeroPos[0]][zeroPos[1]] = True
            elif char == "D":
                if options["D"] != 0:
                    if not self.visited[options["D"][0]][options["D"][1]]:
                        self.swapPosition(zeroPos, options["D"])
                        zeroPos = self.findZero()
                        self.visited[zeroPos[0]][zeroPos[1]] = True
            elif char == "R":
                if options["R"] != 0:
                    if not self.visited[options["R"][0]][options["R"][1]]:
                        self.swapPosition(zeroPos, options["R"])
                        zeroPos = self.findZero()
                        self.visited[zeroPos[0]][zeroPos[1]] = True

    def printBoard(self):
        for i in range(len(self.board)):
            print(self.board[i])

    def bfs(self):
        zeroPos = self.findZero()
        self.visited = [[False for i in range(len(self.board))] for j in range(len(self.board))]
        self.visited[zeroPos[0]][zeroPos[1]] = True
        i = 0

        while not self.checkBoard():
            print(i)
            print(self.checkBoard())
            self.move(self.searchOrder)
            self.printBoard()


fif = Fifteen()
fif.printBoard()
fif.bfs()
