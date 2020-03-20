def saveStats(depth, ID, algorithm, parameter, solutionLength, statesVisited, statesProcessed, maxAquiredLevel, elapsedTime):
    with open(f'4x4_{depth}_{ID}_{algorithm}_{parameter}_stats.txt', 'w') as file:
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

def saveBoard(depth, ID, algorithm, parameter, board):
    with open(f'4x4_{depth}_{ID}_{algorithm}_{parameter}_.txt', 'w') as file:
        file.seek(0)
        for i in range(len(board)):
            file.write(str(board[i]).strip("[]"))
            file.write("\n")
