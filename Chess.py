from Board import Board
from tkinter import *
from PIL import ImageTk, Image
import sys
import Engine
sys.setrecursionlimit(1500)

#Using numbers to represent pieces and board indexes. 
offBoard, freeSpace, wPawn, wKnight, wBishop, wRook, wQueen, wKing, bPawn, bKnight, bBishop, bRook, bQueen, bKing = (-1, 0,1,2,3,4,5,6, 7, 8, 9, 10, 11, 12) 
A1, A2, A3, A4, A5, A6, A7, A8 = range(2,10)
B1, B2, B3, B4, B5, B6, B7, B8 = range(10,18)
C1, C2, C3, C4, C5, C6, C7, C8 = range(18,26)
D1, D2, D3, D4, D5, D6, D7, D8 = range(26,34)
E1, E2, E3, E4, E5, E6, E7, E8 = range(34,42)
F1, F2, F3, F4, F5, F6, F7, F8 = range(42,50)
G1, G2, G3, G4, G5, G6, G7, G8 = range(50,58)
H1, H2, H3, H4, H5, H6, H7, H8 = range(58,66)
pieceRank = 0
pieceFile = 0
enPassant = 0
blackQueenCastle = True
blackKingCastle = True
whiteQueenCastle = True
whiteKingCastle = True
whiteKingCheck = False
blackKingCheck = False
difficulty = "LEVEL2"

#Getter/Setter Methods
def getPieceRank():
    return pieceRank
def getPieceFile():
    return pieceFile
def getEnPassant():
    return enPassant
def getBlackQueenCastle():
    return blackQueenCastle
def getBlackKingCastle():
    return blackKingCastle
def getWhiteQueenCastle():
    return whiteQueenCastle
def getWhiteKingCastle():
    return whiteKingCastle
def getWhiteKingCheck():
    return whiteKingCheck
def getBlackKingCheck():
    return blackKingCheck

def setValues(pieceR, pieceF, enP, blackQC, blackKC, whiteQC, whiteKC, whiteKCH, blackKCH):
    global pieceRank 
    global pieceFile 
    global enPassant 
    global blackQueenCastle 
    global blackKingCastle 
    global whiteQueenCastle 
    global whiteKingCastle 
    global whiteKingCheck 
    global blackKingCheck 
    pieceRank = pieceR
    pieceF = pieceF
    enPassant = enP
    blackQueenCastle = blackQC
    blackKingCastle = blackKC
    whiteQueenCastle = whiteQC
    whiteKingCastle =  whiteKC 
    whiteKingCheck = whiteKCH
    blackKingCheck = blackKCH

#Board object is a 2D integer array. We need to be able to represent this as two numbers (files and ranks) as well as one number (2 for A1, 3 for A2, ect.) for method returning purposes. 
def convertFilesRanks(ranks, files):
    return (9-ranks) + (files - 2) * 8 + 2

def convertFiles(boardIndex):
    files= 0
    if (boardIndex < 10):
        files  = 0
    elif (boardIndex < 18):
        files = 1
    elif (boardIndex < 26):
        files = 2
    elif (boardIndex < 34):
        files = 3
    elif (boardIndex < 42):
        files = 4
    elif (boardIndex < 50):
        files = 5
    elif (boardIndex < 58):
        files = 6
    else:
        files = 7
    return files + 2

def convertRanks(boardIndex):
    if (boardIndex >= 58):
       return 9 - (boardIndex - 58)
    elif (boardIndex >= 50):
       return 9 - (boardIndex - 50)
    elif (boardIndex >= 42):
        return 9 - (boardIndex - 42)
    elif (boardIndex >= 34):
        return 9 - (boardIndex - 34)
    elif (boardIndex >= 26):
        return 9 - (boardIndex - 26)
    elif (boardIndex >= 18):
        return 9 - (boardIndex - 18)
    elif (boardIndex >= 10):
        return 9 - (boardIndex - 10)
    else:
        return 9 - (boardIndex -2)
    
#Add pieces to the board depending on game mode.
def setUpGame(b, mode):
    if mode == "DEFAULT":
        b.setOffBoard()
        b.setPawns()
        b.setKings()
        b.setBishops()
        b.setKnights()
        b.setQueens()
        b.setRooks()
    elif mode == "PAWNSONLY":
        b.setOffBoard()
        b.setPawns()
        b.setKings()
    elif mode == "CHALLENGEMODE":
        b.setOffBoard()
        b.setKings()
        b.setQueens()
       
        for x in range(2, 10):
            b.set(3,x, bQueen)
            b.set(8,x, wQueen)
        b.set(4, 2, bQueen)	
        b.set(4, 9, bQueen)
    elif mode == "KNIGHTS":
        b.setOffBoard()
        b.setKings()
        b.setKnights()	
        for x in range(2, 10):
            b.set(3,x, bKnight)
            b.set(8,x, wKnight)
        b.set(2, 2, bKnight)
        b.set(2, 9, bKnight)
        b.set(9, 2, wKnight)
        b.set(9, 9, wKnight)
    elif mode == "CHECK1":
        b.setOffBoard()
        b.setKings()
        b.set(9,2,wRook)
    elif mode == "CHECK2":
        b.setOffBoard()
        b.setKings()
        b.set(9,2,wBishop)
        b.set(9,3,wKnight)
    else:
        b.setKings()
        b.setOffBoard()
        b.set(2, 2, bRook)
        b.set(3, 2, bRook)

#Moves a piece at startrank and startFile to new position. Needs to also consider edgecases such as castling, en passant, ect.
def move(b, startRank, startFile, endRank, endFile, bol):
    global enPassant
    global whiteKingCastle
    global whiteQueenCastle
    global blackQueenCastle
    global blackKingCastle
    global blackKingCheck
    global whiteKingCheck
    movedPawnTwo = False
    b.set(endRank, endFile,  b.get(startRank, startFile) )
    b.set(startRank, startFile, freeSpace)
    if bol:
        if blackKingCheck == True:
            blackKingCheck = False
        if whiteKingCheck == True:
            whiteKingCheck = False
        if (b.get(endRank, endFile) == wPawn):
            if startRank == 5 and endRank == 4 and startFile != endFile and enPassant == convertFilesRanks(startRank, endFile):
                b.set(startRank, endFile, freeSpace)
            elif startRank == 8 and endRank == 6:
                enPassant = convertFilesRanks(endRank, endFile)
                movedPawnTwo = True
            elif endRank == 2:
                b.set(endRank, endFile, wQueen)
        elif (b.get(endRank, endFile) == bPawn):
            if startRank == 6 and endRank == 7 and startFile != endFile and enPassant == convertFilesRanks(startRank, endFile):
                b.set(startRank, endFile, freeSpace)
            elif startRank == 3 and endRank == 5:
                enPassant = convertFilesRanks(endRank, endFile)
                movedPawnTwo = True
            elif endRank == 9:
                b.set(endRank, endFile, bQueen)
        elif b.get(endRank, endFile) == wKing:
            if (startFile == 6 and endFile == 8):
                b.set(9, 9, freeSpace)
                b.set(9, 7, wRook)
            elif (startFile == 6 and endFile == 4):
                b.set(9, 2, freeSpace)
                b.set(9, 5, wRook)
            whiteKingCastle = False
            whiteQueenCastle = False
        elif b.get(endRank, endFile) == bKing:
            if (startFile == 6 and endFile == 8):
                b.set(2, 9, freeSpace)
                b.set(2, 7, bRook)
            elif (startFile == 6 and endFile == 4):
                b.set(2, 2, freeSpace)
                b.set(2, 5, bRook)
            blackKingCastle = False
            blackQueenCastle = False
        elif(b.get(endRank, endFile) == wRook):
            if (whiteKingCastle or whiteQueenCastle):
                if startFile == 9:
                    whiteKingCastle = False
                elif startFile == 2:
                    whiteQueenCastle = False
        elif(b.get(endRank, endFile) == bRook):
            if (blackKingCastle or blackQueenCastle):
                if startFile == 9:
                    blackKingCastle = False
                elif startFile == 2:
                    blackQueenCastle = False
        if not movedPawnTwo:
            enPassant = 0

#Returns true if index is a white piece.
def isWhite(piece):
    for x in range(1,7):
        if x == piece:
         return True
    return False

#Returns true if index is a black piece.
def isBlack(piece):
    for x in range(7,13):
        if x == piece:
            return True
    return False

#Find all legal pawn moves and add them to array.
def pawnMoves(b, ranks, files):
    legalMoves = []
    global enPassant
    if (b.get(ranks,files) == wPawn):
        if (ranks == 8):
            if (b.get(ranks-2,files) == freeSpace and b.get(ranks-1,files) == freeSpace):
             legalMoves.append(convertFilesRanks(ranks-2,files))
        if (ranks == 5):
            if (b.get(ranks, files + 1) == bPawn and enPassant == convertFilesRanks(ranks, files + 1)):
                if (b.get(ranks-1, files + 1) == freeSpace):
                    legalMoves.append(convertFilesRanks(ranks-1, files + 1))
            if (b.get(ranks, files - 1) == bPawn and enPassant == convertFilesRanks(ranks, files -1)):
                if (b.get(ranks-1, files - 1) == freeSpace):
                    legalMoves.append(convertFilesRanks(ranks-1, files -1))
        if (b.get(ranks-1,files) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks-1,files))
        if (isBlack(b.get(ranks-1, files + 1))):
             legalMoves.append(convertFilesRanks(ranks-1,files+1))
        if (isBlack(b.get(ranks-1, files - 1))):
            legalMoves.append(convertFilesRanks(ranks-1,files-1))
    elif (b.get(ranks,files) == bPawn):
        if (ranks == 3):
            if (b.get(ranks+2,files) == freeSpace and b.get(ranks+1,files) == freeSpace):
                 legalMoves.append(convertFilesRanks(ranks+2,files))
        if ranks == 6:
            if (b.get(ranks, files + 1) == wPawn and enPassant == convertFilesRanks(ranks, files + 1)):
                if (b.get(ranks+1, files + 1) == freeSpace):
                    legalMoves.append(convertFilesRanks(ranks+1, files + 1))
            if (b.get(ranks, files - 1) == wPawn and enPassant == convertFilesRanks(ranks, files -1)):
                if (b.get(ranks+1, files - 1) == freeSpace):
                    legalMoves.append(convertFilesRanks(ranks+1, files -1))
        if (b.get(ranks+1,files) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks+1,files))
        if (isWhite(b.get(ranks+1, files + 1))):
             legalMoves.append(convertFilesRanks(ranks+1,files+1))
        if (isWhite(b.get(ranks+1, files - 1))):
            legalMoves.append(convertFilesRanks(ranks+1,files-1))
    return legalMoves

#Find all legal knight moves and add them to array.
def knightMoves(b, ranks, files):
    legalMoves = []
    if (b.get(ranks,files) == wKnight):
        if (b.get(ranks+2,files + 1) == freeSpace or isBlack(b.get(ranks+2,files + 1)) ):
                 legalMoves.append(convertFilesRanks(ranks+2,files + 1))
        if (b.get(ranks-2,files + 1) == freeSpace or isBlack(b.get(ranks-2,files + 1)) ):
                 legalMoves.append(convertFilesRanks(ranks-2,files + 1))
        if (b.get(ranks-2,files - 1) == freeSpace or isBlack(b.get(ranks-2,files - 1))):
                 legalMoves.append(convertFilesRanks(ranks-2,files - 1))
        if (b.get(ranks+2,files - 1) == freeSpace or isBlack(b.get(ranks+2,files - 1)) ):
                 legalMoves.append(convertFilesRanks(ranks+2,files -1))
        if (b.get(ranks+1,files + 2) == freeSpace or isBlack(b.get(ranks+1,files + 2)) ):
                 legalMoves.append(convertFilesRanks(ranks+1,files + 2))
        if (b.get(ranks-1,files + 2) == freeSpace or isBlack(b.get(ranks-1,files + 2)) ):
                 legalMoves.append(convertFilesRanks(ranks-1,files + 2))
        if (b.get(ranks-1,files - 2) == freeSpace or isBlack(b.get(ranks-1,files - 2))):
                 legalMoves.append(convertFilesRanks(ranks-1,files - 2))
        if (b.get(ranks+1,files - 2) == freeSpace or isBlack(b.get(ranks+1,files - 2)) ):
                legalMoves.append(convertFilesRanks(ranks+1,files - 2))
    elif (b.get(ranks,files) == bKnight):
        if (b.get(ranks+2,files + 1) == freeSpace or isWhite(b.get(ranks+2,files + 1)) ):
                 legalMoves.append(convertFilesRanks(ranks+2,files + 1))
        if (b.get(ranks-2,files + 1) == freeSpace or isWhite(b.get(ranks-2,files + 1)) ):
                 legalMoves.append(convertFilesRanks(ranks-2,files + 1))
        if (b.get(ranks-2,files - 1) == freeSpace or isWhite(b.get(ranks-2,files - 1))):
                 legalMoves.append(convertFilesRanks(ranks-2,files - 1))
        if (b.get(ranks+2,files - 1) == freeSpace or isWhite(b.get(ranks+2,files - 1)) ):
                 legalMoves.append(convertFilesRanks(ranks+2,files -1))
        if (b.get(ranks+1,files + 2) == freeSpace or isWhite(b.get(ranks+1,files + 2)) ):
                 legalMoves.append(convertFilesRanks(ranks+1,files + 2))
        if (b.get(ranks-1,files + 2) == freeSpace or isWhite(b.get(ranks-1,files + 2)) ):
                 legalMoves.append(convertFilesRanks(ranks-1,files + 2))
        if (b.get(ranks-1,files - 2) == freeSpace or isWhite(b.get(ranks-1,files - 2))):
                 legalMoves.append(convertFilesRanks(ranks-1,files - 2))
        if (b.get(ranks+1,files - 2) == freeSpace or isWhite(b.get(ranks+1,files - 2)) ):
                legalMoves.append(convertFilesRanks(ranks+1,files - 2))
    return legalMoves
    
#Find all legal bishop moves and add them to array.
def bishopMoves(b, ranks, files):
    legalMoves = []
    if (b.get(ranks,files) == wBishop):
        count = 1
        while(b.get(ranks+ count, files+ count) != offBoard and not isWhite(b.get(ranks + count, files+ count))):
            if (b.get(ranks + count, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
            elif (isBlack(b.get(ranks + count, files + count))):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks + count, files + count) != offBoard and not  isWhite(b.get(ranks + count, files+ count))):
            if (b.get(ranks + count, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
            elif (isBlack(b.get(ranks + count, files + count))):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
                break
            count = count - 1
        count = 1
        while(b.get(ranks + count, files - count) != offBoard and not isWhite(b.get(ranks + count, files -count))):
            if (b.get(ranks + count, files - count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
            elif (isBlack(b.get(ranks + count, files - count))):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks+ count, files- count) != offBoard and not isWhite(b.get(ranks + count, files- count))):
            if (b.get(ranks + count, files - count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
            elif (isBlack(b.get(ranks + count, files - count))):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
                break
            count = count - 1
    elif (b.get(ranks,files) == bBishop):
        count = 1
        while(b.get(ranks+ count, files+ count) != offBoard and not isBlack(b.get(ranks + count, files+ count))):
            if (b.get(ranks + count, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
            elif (isWhite(b.get(ranks + count, files + count))):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks + count, files + count) != offBoard and not isBlack(b.get(ranks + count, files+ count))):
            if (b.get(ranks + count, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
            elif (isWhite(b.get(ranks + count, files + count))):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
                break
            count = count - 1
        count = 1
        while(b.get(ranks + count, files - count) != offBoard and not isBlack(b.get(ranks + count, files -count))):
            if (b.get(ranks + count, files - count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
            elif (isWhite(b.get(ranks + count, files - count))):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks+ count, files- count) != offBoard and not isBlack(b.get(ranks + count, files- count))):
            if (b.get(ranks + count, files - count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
            elif (isWhite(b.get(ranks + count, files - count))):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
                break
            count = count - 1
        
    return legalMoves

#Find all legal rook moves and add them to array.             
def rookMoves(b, ranks, files):
    legalMoves = []
    if (b.get(ranks,files) == wRook):
        count = 1
        while(b.get(ranks+ count, files) != offBoard and not isWhite(b.get(ranks + count, files))):
            if (b.get(ranks + count, files) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files))
            elif (isBlack(b.get(ranks + count, files))):
                legalMoves.append(convertFilesRanks(ranks+count,files))
                break
            count = count + 1
        count = -1
        while(b.get(ranks+ count, files) != offBoard and not isWhite(b.get(ranks + count, files))):
            if (b.get(ranks + count, files) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files))
            elif (isBlack(b.get(ranks + count, files))):
                legalMoves.append(convertFilesRanks(ranks+count,files))
                break
            count = count - 1
        count = 1
        while(b.get(ranks, files+ count) != offBoard and not isWhite(b.get(ranks, files+ count))):
            if (b.get(ranks, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
            elif (isBlack(b.get(ranks, files+ count))):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks, files+ count) != offBoard and not isWhite(b.get(ranks, files+ count))):
            if (b.get(ranks, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
            elif (isBlack(b.get(ranks, files+ count))):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
                break
            count = count - 1
    if (b.get(ranks,files) == bRook):
        count = 1
        while(b.get(ranks+ count, files) != offBoard and not isBlack(b.get(ranks + count, files))):
            if (b.get(ranks + count, files) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files))
            elif (isWhite(b.get(ranks + count, files))):
                legalMoves.append(convertFilesRanks(ranks+count,files))
                break
            count = count + 1
        count = -1
        while(b.get(ranks+ count, files) != offBoard and not isBlack(b.get(ranks + count, files))):
            if (b.get(ranks + count, files) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files))
            elif (isWhite(b.get(ranks + count, files))):
                legalMoves.append(convertFilesRanks(ranks+count,files))
                break
            count = count - 1
        count = 1
        while(b.get(ranks, files+ count) != offBoard and not isBlack(b.get(ranks, files+ count))):
            if (b.get(ranks, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
            elif (isWhite(b.get(ranks, files+ count))):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks, files+ count) != offBoard and not isBlack(b.get(ranks, files+ count))):
            if (b.get(ranks, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
            elif (isWhite(b.get(ranks, files+ count))):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
                break
            count = count - 1
    return legalMoves
    
#Find all legal queen moves and add them to array.
def queenMoves(b, ranks, files):
    legalMoves = []
    if (b.get(ranks,files) == wQueen):
        count = 1
        while(b.get(ranks+ count, files) != offBoard and not isWhite(b.get(ranks + count, files))):
            if (b.get(ranks + count, files) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files))
            elif (isBlack(b.get(ranks + count, files))):
                legalMoves.append(convertFilesRanks(ranks+count,files))
                break
            count = count + 1
        count = -1
        while(b.get(ranks+ count, files) != offBoard and not isWhite(b.get(ranks + count, files))):
            if (b.get(ranks + count, files) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files))
            elif (isBlack(b.get(ranks + count, files))):
                legalMoves.append(convertFilesRanks(ranks+count,files))
                break
            count = count - 1
        count = 1
        while(b.get(ranks, files+ count) != offBoard and not isWhite(b.get(ranks, files+ count))):
            if (b.get(ranks, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
            elif (isBlack(b.get(ranks, files+ count))):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks, files+ count) != offBoard and not isWhite(b.get(ranks, files+ count))):
            if (b.get(ranks, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
            elif (isBlack(b.get(ranks, files+ count))):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
                break
            count = count - 1
        count = 1
        while(b.get(ranks+ count, files+ count) != offBoard and not isWhite(b.get(ranks + count, files+ count))):
            if (b.get(ranks + count, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
            elif (isBlack(b.get(ranks + count, files + count))):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks + count, files + count) != offBoard and not  isWhite(b.get(ranks + count, files+ count))):
            if (b.get(ranks + count, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
            elif (isBlack(b.get(ranks + count, files + count))):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
                break
            count = count - 1
        count = 1
        while(b.get(ranks + count, files - count) != offBoard and not isWhite(b.get(ranks + count, files -count))):
            if (b.get(ranks + count, files - count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
            elif (isBlack(b.get(ranks + count, files - count))):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks+ count, files- count) != offBoard and not isWhite(b.get(ranks + count, files- count))):
            if (b.get(ranks + count, files - count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
            elif (isBlack(b.get(ranks + count, files - count))):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
                break
            count = count - 1
    if (b.get(ranks,files) == bQueen):
        count = 1
        while(b.get(ranks+ count, files) != offBoard and not isBlack(b.get(ranks + count, files))):
            if (b.get(ranks + count, files) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files))
            elif (isWhite(b.get(ranks + count, files))):
                legalMoves.append(convertFilesRanks(ranks+count,files))
                break
            count = count + 1
        count = -1
        while(b.get(ranks+ count, files) != offBoard and not isBlack(b.get(ranks + count, files))):
            if (b.get(ranks + count, files) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files))
            if (isWhite(b.get(ranks + count, files))):
                legalMoves.append(convertFilesRanks(ranks+count,files))
                break
            count = count - 1
        count = 1
        while(b.get(ranks, files+ count) != offBoard and not isBlack(b.get(ranks, files+ count))):
            if (b.get(ranks, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
            elif (isWhite(b.get(ranks, files+ count))):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks, files+ count) != offBoard and not isBlack(b.get(ranks, files+ count))):
            if (b.get(ranks, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
            elif (isWhite(b.get(ranks, files+ count))):
                legalMoves.append(convertFilesRanks(ranks,files+ count))
                break
            count = count - 1
        count = 1
        while(b.get(ranks+ count, files+ count) != offBoard and not isBlack(b.get(ranks + count, files+ count))):
            if (b.get(ranks + count, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
            elif (isWhite(b.get(ranks + count, files + count))):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks + count, files + count) != offBoard and not isBlack(b.get(ranks + count, files+ count))):
            if (b.get(ranks + count, files + count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
            elif (isWhite(b.get(ranks + count, files + count))):
                legalMoves.append(convertFilesRanks(ranks+count,files+count))
                break
            count = count - 1
        count = 1
        while(b.get(ranks + count, files - count) != offBoard and not isBlack(b.get(ranks + count, files -count))):
            if (b.get(ranks + count, files - count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
            elif (isWhite(b.get(ranks + count, files - count))):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
                break
            count = count + 1
        count = -1
        while(b.get(ranks+ count, files- count) != offBoard and not isBlack(b.get(ranks + count, files- count))):
            if (b.get(ranks + count, files - count) == freeSpace):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
            elif (isWhite(b.get(ranks + count, files - count))):
                legalMoves.append(convertFilesRanks(ranks+count,files-count))
                break
            count = count - 1
    return legalMoves

#Find all legal king moves and add them to array.
def kingMoves(b, ranks, files, includeCastle):
    legalMoves = []
    if (b.get(ranks,files) == wKing):
        if (includeCastle and not whiteKingCheck):
            if whiteQueenCastle == True:
                if b.get(9, 3) == freeSpace and b.get(9,4) == freeSpace and b.get(9,5) == freeSpace and b.get(9,2) == wRook:
                    allMoves = getAllMoves(b, "BLACK", False)
                    if not (convertFilesRanks(9,4) in allMoves or convertFilesRanks(9,5) in allMoves):
                        legalMoves.append(convertFilesRanks(ranks, files - 2))
            if whiteKingCastle == True:
                if b.get(9, 7) == freeSpace and b.get(9,8) == freeSpace and b.get(9,9) == wRook:
                    allMoves = getAllMoves(b, "BLACK", False)
                    if not (convertFilesRanks(9,7) in allMoves or convertFilesRanks(9,8) in allMoves):
                        legalMoves.append(convertFilesRanks(ranks, files +2))
        count = 1
        if (b.get(ranks + count, files) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks+count,files))
        elif (isBlack(b.get(ranks + count, files))):
            piece = b.get(ranks + count, files)
            b.set(ranks + count, files,freeSpace)
            legalMoves.append(convertFilesRanks(ranks+count,files))
            b.set(ranks + count, files,piece)
        count = -1
        if (b.get(ranks + count, files) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks+count,files))
        elif (isBlack(b.get(ranks + count, files))):
            piece = b.get(ranks + count, files)
            b.set(ranks + count, files,freeSpace)
            legalMoves.append(convertFilesRanks(ranks+count,files))
            b.set(ranks + count, files,piece)
        count = 1
        if (b.get(ranks, files + count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks,files + count))
        elif (isBlack(b.get(ranks, files+count))):
            piece = b.get(ranks, files+count)
            b.set(ranks, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks,files+count))
            b.set(ranks, files+count,piece)
        count = -1
        if (b.get(ranks, files+count) == freeSpace ):
            legalMoves.append(convertFilesRanks(ranks,files+count))
        elif (isBlack(b.get(ranks, files+count))):
            piece = b.get(ranks, files+count)
            b.set(ranks, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks,files+count))
            b.set(ranks, files+count,piece)
        count = 1
        if (b.get(ranks+count, files + count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks+count,files+count))
        elif (isBlack(b.get(ranks+count, files+count))):
            piece = b.get(ranks+count, files+count)
            b.set(ranks + count, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks+count,files+count))
            b.set(ranks+count, files+count,piece)
        count = -1
        if (b.get(ranks+count, files+count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks + count,files+count))
        elif (isBlack(b.get(ranks+count, files+count))):
            piece = b.get(ranks+count, files+count)
            b.set(ranks+count, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks+count,files+count))
            b.set(ranks+count, files+count,piece)
        count = 1
        if (b.get(ranks-count, files + count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks-count,files+count))
        elif (isBlack(b.get(ranks-count, files+count))):
            piece = b.get(ranks-count, files+count)
            b.set(ranks- count, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks-count,files+count))
            b.set(ranks-count, files+count,piece)
        count = -1
        if (b.get(ranks-count, files+count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks- count,files+count))
        elif (isBlack(b.get(ranks-count, files+count))):
            piece = b.get(ranks-count, files+count)
            b.set(ranks-count, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks-count,files+count))
            b.set(ranks-count, files+count,piece)
    elif (b.get(ranks,files) == bKing):
        if (includeCastle and not blackKingCheck):
            if blackQueenCastle == True:
                    if b.get(2, 3) == freeSpace and b.get(2,4) == freeSpace and b.get(2,5) == freeSpace and b.get(2,2) == bRook:
                        allMoves = getAllMoves(b, "WHITE", False)
                        if not (convertFilesRanks(2,4) in allMoves or convertFilesRanks(2,5) in allMoves):
                            legalMoves.append(convertFilesRanks(ranks, files - 2))
            if blackKingCastle == True:
                if b.get(2, 7) == freeSpace and b.get(2,8) == freeSpace and b.get(2,9) == bRook:
                    allMoves = getAllMoves(b, "WHITE", False)
                    if not (convertFilesRanks(2,7) in allMoves or convertFilesRanks(2,8) in allMoves):
                        legalMoves.append(convertFilesRanks(ranks, files +2))
        count = 1
        if (b.get(ranks + count, files) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks+count,files))
        elif (isWhite(b.get(ranks + count, files))):
            piece = b.get(ranks + count, files)
            b.set(ranks + count, files,freeSpace)
            legalMoves.append(convertFilesRanks(ranks+count,files))
            b.set(ranks + count, files,piece)
        count = -1
        if (b.get(ranks + count, files) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks+count,files))
        elif (isWhite(b.get(ranks + count, files))):
            piece = b.get(ranks + count, files)
            b.set(ranks + count, files,freeSpace)
            legalMoves.append(convertFilesRanks(ranks+count,files))
            b.set(ranks + count, files,piece)
        count = 1
        if (b.get(ranks, files + count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks,files + count))
        elif (isWhite(b.get(ranks, files+count))):
            piece = b.get(ranks, files+count)
            b.set(ranks, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks,files+count))
            b.set(ranks, files+count,piece)
        count = -1
        if (b.get(ranks, files+count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks,files+count))
        elif (isWhite(b.get(ranks, files+count))):
            piece = b.get(ranks, files+count)
            b.set(ranks, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks,files+count))
            b.set(ranks, files+count,piece)
        count = 1
        if (b.get(ranks+count, files + count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks+count,files+count))
        elif (isWhite(b.get(ranks+count, files+count))):
            piece = b.get(ranks+count, files+count)
            b.set(ranks + count, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks+count,files+count))
            b.set(ranks+count, files+count,piece)
        count = -1
        if (b.get(ranks+count, files+count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks+ count,files+count))
        elif (isWhite(b.get(ranks+count, files+count))):
            piece = b.get(ranks+count, files+count)
            b.set(ranks+count, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks+count,files+count))
            b.set(ranks+count, files+count,piece)
        count = 1
        if (b.get(ranks-count, files + count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks-count,files+count))
        elif (isWhite(b.get(ranks-count, files+count))):
            piece = b.get(ranks-count, files+count)
            b.set(ranks-count, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks-count,files+count))
            b.set(ranks-count, files+count,piece)
        count = -1
        if (b.get(ranks-count, files+count) == freeSpace):
            legalMoves.append(convertFilesRanks(ranks-count,files+count))
        elif (isWhite(b.get(ranks-count, files+count))):
            piece = b.get(ranks-count, files+count)
            b.set(ranks-count, files+count,freeSpace)
            legalMoves.append(convertFilesRanks(ranks-count,files+count))
            b.set(ranks-count, files+count,piece)
    return legalMoves

#If there is not enough pieces on the board that can eventually deliver a checkmate, return true. 
def insufficientMaterial(b):
    wBishopCount = 0
    wKnightCount = 0
    bBishopCount = 0
    bKnightCount = 0
    for x in range(2,10):
        for y in range(2,10):
            piece = b.get(x,y)
            if (piece == wPawn or piece == bPawn or piece == wRook or piece == bRook or piece == wQueen or piece == bQueen):
                return False
            if (piece == wBishop):
                wBishopCount = wBishopCount + 1
            elif (piece == bBishop):
                bBishopCount = bBishopCount + 1
            elif (piece == wKnight):
                wKnightCount = wKnightCount + 1
            elif (piece == bKnight):
                bKnightCount = bKnightCount + 1
    if (wBishopCount > 1 or bBishopCount > 1):
        return False
    if (wBishopCount > 0 and wKnightCount > 0) or (bBishopCount > 0 and bKnightCount > 0) or wKnightCount > 2 or bKnightCount >2:
        return False
    return True

#Get all possible moves that either white or black can make.
def getAllMoves(b, color, bol):
    legalMoves = []
    if color == "WHITE":
        for x in range(2,10):
            for y in range(2,10):
                if isWhite(b.get(x,y)):
                    legalMoves += getLegalMoves(b, x, y, bol)
    elif color == "BLACK":
        for x in range(2,10):
            for y in range(2,10):
                if isBlack(b.get(x,y)):
                    legalMoves += getLegalMoves(b, x, y, bol)
    return legalMoves

#Returns the king location of the white or black king.
def kingLocation(b, color):
    if color == "WHITE":
        for x in range(2,10) :
            for y in range(2,10):
                if b.get(x,y) == wKing:
                    return convertFilesRanks(x,y)
    if color == "BLACK":
            for x in range(2,10) :
                for y in range(2,10):
                    if b.get(x,y) == bKing:
                        return convertFilesRanks(x,y)

#Moves are only legal if following each move, the players king is not in check. Remove all moves that to not meet this condition. If this returns an empty array, it's either checkmate or stalemate. 
def checkMoves(b, pieceRank, pieceFile, legalPieceMoves):
    legalMoves = []
    i = 0
    while (i < len(legalPieceMoves)):
        arr = [[0 for x in range(12)] for y in range(12)]
        tempBoard = Board(arr)
        for x in range(0,12):
            for y in range(0,12):
                tempBoard.set(x,y,b.get(x,y))
        moveRank = convertRanks(legalPieceMoves[i])
        moveFile = convertFiles(legalPieceMoves[i])
        move(tempBoard, pieceRank, pieceFile, moveRank, moveFile, False)
        if isWhite(tempBoard.get(moveRank, moveFile)):
            legalMoves = getAllMoves(tempBoard, "BLACK", False)
            if kingLocation(tempBoard, "WHITE") in legalMoves:
                legalPieceMoves.pop(i)
                i = i - 1
        elif isBlack(tempBoard.get(moveRank, moveFile)):
            legalMoves = getAllMoves(tempBoard, "WHITE", False)
            if kingLocation(tempBoard, "BLACK") in legalMoves:
                legalPieceMoves.pop(i)
                i = i -1 
        i = i + 1     

    return legalPieceMoves

#Gets all the legal moves that a specific piece can make. 
def getLegalMoves(b, ranks, files, bol):
    legalMoves = []
    if b.get(ranks,files) == 1 or b.get(ranks,files) == 7:
        legalMoves = pawnMoves(b,ranks,files)
    elif b.get(ranks,files) == 2 or b.get(ranks,files) == 8:
        legalMoves = knightMoves(b,ranks,files)
    elif b.get(ranks,files) == 3 or b.get(ranks,files) == 9:
        legalMoves = bishopMoves(b,ranks,files)
    elif b.get(ranks,files) == 4 or b.get(ranks,files) == 10:
        legalMoves = rookMoves(b,ranks,files)
    elif b.get(ranks,files) == 5 or b.get(ranks,files) == 11:
        legalMoves = queenMoves(b,ranks,files)
    elif b.get(ranks,files) == 6 or b.get(ranks,files) == 12:
        legalMoves = kingMoves(b,ranks,files, bol)
    if bol:
       legalMoves = checkMoves(b, ranks, files, legalMoves)
    return legalMoves

#Draws the chess board by using colored rectangles and by displaying piece images on the board.
def displayBoard(b, canvas, board, pieces, highlight, highlightMoves, firstTime):
    white = True
    count = 0
    while len(pieces) > 0:
        canvas.delete(pieces[0])
        pieces.pop(0)
    while len(highlight) > 0:
        canvas.delete(highlight[0])
        highlight.pop(0)
    if len(highlightMoves)>0:
        for x in range (len(highlightMoves)):
            canvas.delete(highlightMoves[0])
            highlightMoves.pop(0)
    board =  [[None for x in range(8)] for y in range(8)]
    if firstTime:
        for x in range(8):
            for y in range(8):
                    if (white):
                        board[x][y]= canvas.create_rectangle(0 , 0 , 75, 75, fill='burlywood')
                        white = False
                    else:
                        board[x][y] = canvas.create_rectangle(0, 0, 75, 75, fill='burlywood4')
                        white = True
                    if y == 7:
                        white = not white
        for x in range(8):
            for y in range(8):
                canvas.move(board[x][y],50 + 75 * y,  50 + 75 * x)
    for x in range(12):
        for y in range(12):
            if(b.get(x,y) == wPawn):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/whitePawn.png")))
                canvas.create_image(75 * (y-2) + 49, 75 * (x-2) + 50, anchor=NW, image=pieces[count]) 
                count = count + 1 
            elif(b.get(x,y)== bPawn):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/blackPawn.png")))
                canvas.create_image(75 * (y-2) + 50, 75 * (x-2) + 48, anchor=NW, image=pieces[count]) 
                count = count + 1 
            elif(b.get(x,y)== wRook):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/whiteRook.png")))
                canvas.create_image(75 * (y-2) + 54, 75 * (x-2) + 50, anchor=NW, image=pieces[count]) 
                count = count + 1 
            elif(b.get(x,y)== bRook):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/blackRook.png")))
                canvas.create_image(75 * (y-2) + 50, 75 * (x-2) + 48, anchor=NW, image=pieces[count]) 
                count = count + 1 
            elif(b.get(x,y)== wQueen):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/whiteQueen.png")))
                canvas.create_image(75 * (y-2) + 52, 75 * (x-2) + 52, anchor=NW, image=pieces[count]) 
                count = count + 1 
            elif(b.get(x,y)== bQueen):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/blackQueen.png")))
                canvas.create_image(75 * (y-2) + 46, 75 * (x-2) + 50, anchor=NW, image=pieces[count]) 
                count = count + 1 
            elif(b.get(x,y)== wKing):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/whiteKing.png")))
                canvas.create_image(75 * (y-2) + 48, 75 * (x-2) + 52, anchor=NW, image=pieces[count]) 
                count = count + 1 
            elif(b.get(x,y)== bKing):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/blackKing.png")))
                canvas.create_image(75 * (y-2) + 49, 75 * (x-2) + 48, anchor=NW, image=pieces[count]) 
                count = count + 1
            elif(b.get(x,y)== wKnight):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/whiteKnight.png")))
                canvas.create_image(75 * (y-2) + 54, 75 * (x-2) + 45, anchor=NW, image=pieces[count]) 
                count = count + 1
            elif(b.get(x,y)== bKnight):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/blackKnight.png")))
                canvas.create_image(75 * (y-2) + 48, 75 * (x-2) + 45, anchor=NW, image=pieces[count]) 
                count = count + 1
            elif(b.get(x,y)== wBishop):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/whiteBishop.png")))
                canvas.create_image(75 * (y-2) + 56, 75 * (x-2) + 49, anchor=NW, image=pieces[count]) 
                count = count + 1
            elif(b.get(x,y)== bBishop):
                pieces.append(ImageTk.PhotoImage(Image.open("Assets/blackBishop.png")))
                canvas.create_image(75 * (y-2) + 48, 75 * (x-2) + 55, anchor=NW, image=pieces[count]) 
                count = count + 1

#Main event loop for tkinter (Chess GUI).
def play(b):
    global enPassant
    mouseX = 0
    mouseY = 0
    bol = True
    root = Tk()
    root.title("Chess Engine")
    root.wm_iconbitmap('Assets/Neil.ico')
    canvas = Canvas(root, width=1000, height=700)
    canvas.pack()
    gameOver = False
    pieces = []
    board =  [[None for x in range(8)] for y in range(8)]
    highlightMoves = []
    global whiteMove
    whiteMove = True
    gameState = []
    highlight = []
    text = []
    level = []
    if len(level) > 0:
        level.pop(0)
    currentLevel = Label(root, text= "LEVEL 2",font=('Helvetica 15 bold'))
    level.append(currentLevel)

    level[0].place(x = 765,y = 400)
    #Methods that will occur when their corresponding button is pressed.
    def level1():
        global difficulty
        difficulty = "LEVEL1"
        if len(level) > 0:
            level.pop(0)
        currentLevel = Label(root, text= "LEVEL 1",font=('Helvetica 15 bold'))
        level.append(currentLevel)
        level[0].place(x = 765,y = 400)
    def level2():
        global difficulty
        difficulty = "LEVEL2"
        if len(level) > 0:
            level.pop(0)
        currentLevel = Label(root, text= "LEVEL 2",font=('Helvetica 15 bold'))
        level.append(currentLevel)
        level[0].place(x = 765,y = 400)
    def level3():
        global difficulty
        difficulty = "LEVEL3"
        if len(level) > 0:
            level.pop(0)
        currentLevel = Label(root, text= "LEVEL 3",font=('Helvetica 15 bold'))
        level.append(currentLevel)
        level[0].place(x = 765,y = 400)
    def level4():
        global difficulty
        difficulty = "LEVEL4"
        if len(level) > 0:
            level.pop(0)
        currentLevel = Label(root, text= "LEVEL 4",font=('Helvetica 15 bold'))
        level.append(currentLevel)
        level[0].place(x = 765,y = 400)
    def level5():
        global difficulty
        difficulty = "LEVEL5"
        if len(level) > 0:
            level.pop(0)
        currentLevel = Label(root, text= "LEVEL 5",font=('Helvetica 15 bold'))
        level.append(currentLevel)
        level[0].place(x = 765,y = 400)
    def reset():
        b.reset()
        setUpGame(b, "DEFAULT")
        displayBoard(b, canvas, board, pieces, highlight, highlightMoves, False)
        setValues(0, 0, 0, True, True, True, True, False, False)
        canvas.bind('<Button-1>', mouseHighlight) 
        global whiteMove
        global bol
        bol = True
        whiteMove = True
    def pawnGame():
        b.reset()
        setUpGame(b, "PAWNSONLY")
        displayBoard(b, canvas, board, pieces, highlight, highlightMoves, False)
        setValues(0, 0, 0, True, True, True, True, False, False)
        canvas.bind('<Button-1>', mouseHighlight) 
        global whiteMove
        global bol
        bol = True
        whiteMove = True
    def knights():
        b.reset()
        setUpGame(b, "KNIGHTS")
        displayBoard(b, canvas, board, pieces, highlight, highlightMoves, False)
        setValues(0, 0, 0, True, True, True, True, False, False)
        canvas.bind('<Button-1>', mouseHighlight) 
        global whiteMove
        global bol
        bol = True
        whiteMove = True
    def check1():
        b.reset()
        setUpGame(b, "CHECK1")
        displayBoard(b, canvas, board, pieces, highlight, highlightMoves, False)
        setValues(0, 0, 0, True, True, True, True, False, False)
        canvas.bind('<Button-1>', mouseHighlight) 
        global whiteMove
        global bol
        bol = True
        whiteMove = True
    def check2():
        b.reset()
        setUpGame(b, "CHECK2")
        displayBoard(b, canvas, board, pieces, highlight, highlightMoves, False)
        setValues(0, 0, 0, True, True, True, True, False, False)
        canvas.bind('<Button-1>', mouseHighlight) 
        global whiteMove
        global bol
        bol = True
        whiteMove = True
    def challengeGame():
        b.reset()
        setUpGame(b, "CHALLENGEMODE")
        displayBoard(b, canvas, board, pieces, highlight, highlightMoves, False)
        setValues(0, 0, 0, True, True, True, True, False, False)
        canvas.bind('<Button-1>', mouseHighlight) 
        global whiteMove
        global bol
        bol = True
        whiteMove = True
    
    displayBoard(b, canvas, board, pieces, highlight, highlightMoves, True)
    #Inatialitze all buttons and display them on the screen.
    button = Button(root, text = "ENGINE LEVEL 1", command = level1, fg = 'blue')
    button.pack()
    button.place(x = 760, y = 150)
    button1= Button(root, text = "ENGINE LEVEL 2", command = level2, fg = 'blue')
    button1.pack()
    button1.place(x = 760, y = 200)
    button2 = Button(root, text = "ENGINE LEVEL 3", command = level3, fg = 'blue')
    button2.pack()
    button2.place(x = 760, y = 250)
    button3 = Button(root, text = "ENGINE LEVEL 4", command = level4, fg = 'blue')
    button3.pack()
    button3.place(x = 760, y = 300)
    button9 = Button(root, text = "ENGINE LEVEL 5", command = level5, fg = 'blue')
    button9.pack()
    button9.place(x = 760, y = 350)
    button4 = Button(root, text = "RESET GAME", command = reset, fg = 'red')
    button4.pack()
    button4.place(x = 769, y = 450)
    button5 = Button(root, text = "PAWN GAME", command = pawnGame, fg = 'green')
    button5.pack()
    button5.place(x = 767, y = 500)
    button5 = Button(root, text = "CHALLENGE MODE: DO NOT EXCEED LEVEL 2", command = challengeGame, fg = 'red', bg = 'black')
    button5.pack()
    button5.place(x = 685, y = 650)
    button6 = Button(root, text = "KNIGHT GAME", command = knights, fg = 'orange')
    button6.pack()
    button6.place(x = 764, y = 550)
    button7 = Button(root, text = "PRACTICE 1", command = check1, fg = 'red')
    button7.pack()
    button7.place(x = 730, y = 600)
    button8 = Button(root, text = "PRACTICE 2", command = check2, fg = 'red')
    button8.pack()
    button8.place(x = 810, y = 600)
    boardEval = Label(root, text= "Board Evaluation\n0",font=('Helvetica 15 bold'))
    text.append(boardEval)
    text[0].place(x = 726,y = 80)

    #When mouse if first clicked on a piece, highlight that piece and all legal moves corresponding to that piece.
    def mouseHighlight(event): 
        if(event.x >= 50 and event.y >= 50):
            mouseX = int((int(event.x) - 50) / 75 )
            mouseY = int((int(event.y) - 50) / 75 )
        if (not mouseX > 7 and not mouseY > 7):
                if whiteMove and isWhite(b.get(mouseY + 2, mouseX + 2)):
                    global pieceRank
                    pieceRank = mouseY + 2
                    global pieceFile
                    pieceFile = mouseX + 2
                    highlight.append(canvas.create_rectangle(0, 0, 75, 75, fill='red', stipple="gray50"))
                    canvas.move(highlight[len(highlight) -1], 50 + 75 * mouseX,   50 + 75 * mouseY)
                    if len(highlight) > 1:
                        canvas.delete(highlight[0])
                        highlight.pop(0)
                    if len(highlightMoves)>0:
                        for x in range (len(highlightMoves)):
                            canvas.delete(highlightMoves[0])
                            highlightMoves.pop(0)
                    legalMoves = getLegalMoves(b,pieceRank, pieceFile, True)
                    count = 0
                    for x in legalMoves:
                        moveRank = convertRanks(x)
                        moveFile = convertFiles(x)
                        highlightMoves.append((canvas.create_rectangle(0, 0, 75, 75, fill='red', stipple="gray50")))
                        canvas.move(highlightMoves[count], 50 + 75 * (moveFile - 2),   50 + 75 * (moveRank- 2))
                        count = count + 1
                    canvas.bind('<Button-1>', mouseMove)

    #When a piece is highlighted and the user clicks a legal move square, move the piece to that square.             
    def mouseMove(event):
        if(event.x >= 50 and event.y >= 50):
            mouseX = int((int(event.x) - 50) / 75 )
            mouseY = int((int(event.y) - 50) / 75 )
            if (not mouseX > 7 and not mouseY > 7):
                global whiteMove
                global blackKingCheck
                global whiteKingCheck
                moveRank = mouseY + 2
                moveFile = mouseX + 2
                if whiteMove and isWhite(b.get(pieceRank,pieceFile)):
                    legalMoves = getLegalMoves(b,pieceRank, pieceFile, True)
                    if convertFilesRanks(moveRank, moveFile) in legalMoves: 
                        move(b,pieceRank , pieceFile, moveRank, moveFile, True)
                        if len(gameState) > 0:
                            canvas.delete(gameState[0])
                            gameState.pop(0)
                        displayBoard(b, canvas, board, pieces, highlight, highlightMoves, False)
                        allMoves = getAllMoves(b, "WHITE", False)
                        if kingLocation(b, "BLACK") in allMoves:
                            blackKingCheck = True
                            if len(getAllMoves(b, "BLACK", True)) < 1:
                                gameState.append(ImageTk.PhotoImage(Image.open("Assets/checkmate.png")))
                                canvas.create_image(249, -5, anchor=NW, image=gameState[0])
                            else:
                                gameState.append(ImageTk.PhotoImage(Image.open("Assets/check.png")))
                                canvas.create_image(289, -5, anchor=NW, image=gameState[0])
                        elif len(getAllMoves(b, "BLACK", True)) < 1:
                            gameState.append(ImageTk.PhotoImage(Image.open("Assets/draw.png")))
                            canvas.create_image(300, -5, anchor=NW, image=gameState[0]) 
                        elif insufficientMaterial(b):
                            gameState.append(ImageTk.PhotoImage(Image.open("Assets/draw.png")))
                            canvas.create_image(300, -5, anchor=NW, image=gameState[0])
                        whiteMove = False 
                     
                        root.update_idletasks()
                        bestMove = Engine.getBestMove(b, difficulty)
                        moveRank = convertRanks(bestMove[0])
                        moveFile = convertFiles(bestMove[0])
                        pR = bestMove[1]
                        pF = bestMove[2]
                        bol = True
                        if(bestMove[0] != 0):
                            while len(text) > 0:
                                text[0].destroy()
                                text.pop(0)
                                
                            evaluation = round(-1 * bestMove[3] /  100, 2)
                            if evaluation < 0:
                                evalMessage = Label(root, text= "Black is Winning",font=('Helvetica 20 bold'))
                                text.append(evalMessage)
                            else:
                                evalMessage = Label(root, text= "White is Winning",font=('Helvetica 20 bold'))
                                text.append(evalMessage)
                            boardEval = Label(root, text= "Board Evaluation\n" + str(evaluation),font=('Helvetica 15 bold'))
                            text.append(boardEval)
                            text[1].place(x = 725,y = 80)
                            text[0].place(x = 696,y = 50)
                            
                            highlightMoves.append((canvas.create_rectangle(0, 0, 75, 75, fill='red', stipple="gray50")))
                            canvas.move(highlightMoves[len(highlightMoves) -1], 50 + 75 * (moveFile - 2),   50 + 75 * (moveRank- 2))
                            highlightMoves.append((canvas.create_rectangle(0, 0, 75, 75, fill='red', stipple="gray50")))
                            canvas.move(highlightMoves[len(highlightMoves) -1], 50 + 75 * (pF - 2),   50 + 75 * (pR- 2))
                            move(b,pR , pF, moveRank, moveFile, True)
                            root.update_idletasks()
                            if len(gameState) > 0:
                                canvas.delete(gameState[0])
                                gameState.pop(0)
                            displayBoard(b, canvas, board, pieces,highlight, highlightMoves, False)
                            allMoves = getAllMoves(b, "BLACK", False)
                            if kingLocation(b, "WHITE") in allMoves:
                                whiteKingCheck = True
                                if len(getAllMoves(b, "WHITE", True)) < 1:
                                    gameState.append(ImageTk.PhotoImage(Image.open("Assets/checkmate.png")))
                                    canvas.create_image(249, -5, anchor=NW, image=gameState[0])
                                else:
                                    gameState.append(ImageTk.PhotoImage(Image.open("Assets/check.png")))
                                    canvas.create_image(289, -5, anchor=NW, image=gameState[0])
                            elif len(getAllMoves(b, "WHITE", True)) < 1:
                                gameState.append(ImageTk.PhotoImage(Image.open("Assets/draw.png")))
                                canvas.create_image(300, -5, anchor=NW, image=gameState[0]) 
                            elif insufficientMaterial(b):
                                gameState.append(ImageTk.PhotoImage(Image.open("Assets/draw.png")))
                                canvas.create_image(300, -5, anchor=NW, image=gameState[0]) 
                        else:
                            bol = False
                        if bol:
                            whiteMove = True 
                            canvas.bind('<Button-1>', mouseHighlight) 
                        else: 
                            bol = False
                        
                    else:
                        mouseHighlight(event)    
                else:
                    mouseHighlight(event)  
    canvas.bind('<Button-1>', mouseHighlight)
    root.mainloop()
 
