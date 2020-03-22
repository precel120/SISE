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
        file.write(str("{:.3f}".format(elapsedTime)))

def saveBoard(fileName, algorithm, parameter, board):
    with open(fileName, 'w') as file:
        file.seek(0)
        for i in range(len(board)):
            file.write(str(board[i]).strip("[]"))
            file.write("\n")

def saveSolution(fileName, solutionLength, allMoves):
    with open(fileName, 'w') as file:
        file.seek(0)
        file.write(str(solutionLength))
        if solutionLength != -1:
            file.write('\n')
            file.write(''.join(allMoves))

def readBoard(fileName, board):
    with open(fileName) as file:
        file.readline()
        for i in range(len(board)):
            temp = file.readline().split()
            temp = list(map(int, temp))
            board[i] = temp