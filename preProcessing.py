import chess
import chess.pgn
import re
import numpy as np
import json
import chess.engine

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

def fenFromPosition(boardState):
     return fen_from_current_position(boardState)

def evalFromFen(fen):
     engine = createEngine()
     board = chess.Board(fen)
     info = engine.analyse(board, chess.engine.Limit(time=0.1))
     print("Score:", info["score"])
     return info["score"]

def createEngine():
     engine = chess.engine.SimpleEngine.popen_uci("./Engines/stockfish.exe")
     return engine

def evalFromPosition(boardState):
     return evalFromFen(fenFromPosition(boardState))


def fen_from_current_position(position):
    result = ""
    piecemap = {7: "p", 10: "r", 8: "n", 9: "b", 11:"q", 12: "k", 1: "P", 4: "R", 2: "N", 3: "B", 5: "Q", 6: "K"}
    i = 0
    start = 56
    spaces = 0
    while start > -1:
        while i < 8:
            val = position[start + i]
            if val:
                if spaces:
                    result += str(spaces)
                    spaces = 0
                result += piecemap[val]
            else:
                spaces += 1
            i += 1
        if spaces:
            result += str(spaces)
        start -= 8
        if start > -1:
            result += "/"
        i = 0
        spaces = 0
    result += " b" if position[-1] == 1 else " w"
    result += " - - 0 0" # This should really not be hardcoded fwiw but should be good enough
    return result

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

def evalData(gameVectors):
     newVector = []
     for game in gameVectors:
          game = game[1:]
          for i in range(len(game)):
               print(game[i])
               game[i].append(evalFromPosition(game[i]))
               newVector.append(game[i])
     return newVector


# This function will return an array of eval-labeled boardstates from minhs data
def evalProcessing():
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

     gameVectors = evalData(gameVectors)
     print(gameVectors)
     stateVectors, targetVectors = getTargetVector(gameVectors)
     data = np.array(stateVectors)
     target = np.array(targetVectors)
     print(gameVectors[0])
     return data, target

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
     for pos in npArray_data:
          evalFromPosition(pos)
     # board  = chess.Board()
     # print(str(board).split())
     # for move in games[1].mainline_moves():
     #           board.push(move)
     #           print(board)
     return npArray_data, npArray_target


# main()
evalProcessing()

# 10, 8, 9, 11, 12, 9, 8, 10, 
# 7, 7, 7, 7, 0, 7, 7, 7
# 0, 0, 0, 0, 0, 0, 0, 0,
# 0, 0, 0, 0, 7, 0, 0, 0
# 0, 0, 0, 0, 0, 0, 0, 0
# 0, 0, 0, 0, 0, 0, 0, 0
# 1, 1, 1, 1, 1, 1, 1, 1,
# 4, 2, 3, 5, 6, 3, 2, 4

