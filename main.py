#Create a board, and start the chess GUI.
from Board import Board
import Chess
arr = [[0 for x in range(12)] for y in range(12)]
b = Board(arr)
Chess.setUpGame(b, "DEFAULT")
Chess.play(b)



