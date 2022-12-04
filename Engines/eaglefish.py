# imports
import time
import chess
import random

# Load trained ML engine
pass

# global variables
BESTMOVE = "e2e4"
NODES = 0
CURRENT_POSITION = [4, 2, 3, 5, 6, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 10, 8, 9, 11, 12, 9, 8, 10, -1]

# setname Options
forcedEnpassant = False

# Internal necessary options
default_internal = {
    'searchmoves': None, # array of possible moves
    'ponder': False,  # boolean
    'wtime': 100000, # in ms
    'btime': 100000, 
    'winc': None, # in ms
    'binc': None,
    'movestogo': None, # moves until next time control
    'depth': 3, # moves ahead (including opponent)
    'nodes': None, # legal moves looked at
    'mate': None, # searching for mate in exactly x moves
    'movetime': 10000, # in ms
    'infinite': False
}

internal = default_internal

def get_current_possible():
    board = chess.Board(fen=fen_from_current_position())
    legal_moves = [str(x) for x in board.legal_moves]
    return legal_moves

def fen_from_current_position():
    result = ""
    piecemap = {7: "p", 10: "r", 8: "n", 9: "b", 11:"q", 12: "k", 1: "P", 4: "R", 2: "N", 3: "B", 5: "Q", 6: "K"}
    i = 0
    start = 56
    spaces = 0
    while start > -1:
        while i < 8:
            val = CURRENT_POSITION[start + i]
            if val:
                if spaces:
                    result += str(spaces)
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
    result += " " + "b" if CURRENT_POSITION[-1] else "w"
    result += " - - 0 0" # This should really not be hardcoded fwiw but should be good enough
    return result

def set_position_from_fen(fen):
    fen_args = fen.split()
    pos_string = fen_args[0]
    move = -1 if fen_args[1] == "w" else 1
    start = 56
    i = 0
    piecemap = {"p": 7,"r": 10,"n": 9, "b": 8,"q": 11,"k": 12, "P": 1,"R": 4,"N": 3,"B": 2,"Q": 5,"K": 6}
    for char in pos_string:
        if i > 8 or start < 0: raise Exception("Invalid FEN")
        if char in '12345678':
            num = int(char)
            CURRENT_POSITION[start+i:start+num] = [0]*num
            i += num
        elif char == '/':
            i = 0
            start -= 8
        else:
            try:
                CURRENT_POSITION[start + i] = piecemap[char]
                i += 1
            except:
                raise Exception("Invalid FEN")
    CURRENT_POSITION[-1] = move
    return

def valid_move(stringmove):
    alphabet = 'abcdefgh'
    numbet = '12345678'
    return stringmove[0] in 'alphabet' and stringmove[1] in numbet and stringmove[2] in alphabet and stringmove[3] in numbet 

def main_loop():
    print("starting game")
    while True:
        option = input()
        match option:
            case "uci":
                print("id name eaglefish")
                print("id author David Evan Joe Mike Minh")
                print("option name forcedEnpassant type check default false")
                print("uci ok")
                continue
            case "debug on":
                pass
                continue
            case "debug off":
                pass
                continue
            case "isready":
                # load the NN weights
                
                # print ready
                print("readyok")
                continue
            case "register":
                pass
                continue
            case "ucinewgame":
                continue
            case "quit":
                break
        args = option.split()
        length = len(args)
        i = 1
        match args[0]:
            case "go":
                start_time = time.time()
                internal = default_internal
                search = None
                while(i < length):
                    if search == None:
                        if args[i] in internal.keys():
                            search = args[i]
                        else:
                            break # ignore the remaining commands
                    else:
                        match search:
                            case 'searchmoves': 
                                if args[i] in internal.keys():
                                    i -= 1 
                                    search = None
                                    continue
                                elif valid_move(args[i]):
                                    if internal['searchmoves']:
                                        internal['searchmoves'].append(args[i])
                                    else:
                                        internal['searchmoves'] = [args[i]]
                                else:
                                    break # ignore the remaining commands
                            case 'ponder':
                                internal['ponder'] = True
                                search = None
                                continue
                            case "wtime":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['wtime'] = args[i]
                                    continue
                                else:
                                    break
                            case "btime":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['btime'] = args[i]
                                    continue
                                else:
                                    break
                            case "winc":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['winc'] = args[i]
                                    continue
                                else:
                                    break
                            case "binc":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['binc'] = args[i]
                                    continue
                                else:
                                    break
                            case "movestogo":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['movestogo'] = args[i]
                                    continue
                                else:
                                    break
                            case "depth":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['depth'] = args[i]
                                    continue
                                else:
                                    break
                            case "nodes":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['nodes'] = args[i]
                                    continue
                                else:
                                    break
                            case "mate":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['mate'] = args[i]
                                    continue
                                else:
                                    break
                            case "movetime":
                                if type(args[i]) == int and args[i] > 0:
                                    search = None
                                    internal['movetime'] = args[i]
                                    continue
                                else:
                                    break
                            case "infinite":
                                search = None
                                internal['infinite'] = True
                                continue
                            case "ponderhit":
                                print("user played expected moves!")
                                continue
                            case "stop":
                                print("info nodes" + NODES + " time " + str(start_time - time.time()))
                                print('bestmove ' + BESTMOVE)
                                continue
                            case "quit":
                                break
                    i += 1
                # get all possible moves as array in ['e2e4', 'f3g5'] format
                poss = get_current_possible()

                # do thinking stuff (or just pick a random move for now)
                BESTMOVE = random.choice(poss)
                while True:
                    # we should do background processing instead of just waiting here
                    cmd = input()
                    match cmd:
                        case "quit":
                            quit()
                        case "stop":
                            print("info nodes" + NODES + " time " + str(start_time - time.time()))
                            print('bestmove ' + BESTMOVE)
                            break
            case "setoption":
                if not length == 5: continue
                if args[1] != 'name': continue
                if args[3] != 'value': continue
                match args[2].lower():
                    case "forcedenpassant":
                        forcedEnpassant = args[4].lower() == "true\n" 
                    case _:
                        continue
            case "position":
                if length < 2: continue
                if args[1] == 'fen':
                    try:
                        set_position_from_fen(args[2:8]) # <----- Untested
                        i = 8
                    except Exception as e:
                        # print(e)
                        continue
                    if length == 3: continue
                elif args[1] != 'startpos':
                    if length == 2: continue
                    i = 2
                else: continue 
                if not args[i] == 'moves': 
                    continue
                i += 1
                # make moves on current position
                # Mike TODO
                while(i < length):
                    i += 1
            case _:
                print("no command matched")
        

main_loop()


