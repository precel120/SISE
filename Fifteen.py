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
                if self.board[3][3] != 0 and self.board[i][j] != (i * 4 + j) + 1:
                    return False
        return True

    def move(self, direction):
        zeroPos = self.findZero()
        previousPos = zeroPos

        self.swapPosition(zeroPos, direction)
        if self.checkBoard():
            return True
        else:
            zeroPos = self.findZero()
            self.visited[zeroPos[0]][zeroPos[1]] = True
            self.swapPosition(previousPos, zeroPos)

    def printBoard(self):
        print(self.board)

    def bfs(self):
        #defining search order
        allowed_chars = {"L", "R", "D", "U"}
        searchOrder = input("Define search order\n").upper()
        while not set(searchOrder).issubset(allowed_chars):
            print("Wrong!")
            searchOrder = input("Define search order again\n").upper()

        zeroPos = self.findZero()
        queue = [[]]
        self.visited = [[False for i in range(len(self.board))] for j in range(len(self.board))]

        self.visited[zeroPos[0]][zeroPos[1]] = True

        # print(visited)
        # queue.append(zeroPos)
        #
        # while queue:
        #     s = queue.pop(0)
        #
        #     for i in range(len(self.board)):
        #         for j in range(len(self.board[i])):
        #             if not visited[i][j]:
        #                 temp = [i, j]
        #                 queue.append(temp)
        #                 visited[i][j] = True
        #                 print(queue)

        while not self.checkBoard():
            options = self.findOptions()
            print(self.board)
            for char in searchOrder:
                if char == "L":
                    if options["L"] != 0:
                        if not self.visited[options["L"][0]][options["L"][1]]:
                            self.move(options["L"])
                elif char == "U":
                    if options["U"] != 0:
                        if not self.visited[options["U"][0]][options["U"][1]]:
                            self.move(options["U"])
                elif char == "D":
                    if options["D"] != 0:
                        if not self.visited[options["D"][0]][options["D"][1]]:
                            self.move(options["D"])
                elif char == "R":
                    if options["R"] != 0:
                        if not self.visited[options["R"][0]][options["R"][1]]:
                            self.move(options["R"])

            print(self.board)
            print(self.visited)


fif = Fifteen()
fif.printBoard()
fif.bfs()
