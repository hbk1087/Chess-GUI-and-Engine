import Chess
from Board import Board
from threading import *
import copy
results = []
highest = -999999

#Method to see if a piece is hanging (it can be captured but is not protected by one of its own pieces).
def isHanging(b, x, y, opponentMoves, color):
    position = Chess.convertFilesRanks(x,y)
    piece = b.get(x,y)
    if position in opponentMoves:
        arr = [[0 for x in range(12)] for y in range(12)]
        if color == "WHITE":
           b.set(x, y, Chess.bPawn)
        else:
            b.set(x, y, Chess.wPawn)
        legalMoves = Chess.getAllMoves(b, color, False)
        if not (position in legalMoves):
            b.set(x, y, piece)
            return True
    b.set(x, y, piece)        
    return False

#Method that will assign a numerical value to any board position without searching different move variations. 
def staticEvaluationFunction(b, turn):
    blackEvaluation = 0
    whiteEvaluation = 0
    whitePawnIndex = 0
    blackPawnIndex = 0
    whiteLegalMoves = Chess.getAllMoves(b,'WHITE', False)
    blackLegalMoves = Chess.getAllMoves(b,'BLACK', False)

    #We want the engine to take control of as many squares as possible. High level chess players play positionally. Engine will simulate this by maxmizing possilbe moves it can make.
    whiteEvaluation = whiteEvaluation  + len(whiteLegalMoves)
    blackEvaluation = blackEvaluation + len(blackLegalMoves)
    hangingPiece = True 

    #Loop that will go through the board and add up all the material. Will also take into account pieces that are hanging, doubled pawns, potential checkmates, position, ect.  
    for x in range(2,10):
        for y in range(2,10):
            if b.get(x,y) == Chess.wQueen:
                whiteEvaluation = whiteEvaluation + 900
                if (turn == "BLACK" and isHanging(b,x,y,blackLegalMoves, "WHITE")and hangingPiece):
                    whiteEvaluation = whiteEvaluation - 450
                    hangingPiece = False
                elif (turn == "BLACK" and b.get(x - 1,y + 1) == Chess.bPawn):
                    whiteEvaluation = whiteEvaluation - 40
                    hangingPiece = False
                elif (turn == "BLACK" and b.get(x - 1,y - 1) == Chess.bPawn):
                    whiteEvaluation = whiteEvaluation - 40
            elif b.get(x,y) == Chess.wRook:
                whiteEvaluation = whiteEvaluation + 250
                if (turn == "BLACK" and isHanging(b,x,y,blackLegalMoves, "WHITE") and hangingPiece):
                    whiteEvaluation = whiteEvaluation - 470
                    hangingPiece = False
                elif (turn == "BLACK" and b.get(x - 1,y + 1) == Chess.bPawn):
                    whiteEvaluation = whiteEvaluation - 30
                elif (turn == "BLACK" and b.get(x - 1,y - 1) == Chess.bPawn):
                    whiteEvaluation = whiteEvaluation - 30
            elif b.get(x,y) == Chess.wBishop:
                whiteEvaluation = whiteEvaluation + 310
                if (turn == "BLACK" and isHanging(b,x,y,blackLegalMoves, "WHITE") and hangingPiece):
                    whiteEvaluation = whiteEvaluation - 155
                    hangingPiece = False
                elif (turn == "BLACK" and b.get(x - 1,y + 1) == Chess.bPawn):
                    whiteEvaluation = whiteEvaluation - 20
                    hangingPiece = False
                elif (turn == "BLACK" and b.get(x - 1,y - 1) == Chess.bPawn):
                        whiteEvaluation = whiteEvaluation - 20
                        hangingPiece = False
            elif b.get(x,y) == Chess.wKnight:
                whiteEvaluation = whiteEvaluation + 300
                if (turn == "BLACK" and isHanging(b,x,y,blackLegalMoves, "WHITE") and hangingPiece):
                    whiteEvaluation = whiteEvaluation - 150
                    hangingPiece = False
                elif (turn == "BLACK" and b.get(x - 1,y + 1) == Chess.bPawn):
                    whiteEvaluation = whiteEvaluation - 20
                elif (turn == "BLACK" and b.get(x - 1,y - 1) == Chess.bPawn):
                        whiteEvaluation = whiteEvaluation - 20
                if x == 5:
                    whiteEvaluation = whiteEvaluation + 5
            elif b.get(x,y) == Chess.wPawn:
                whiteEvaluation = whiteEvaluation + 100 + (8 - x) * 5
                if (turn == "BLACK" and isHanging(b,x,y,blackLegalMoves, "WHITE") and hangingPiece):
                    whiteEvaluation = whiteEvaluation - 50
                    hangingPiece = False
                elif x < 5:
                    whiteEvaluation = whiteEvaluation + 5
                elif whitePawnIndex == y:
                    whiteEvaluation = whiteEvaluation - 2
                whitePawnIndex = y
            elif b.get(x,y) == Chess.wKing:
                if Chess.convertFilesRanks(x,y) in blackLegalMoves:
                    if len(Chess.getAllMoves(b,"WHITE", True)) < 1:
                        return 9999
                    whiteEvaluation = whiteEvaluation -10
                if len(whiteLegalMoves) < 9:
                    moves = Chess.getLegalMoves(b,x,y,True)
                    if len(moves) < 1:
                        return 0
                    whiteEvaluation = whiteEvaluation + len(moves)
                    blackKing = Chess.kingLocation(b, "BLACK")
                    ranks = Chess.convertRanks(blackKing)
                    files = Chess.convertFiles(blackKing)
                    if ranks > x:
                        whiteEvaluation = whiteEvaluation + (ranks - x)
                    elif ranks < x:
                        whiteEvaluation = whiteEvaluation - (ranks - x)
                    if files > y:
                        whiteEvaluation = whiteEvaluation + (files- y)
                    elif files < y:
                        whiteEvaluation = whiteEvaluation - (files - y)
                    if x < 5:
                        whiteEvaluation = whiteEvaluation - (4 - x)
                    elif x > 5:
                        whiteEvaluation = whiteEvaluation - (x - 5)
                    if y < 5:
                        whiteEvaluation = whiteEvaluation - (4 - y)
                    elif y > 5:
                        whiteEvaluation = whiteEvaluation - (y - 5)
                    if Chess.convertFilesRanks(x,y) in blackLegalMoves:
                        whiteEvaluation = whiteEvaluation -50
                whiteEvaluation = whiteEvaluation + 9999
                if(x == 9):
                    whiteEvaluation = whiteEvaluation + 1
                if y < 4 or y > 7:
                    whiteEvaluation = whiteEvaluation + 2
            elif b.get(x,y) == Chess.bQueen:
                blackEvaluation = blackEvaluation + 900
                if (turn == "WHITE" and isHanging(b,x,y,whiteLegalMoves, "BLACK")and hangingPiece):
                   blackEvaluation = blackEvaluation - 450
                   hangingPiece = False
                elif (turn == "WHITE" and b.get(x + 1,y + 1) == Chess.wPawn):
                    blackEvaluation = blackEvaluation - 40
                    hangingPiece = False
                elif (b.get(x + 1,y - 1) == Chess.wPawn):
                    blackEvaluation = blackEvaluation - 40
                    hangingPiece = False
            elif b.get(x,y) == Chess.bRook:
                blackEvaluation = blackEvaluation + 250
                if (turn == "WHITE" and isHanging(b,x,y,whiteLegalMoves, "BLACK") and hangingPiece):
                   blackEvaluation = blackEvaluation - 470
                   hangingPiece = False
                elif (turn == "WHITE" and b.get(x + 1,y + 1) == Chess.wPawn):
                    blackEvaluation = blackEvaluation - 30
                    hangingPiece = False
                elif (turn == "WHITE" and b.get(x + 1,y - 1) == Chess.wPawn):
                    blackEvaluation = blackEvaluation - 30
                    hangingPiece = False
            elif b.get(x,y) == Chess.bBishop:
                blackEvaluation = blackEvaluation + 310
                if (turn == "WHITE" and isHanging(b,x,y,whiteLegalMoves, "BLACK") and hangingPiece):
                    blackEvaluation = blackEvaluation - 155
                    hangingPiece = False
                elif (turn == "WHITE" and b.get(x + 1,y + 1) == Chess.wPawn):
                    blackEvaluation = blackEvaluation - 20
                    hangingPiece = False
                elif (turn == "WHITE" and b.get(x + 1,y - 1) == Chess.wPawn):
                    blackEvaluation = blackEvaluation - 20
                    hangingPiece = False
            elif b.get(x,y) == Chess.bKnight:
                blackEvaluation = blackEvaluation + 300
                if (turn == "WHITE" and isHanging(b,x,y,whiteLegalMoves, "BLACK") and hangingPiece):
                   blackEvaluation = blackEvaluation - 150
                   hangingPiece = False
                elif (turn == "WHITE" and b.get(x + 1,y + 1) == Chess.wPawn):
                    blackEvaluation = blackEvaluation - 20
                elif (turn == "WHITE" and b.get(x + 1,y - 1) == Chess.wPawn):
                        blackEvaluation = blackEvaluation - 20
                if x == 5:
                    blackEvaluation = blackEvaluation + 5
            elif b.get(x,y) == Chess.bPawn:
                blackEvaluation = blackEvaluation + 100 + (x - 3) * 5
                if (turn == "WHITE" and isHanging(b,x,y,whiteLegalMoves, "BLACK") and hangingPiece):
                   blackEvaluation = blackEvaluation - 50
                   hangingPiece = False
                if x > 6:
                    blackEvaluation = blackEvaluation + 5
                if blackPawnIndex == y:
                    blackEvaluation = blackEvaluation - 2
                blackPawnIndex = y
            elif b.get(x,y) == Chess.bKing:
                if Chess.convertFilesRanks(x,y) in whiteLegalMoves:
                    if len(Chess.getAllMoves(b,"BLACK", True)) < 1:
                        return -9999
                    blackEvaluation = blackEvaluation -10
                if len(blackLegalMoves)< 9:
                    moves = Chess.getLegalMoves(b,x,y,True)
                    if len(moves) < 1:
                        return 0
                    blackEvaluation = blackEvaluation + len(moves)
                    whiteKing = Chess.kingLocation(b, "WHITE")
                    ranks = Chess.convertRanks(whiteKing)
                    files = Chess.convertFiles(whiteKing)
                    if ranks > x:
                        blackEvaluation = blackEvaluation + (ranks - x)
                    elif ranks < x:
                        blackEvaluation = blackEvaluation - (ranks - x)
                    if files > y:
                        blackEvaluation = blackEvaluation + (files- y)
                    elif files < y:
                        blackEvaluation = blackEvaluation - (files - y)
                    if x < 5:
                       blackEvaluation = blackEvaluation - (4 - x)
                    elif x > 5:
                        blackEvaluation = blackEvaluation - (x - 5)
                    if y < 5:
                        blackEvaluation = blackEvaluation - (4 - y)
                    elif y > 5:
                        blackEvaluation = blackEvaluation - (y - 5)
                    if Chess.convertFilesRanks(x,y) in whiteLegalMoves:
                        blackEvaluation = blackEvaluation -50
                blackEvaluation = blackEvaluation + 9999
                if(x == 2):
                    blackEvaluation = blackEvaluation + 1
                elif y < 4 or y > 7:
                    blackEvaluation = blackEvaluation + 2
            if x > 3 and x < 8 and y > 4 and y < 8:
                if b.get(x,y) == Chess.wBishop or b.get(x,y) == Chess.wKnight or b.get(x,y) == Chess.wRook or b.get(x,y) == Chess.wQueen:
                    whiteEvaluation = whiteEvaluation + 4
                elif b.get(x,y) == Chess.bBishop or b.get(x,y) == Chess.bKnight or b.get(x,y) == Chess.bRook or b.get(x,y) == Chess.bQueen:
                    blackEvaluation =  blackEvaluation + 4
            if x > 4 and x < 7 and y > 4 and y < 8:
                if b.get(x,y) == Chess.wPawn:
                    whiteEvaluation = whiteEvaluation + 4
                if b.get(x,y) == Chess.bPawn:
                    blackEvaluation = blackEvaluation + 4
            if x > 3 and x < 8:
                if b.get(x,y) == Chess.wBishop or b.get(x,y) == Chess.wKnight or b.get(x,y) == Chess.wRook or b.get(x,y) == Chess.wQueen:
                    whiteEvaluation = whiteEvaluation + 2
                elif b.get(x,y) == Chess.bBishop or b.get(x,y) == Chess.bKnight or b.get(x,y) == Chess.bRook or b.get(x,y) == Chess.bQueen:
                    blackEvaluation =  blackEvaluation + 2
            if x > 4 and x < 7:
                if b.get(x,y) == Chess.wPawn:
                    whiteEvaluation = whiteEvaluation + 1
                if b.get(x,y) == Chess.bPawn:
                    blackEvaluation = blackEvaluation + 1          
    return blackEvaluation - whiteEvaluation
#Method that will return the best moves that the engine can find. Will search varying depths depending on the difficulty level that is passed as a paramter. 
def getBestMove(b, difficulty):
    pieceR, pieceF, enP, blackQC, blackKC, whiteQC, whiteKC, whiteKCH, blackKCH = (Chess.getPieceRank(), Chess.getPieceFile(),Chess.getEnPassant(), Chess.getBlackQueenCastle(),Chess.getBlackKingCastle(), Chess.getWhiteQueenCastle(), Chess.getWhiteKingCastle(), Chess.getWhiteKingCheck(), Chess.getBlackKingCheck())
    legalMoves = []
    global results
    results = []
    toReturn = [0 for x in range(4)]
    threads = []
    depth = 2
    if difficulty == "LEVEL1":
        depth = 1
    for x in range(2,10):
        for y in range(2,10):
            if Chess.isBlack(b.get(x,y)):
                Chess.setValues(pieceR, pieceF, enP, blackQC, blackKC, whiteQC, whiteKC, whiteKCH, blackKCH)
                legalMoves = Chess.getLegalMoves(b, x, y, True)
                
                #Create a thread to search each move. 
                for i in legalMoves:
                        myThread = Thread(target = getWorstOutcome, args= (b, i, x,y, 0, depth))
                        myThread.start()
                        threads.append(myThread)
                    
    for x in threads:
        x.join()
    #Threads hace completed. Decide whether to search deeper using alpha-beta pruning or just return current best move.
    tempResults = copy.deepcopy(results)
    if difficulty == "LEVEL2" or difficulty == "LEVEL1":
        highest = -999999
        index = 0
        x = 0

        #Search for the move with the highest evaulation and return it. Depth here is 1 or 2. The goal is to find the move with the best worst possible outcome.
        while(x < len(results)):
                if results[x] > highest:
                    highest = results[x]
                    index = x
                x = x + 6
        if len(results) > 1:
            toReturn[0] = tempResults[index + 3]
            toReturn[1] = tempResults[index + 1]
            toReturn[2] = tempResults [index + 2]
            toReturn[3] = tempResults[index]

    elif not difficulty == "LEVEL1":
        depth = 1
        movesToSearch = 14
        if difficulty == "LEVEL4" or difficulty == "LEVEL5":
            depth = 2
        threads = []
        fiveBestMoves = []

        #Here we are finding the top 14 moves and searching them deeper. Depth here is 3 or 4. 
        for x in range(movesToSearch):
            highest = -999999
            index = 0
            count = 0
            while count < len(tempResults):
                if tempResults[count] > highest and tempResults[count + 1] > 0:
                    highest = tempResults[count]
                    index = count
                count = count + 6
            
            if highest >= 9999:
                toReturn[0] = tempResults[index + 3]
                toReturn[1] = tempResults[index + 1]
                toReturn[2] = tempResults [index + 2]
                toReturn[3] = tempResults[index]
                return toReturn
            
            if len(tempResults) > 1:
                tempResults[index+1] = tempResults[index+1] * -1
                fiveBestMoves.append(tempResults[index])
                fiveBestMoves.append(tempResults[index+1] * -1)
                fiveBestMoves.append(tempResults[index+2])
                fiveBestMoves.append(tempResults[index+3])
                fiveBestMoves.append(tempResults[index+4])
                fiveBestMoves.append(tempResults[index+5])

        tempResults = copy.deepcopy(results)
        count = 0
        while count < len(fiveBestMoves):
            for x in range(2,10):
                for y in range(2,10):
                    if fiveBestMoves[count+4] != None and Chess.isBlack(fiveBestMoves[count+4].get(x,y)):
                        Chess.setValues(pieceR, pieceF, enP, blackQC, blackKC, whiteQC, whiteKC, whiteKCH, blackKCH)
                        legalMoves = Chess.getLegalMoves(fiveBestMoves[count+4], x , y, True)
                        for i in legalMoves:
                                myThread = Thread (target= getWorstOutcome(fiveBestMoves[count + 4], i, x, y, count, depth))
                                myThread.start()
                                threads.append(myThread)     
            count = count + 6
        
        for x in threads:
            x.join()
        if (difficulty == "LEVEL5"):
            movesToSearch = 5
            depth = 2
            threads = []
            fiveBestMoves2 = []
            tempBestMoves = copy.deepcopy(fiveBestMoves)
            tempResults2 = copy.deepcopy(results)

            #Selecting the top 5 moves and searching them even deeper. Depth is now 6.
            for x in range(movesToSearch):
                highest = -999999
                index = 0
                count = len(tempResults)
                while count < len(tempResults2):
                    if tempResults2[count] > highest and tempResults2[count + 1] > 0:
                        highest = tempResults2[count]
                        index = count
                    count = count + 6
                if highest >= 9999:
                    index = tempResults2[index + 5]
                    index = fiveBestMoves[index + 5]
                    toReturn[0] = tempResults2[index + 3]
                    toReturn[1] = tempResults2[index + 1]
                    toReturn[2] = tempResults2 [index + 2]
                    toReturn[3] = tempResults2[index]
                    return toReturn
                if len(tempResults2) > 1:
                    tempResults2[index + 1] = tempResults2[index + 1] * -1
                    fiveBestMoves2.append(tempResults2[index])
                    fiveBestMoves2.append(tempResults2[index+1] * -1)
                    fiveBestMoves2.append(tempResults2[index+2])
                    fiveBestMoves2.append(tempResults2[index+3])
                    fiveBestMoves2.append(tempResults2[index+4])
                    fiveBestMoves2.append(tempResults2[index+5])
            tempResults = copy.deepcopy(results)
            count = 0
            while count < len(fiveBestMoves2):
                for x in range(2,10):
                    for y in range(2,10):
                        if fiveBestMoves2[count+4] != None and Chess.isBlack(fiveBestMoves2[count+4].get(x,y)):
                            Chess.setValues(pieceR, pieceF, enP, blackQC, blackKC, whiteQC, whiteKC, whiteKCH, blackKCH)
                            legalMoves = Chess.getLegalMoves(fiveBestMoves2[count+4], x , y, True)
                            for i in legalMoves:
                                    myThread = Thread (target= getWorstOutcome(fiveBestMoves2[count + 4], i, x, y, count, depth))
                                    myThread.start()
                                    threads.append(myThread)     
                count = count + 6
            
            for x in threads:
                x.join()
            highest = -999999
            index = 0
            x = len(tempResults)
            while(x < len(results)):
                    if results[x] > highest:
                        highest = results[x]
                        index = x
                    x = x + 6
            if len(results) > 1:
                index = results[index + 5]
                index = fiveBestMoves2[index+5]
                if len(results) > 1:
                    toReturn[0] = fiveBestMoves[index + 3]
                    toReturn[1] = fiveBestMoves[index + 1]
                    toReturn[2] = fiveBestMoves [index + 2]
                    toReturn[3] = fiveBestMoves[index]
        
            Chess.setValues(pieceR, pieceF, enP, blackQC, blackKC, whiteQC, whiteKC, whiteKCH, blackKCH)
            return toReturn
        highest = -999999
        index = 0
        x = len(tempResults)
        while(x < len(results)):
                if results[x] > highest:
                    highest = results[x]
                    index = x
                x = x + 6
        if len(results) > 1:
            index = results[index + 5]
            if len(fiveBestMoves) > 1:
                toReturn[0] = fiveBestMoves[index + 3]
                toReturn[1] = fiveBestMoves[index + 1]
                toReturn[2] = fiveBestMoves [index + 2]
                toReturn[3] = fiveBestMoves[index]
    
    Chess.setValues(pieceR, pieceF, enP, blackQC, blackKC, whiteQC, whiteKC, whiteKCH, blackKCH)
   
    return toReturn

#In order to find the best moves at certain depths, we also have to assume that the opponent is going to be making the best moves. 
#The goal is to minimize the losses while maximizing the gains. 
#Return worst possible outcome for each move.
def getWorstOutcome(b, i,x,y, parentMoveNumber, depth):
    lowest = 99999
    global results
    global highest
    toReturn = [0 for x in range(6)]
    arr = [[0 for x in range(12)] for y in range(12)]
    boardFirstSearch = Board(arr)
    tempBoard = None
    for num1 in range(0,12):
        for num2 in range(0,12):
            boardFirstSearch.set(num1,num2,b.get(num1,num2))
    moveRank = Chess.convertRanks(i)
    moveFile = Chess.convertFiles(i)  
    Chess.move(boardFirstSearch, x, y, moveRank, moveFile, True)
    if depth == 2 or depth == 3:
        for num3 in range(2,10):
            for num4 in range(2,10):
                if Chess.isWhite(boardFirstSearch.get(num3,num4)):
                    legalMoves = Chess.getLegalMoves(boardFirstSearch, num3, num4, True)
                    if len(legalMoves) < 1:
                        blackMoves = Chess.getAllMoves(boardFirstSearch,"BLACK",False)
                        if Chess.kingLocation(boardFirstSearch, "WHITE") in blackMoves: 
                            whiteMoves = Chess.getAllMoves(boardFirstSearch, "WHITE", True)
                            if len(whiteMoves) < 1:
                                    lowest = 9999
                    for j in legalMoves:
                        arr = [[0 for x in range(12)] for y in range(12)]
                        boardSecondSearch = Board(arr)
                        for num5 in range(0,12):
                            for num6 in range(0,12):
                                boardSecondSearch.set(num5, num6, boardFirstSearch.get(num5,num6))
                        moveRank = Chess.convertRanks(j)
                        moveFile = Chess.convertFiles(j)  
                        Chess.move(boardSecondSearch, num3, num4, moveRank, moveFile, True) 
                        if depth == 2:
                            evaluate = staticEvaluationFunction(boardSecondSearch, "BLACK")
                            if evaluate < lowest:
                                lowest = evaluate
                                tempBoard = boardSecondSearch
                        elif(depth == 3):
                            for num7 in range(2,10):
                                for num8 in range(2,10):
                                    if Chess.isWhite(boardSecondSearch.get(num7,num8)):
                                        legalMoves = Chess.getLegalMoves(boardSecondSearch, num7, num8, True)
                                        for z in legalMoves:
                                            arr = [[0 for x in range(12)] for y in range(12)]
                                            boardThirdSearch = Board(arr)
                                            for num9 in range(0,12):
                                                for num10 in range(0,12):
                                                    boardThirdSearch.set(num9, num10, boardSecondSearch.get(num9,num10))
                                            moveRank = Chess.convertRanks(z)
                                            moveFile = Chess.convertFiles(z)  
                                            Chess.move(boardThirdSearch, num7, num8, moveRank, moveFile, True) 
                                            evaluate = staticEvaluationFunction(boardThirdSearch, "WHITE")
                                            if evaluate < lowest:
                                                lowest = evaluate
                                                tempBoard = boardThirdSearch
                                        if lowest > highest:
                                            highest = lowest
                        else:       
                            break
        if lowest == 99999:
            lowest = staticEvaluationFunction(boardFirstSearch, "BLACK")
        toReturn[0] = lowest
        toReturn[1] = x
        toReturn[2] = y
        toReturn[3] = i
        toReturn[4] = tempBoard
        toReturn[5] = parentMoveNumber
        results = results + toReturn
    else:
        evaluate = staticEvaluationFunction(boardFirstSearch, "WHITE")
        toReturn[0] = evaluate
        toReturn[1] = x
        toReturn[2] = y
        toReturn[3] = i
        toReturn[4] = boardFirstSearch
        toReturn[5] = parentMoveNumber
        results = results + toReturn
    

