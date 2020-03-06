from random import shuffle


class Fifteen:

    def __init__(self):
        self.board = [[0 for x in range(4)] for y in range(4)]
        temp = [*range(0, 16)]
        shuffle(temp)
        with open('fifteen_starting_matrix.txt', 'w') as file:
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    self.board[i][j] = temp[i * 4 + j]
                file.write(str(self.board[i]).strip('[]'))
                file.write('\n')

    def swapPosition(self, pos1, pos2):
        self.board[pos1[0]][pos1[1]], self.board[pos2[0]][pos2[1]] = self.board[pos2[0]][pos2[1]], self.board[pos1[0]][
            pos1[1]]

    def findZero(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return [i, j]

    def findOptions(self):
        zeroPos = self.findZero()
        options = {"U": 0, "D": 0, "R": 0, "L": 0}
        if zeroPos[0] > 0 and any(self.board[zeroPos[0] - 1][zeroPos[1]] in sublist for sublist in self.board):
            options["U"] = [zeroPos[0] - 1, zeroPos[1]]
        if zeroPos[0] < 3 and any(self.board[zeroPos[0] + 1][zeroPos[1]] in sublist for sublist in self.board):
            options["D"] = [zeroPos[0] + 1, zeroPos[1]]
        if zeroPos[1] < 3 and any(self.board[zeroPos[0]][zeroPos[1] + 1] in sublist for sublist in self.board):
            options["R"] = [zeroPos[0], zeroPos[1] + 1]
        if zeroPos[1] > 0 and any(self.board[zeroPos[0]][zeroPos[1] - 1] in sublist for sublist in self.board):
            options["L"] = [zeroPos[0], zeroPos[1] - 1]
        return options

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
        for i in range(len(self.board)):
            print(self.board[i])

    def bfs(self, search_order=0):
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
            print(self.board)
            if self.checkLeft() != 0:
                if not self.visited[self.checkLeft()[0]][self.checkLeft()[1]]:
                    self.move(self.checkLeft())
            elif self.checkUp() != 0:
                if not self.visited[self.checkUp()[0]][self.checkUp()[1]]:
                    self.move(self.checkUp())
            elif self.checkDown() != 0:
                if not self.visited[self.checkDown()[0]][self.checkDown()[1]]:
                    self.move(self.checkDown())
            elif self.checkRight() != 0:
                if not self.visited[self.checkRight()[0]][self.checkRight()[1]]:
                    self.move(self.checkRight())
            else:
                break

            print(self.board)
            print(self.visited)


fif = Fifteen()
fif.printBoard()
fif.bfs()
