#Class that will be used to hold a board object and all the pieces on that board.
class Board():
	rows, cols = (12, 12)

	#Board will be an integer array and these numbers will represent different pieces.
	offBoard, freeSpace, wPawn, wKnight, wBishop, wRook, wQueen, wKing, bPawn, bKnight, bBishop, bRook, bQueen, bKing = (-1, 0,1,2,3,4,5,6, 7, 8, 9, 10, 11, 12)

	#potential values that we may want to store on a board object.
	boardEvaluation = 0
	parentMove = 0
	parentRank = 0
	parentFile = 0
	bestMoves = []

	#Constructor
	def __init__(self, board):
		self.board = board

	#Getter/setter methods
	def getBestMoves(object):
		return object.bestMoves
	def getBoardEvaluation(object):
		return object.boardEvaluation
	def getParentMove(object):
		return object.parentMove
	def getParentRank(object):
		return object.parentRank
	def getParentFile(object):
		return object.parentFile
	def setBoardEvaluation(object, val):
		object.boardEvaluation = val
	def setParentMove(object, val):
		object.parentMove = val
	def setParentRank(object, val):
		object.parentRank = val
	def setParentFile(object, val):
		object.parentFile = val
	def addBestMove(object,position, arr):
		object.bestMoves.append(position, arr)
	
  	#Convert board index to string for printing and testing purposes.
	def convertString(index):
		if(index == Board.freeSpace):
			return "ES"
		if(index == Board.wPawn):
			return "wP"
		if(index == Board.wKnight):
			return "wK"
		if(index == Board.wBishop):
			return "wB"
		if(index == Board.wRook):
			return "wR"
		if(index == Board.wQueen):
			return "wQ"
		if(index == Board.wKing):
			return "KW"
		if(index == Board.bPawn):
			return "bP"
		if(index == Board.bKnight):
			return "bK"
		if(index == Board.bBishop):
			return "bB"
		if(index == Board.bRook):
			return "bR"
		if(index == Board.bQueen):
			return "bQ"
		if(index == Board.bKing):
			return "KB"

	#Prints entire board in string form to terminal
	def printBoard(object):
		for x in range(Board.rows):
			for y in range(Board.cols):
				if(not object.board[x][y] == -1):
					print(Board.convertString(object.board[x][y]), end = "  ")
			print("\n")

	#Sets out-of-bounds values in the board array to -1 so that pieces can recognize offboard positions. 
	def setOffBoard(object):
		count = 0
		for x in range(2):
			for y in range(Board.cols):
				object.board[x][y] = Board.offBoard
		for x in range(Board.rows-2, Board.rows):
			for y in range(Board.cols):
				object.board[x][y] = Board.offBoard
		for x in range(Board.rows):
			for y in range(2):
				object.board[x][y] = Board.offBoard
		for x in range(Board.rows):
			for y in range(Board.cols-2, Board.cols):
				object.board[x][y] = Board.offBoard

	#Sets black and white pawns in their default position.
	def setPawns(object):
		for x in range(2, Board.cols - 2):
			object.board[3][x] = Board.bPawn
			object.board[8][x] = Board.wPawn

	#Sets black and white knights in their default position.
	def setKnights(object):
		object.board[2][3] = Board.bKnight
		object.board[2][8] = Board.bKnight
		object.board[9][3] = Board.wKnight
		object.board[9][8] = Board.wKnight

	def setBishops(object):
		object.board[2][4] = Board.bBishop
		object.board[2][7] = Board.bBishop
		object.board[9][4] = Board.wBishop
		object.board[9][7] = Board.wBishop

	def setQueens(object):
		object.board[2][5] = Board.bQueen
		object.board[9][5] = Board.wQueen

	def setKings(object):
		object.board[2][6] = Board.bKing
		object.board[9][6] = Board.wKing

	def setRooks(object):
		object.board[2][2] = Board.bRook
		object.board[2][9] = Board.bRook
		object.board[9][2] = Board.wRook
		object.board [9][9] = Board.wRook

	def set(object,row, col, val):
		object.board[row][col] = val

	def get(object, row, col):
		return object.board[row][col]
	def reset(object):
		for x in range(Board.rows):
			for y in range(Board.cols):
				object.set(x, y, Board.freeSpace)
	


	
				
				
				
				