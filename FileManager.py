def saveStats(fileName, algorithm, parameter, solutionLength, statesVisited, statesProcessed, maxAquiredLevel, elapsedTime):
    with open(fileName, 'w') as file:
        file.seek(0)
        file.write(str(solutionLength))
        file.write("\n")
        file.write(str(statesVisited))
        file.write("\n")
        file.write(str(statesProcessed))
        file.write("\n")
        file.write(str(maxAquiredLevel))
        file.write("\n")
        file.write(str(elapsedTime))

def saveBoard(fileName, algorithm, parameter, board):
    with open(fileName, 'w') as file:
        file.seek(0)
        for i in range(len(board)):
            file.write(str(board[i]).strip("[]"))
            file.write("\n")

def readBoard(fileName, board):
    with open(fileName) as file:
        file.readline()
        for i in range(len(board)):
            temp = file.readline().split()
            temp = list(map(int, temp))
            board[i] = temp