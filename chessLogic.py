import numpy as np

# Initialize board vector
# Index 0 = turn (-1 = white, 1 = black)
# Index 1 - 8 = A1 -> H1 and so forth
# Pieces
#   0 - empty
#   1 - white pawn
#   2 - white knight
#   3 - white bishop
#   4 - white rook
#   5 - white queen
#   6 - white king
#   7 - black pawn
#   8 - black knight
#   9 - black bishop
#   10 - black rook
#   11 - black queen
#   12 - black king

pieceList = [-1, 4, 2, 3, 5, 6, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 10, 8, 9, 11, 12, 9, 8, 10]
initialState = np.array(pieceList)

print(initialState)

