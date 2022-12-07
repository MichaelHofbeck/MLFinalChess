import chess
import chess.pgn
import re
import numpy as np
import random

# define user
USER = 'minhle10'
COLORDEX = {'White': -1, 'Black': 1}

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

def labelData(gameVectors):
     newGameVectors = []
     for game in gameVectors:
          newGame = []
          for i in range(len(game) - 1):
               if i == 0:
                    color = COLORDEX[game[i]]
               else:
                    game[i].append(boardStateToMoveInt(game[i], game[i + 1]))
                    del game[i][0]
                    if color == game[i][-2]:
                         newGame.append(game[i])
          newGameVectors.append(newGame)
     return newGameVectors

# TODO ADD CASTLING FUNCTIONALITY
def boardStateToMoveInt(initialBoardState, endBoardState):
     for i in range(len(initialBoardState) - 1):
          if (endBoardState[i] == 0) and (initialBoardState[i] != 0):
               startSquare = i
          if (endBoardState[i] != initialBoardState[i]) and (endBoardState[i] != 0):
               endSquare = i
     return startSquare * 100 + endSquare

def randomizeGameStates(gameVectors):
     newStateVector = []
     for game in gameVectors:
          for state in game:
               newStateVector.append(state)
     return newStateVector

def getTargetVector(stateVectors):
     target = []
     for state in stateVectors:
          target.append(state[-1])
          del state[-1]
     return stateVectors, target

def main():
     games = []
     gameVectors = []
     for i in range(23):
          pgn = open("minhChessData/chess_com_games_2022-12-03 (" + str(i) + ").pgn")
          # print(pgn)
          for i in range(50):
               if chess.pgn.read_game(pgn) is not None:
                    if chess.pgn.read_game(pgn).headers["White"] == USER:
                         games.append(['White', chess.pgn.read_game(pgn)])
                    else:
                         games.append(['Black', chess.pgn.read_game(pgn)])

     for i in range(len(games)):     
          # creating a virtual chessboard
          board = chess.Board()
          game = []
          # prints out all chessboard positions
          if games[i][1] is not None:
               game.append(games[i][0])
               for move in games[i][1].mainline_moves():
                    board.push(move)
                    # print(board)
                    game.append(boardToVec(board))
               gameVectors.append(game)

     gameVectors = labelData(gameVectors)
     stateVectors = randomizeGameStates(gameVectors)
     stateVectors, targetVectors = getTargetVector(stateVectors)
     npArray_data = np.array(stateVectors)
     npArray_target = np.array(targetVectors)
     # print(npArray.shape)
     # board  = chess.Board()
     # print(str(board).split())
     # for move in games[1].mainline_moves():
     #           board.push(move)
     #           print(board)
     return npArray_data, npArray_target

main()

# 10, 8, 9, 11, 12, 9, 8, 10, 
# 7, 7, 7, 7, 0, 7, 7, 7
# 0, 0, 0, 0, 0, 0, 0, 0,
# 0, 0, 0, 0, 7, 0, 0, 0
# 0, 0, 0, 0, 0, 0, 0, 0
# 0, 0, 0, 0, 0, 0, 0, 0
# 1, 1, 1, 1, 1, 1, 1, 1,
# 4, 2, 3, 5, 6, 3, 2, 4

