import MaxConnect4Game as m
import time
import maxconnect4 as p
import sys

class AIPlay:
    def __init__(self):
        initialGameboard = m.MaxConnect4Game()
        depth_limit=0

    def setInitState(self,inputFile,game_mode,nextPlayer):
        self.initialGameboard = m.MaxConnect4Game()
        self.initialGameboard.setBoard(inputFile,game_mode,nextPlayer)
        self.initialGameboard.printBoard()
        return self.initialGameboard

    def minimaxDecision(self, initialGameboard):
        score = 0
        move = -1
        starttime = time.time()
        matrix = self.getSuccessors(initialGameboard)
        v = float(-100000)
        for k in matrix.iterkeys():
            temp = self.minValue(matrix[k], alpha=-100000, beta=100000, depth=1)
            if temp >= v:
                v = temp
                move = k
        endtime = time.time()
        print 'Time :', (endtime-starttime)
        isvalid, demo = initialGameboard.playPiece(move)
        return demo, move, v

    def getSuccessors(self, gameboard):
        matrix = {}
        nCol = gameboard.numberofpossibleColumns()
        for i in range(len(nCol)):
            move = nCol.pop()
            isValid, newGameboard = gameboard.playPiece(move)
            matrix[move] = newGameboard
        return matrix

    def maxValue(self,currentGameboard, alpha, beta, depth):
        v = float(-100000)
        cnt = currentGameboard.checkPieceCount()
        if cnt == 42:
            util = currentGameboard.utility()
            return util
        elif depth == self.depth_limit:
            score = currentGameboard.evaluation()
            return score
        else:
            depth = depth + 1
            matrix = self.getSuccessors(currentGameboard)
            for k in matrix.iterkeys():
                board = matrix[k]
                temp = self.minValue(board, alpha, beta, depth)
                if temp >= v:
                    v = temp
                    move = k
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

    def minValue(self, currentGameboard, alpha, beta, depth):
        v = float(100000)
        cnt = currentGameboard.checkPieceCount()
        if cnt == 42:
            util = currentGameboard.utility()
            return util
        if depth == self.depth_limit:
            score = currentGameboard.evaluation()
            return score
        else:
            depth = depth + 1
            matrix = self.getSuccessors(currentGameboard)
            for k in matrix.iterkeys():
                board = matrix[k]
                temp = self.maxValue(board, alpha, beta, depth)
                if temp <= v:
                    v = temp
                    move = k
                if v <= alpha:
                    return  v
                beta = min(beta, v)
            return v

def main(argv):
    nextPlayer = ''
    inputFile = ''
    outputFile = ''
    game_mode = argv[1]

    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    if game_mode == 'interactive':
        inputFile = argv[2]
        nextPlayer = argv[3]
        initnextplayer=nextPlayer
        player = p.AIPlay()
        player.depth_limit = int(argv[4])
        initstate = player.setInitState(inputFile,game_mode,nextPlayer)
        while True:
            count = initstate.checkPieceCount()
            if count == 42 and initnextplayer=='computer-next':
                initstate.countScore()
                print 'Computers Score: ', initstate.player2score
                print 'Players Score:', initstate.player1score
                initstate.printBoard()
                break
            elif count==42 and initnextplayer=='human-next':
                initstate.countScore()
                print 'Computers Score: ', initstate.player2score
                print 'Players core:', initstate.player1score
                initstate.printBoard()
                break

            elif nextPlayer == 'computer-next':
                initstate, move, score = player.minimaxDecision(initstate)
                initstate.countScore()
                print 'Computer Score: ', initstate.player2score
                print 'Players scores:', initstate.player1score
                initstate.printBoardToFile('computer.txt')
                nextPlayer = 'human-next'

            elif nextPlayer == 'human-next':
                initstate.countScore()
                initstate.printBoard()
                print 'Computer Score:', initstate.player2score
                print 'Players Score: ', initstate.player1score
                print "Enter column between 1-7:"
                humanMove = int(raw_input())
                while humanMove<1 or humanMove>7:
                    print "Enter column between 1-7:"
                    humanMove = int(raw_input())
                isValid, initstate = initstate.playPiece(humanMove-1)
                while not isValid:
                    print "Enter column between 1-7:"
                    humanMove = int(raw_input())
                    isValid, initstate = initstate.playPiece(humanMove-1)
                initstate.printBoardToFile('human.txt')
                nextPlayer = 'computer-next'

    elif game_mode == 'one-move':
        inputFile = argv[2]
        outputFile = argv[3]
        player = p.AIPlay()
        player.depth_limit = int(argv[4])
        initstate = player.setInitState(inputFile,game_mode,nextPlayer)
        temp, move, score = player.minimaxDecision(initstate)
        print 'Move : Column', move+1
        print 'Score:', score
        print 'GameBoard after column',move+1,'move:'
        temp.printBoard()
        temp.printBoardToFile(outputFile)

if __name__ == '__main__':
    main(sys.argv)