import chess
import chess.pgn
import re
import numpy as np

# converts Board() object to a vector of 1x65
def boardToVec(board):
     currentBoard = str(board)
     positionArray = currentBoard.split()
     # 12 unique pieces
     pieceToNum = {'.': 0, 'p': 7, 'n': 8, 'b': 9, 'r':10, 'k': 11, 'q': 12, 'P': 1, 'N': 2, 'B': 3, 'R': 4, 'K': 5, 'Q': 6}
     vector = []
     for i in range(len(positionArray)- 1 , -1, -1):
          file = i % 8
          rank = i // 8
          vector.append(pieceToNum[positionArray[(7 - rank) * 8 + file]])
     vector.reverse()
     vector.append(-1 if board.turn == True else 1)
     return vector

def main():
     games = []
     gameVectors = []
     for i in range(23):
          pgn = open("minhChessData/chess_com_games_2022-12-03 (" + str(i) + ").pgn")
          # print(pgn)
          for i in range(50):
               games.append(chess.pgn.read_game(pgn))

     for i in range(len(games)):     
          # creating a virtual chessboard
          board = chess.Board()
          game = []
          # prints out all chessboard possitions
          for move in games[i].mainline_moves():
               board.push(move)
               # print(board)
               game.append(boardToVec(board))
          gameVectors.append(game)

     npArray = np.array(gameVectors)
     # print(npArray)
     # print(npArray.shape)
     # print(npArray[1])
     # board  = chess.Board()
     # print(str(board).split())
     # for move in games[1].mainline_moves():
     #           board.push(move)
     #           print(board)
main()

# 10, 8, 9, 11, 12, 9, 8, 10, 
# 7, 7, 7, 7, 0, 7, 7, 7
# 0, 0, 0, 0, 0, 0, 0, 0,
# 0, 0, 0, 0, 7, 0, 0, 0
# 0, 0, 0, 0, 0, 0, 0, 0
# 0, 0, 0, 0, 0, 0, 0, 0
# 1, 1, 1, 1, 1, 1, 1, 1,
# 4, 2, 3, 5, 6, 3, 2, 4

