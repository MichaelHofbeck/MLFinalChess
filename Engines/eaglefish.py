# imports
import time
import chess
import random
import threading
import queue
import time


def get_input(message, channel):
    response = input()
    channel.put(response)


def input_with_timeout(message, timeout):
    channel = queue.Queue()
    thread = threading.Thread(target=get_input, args=(message, channel))
    # by setting this as a daemon thread, python won't wait for it to complete
    thread.daemon = True
    thread.start()

    try:
        response = channel.get(True, timeout)
        return response
    except queue.Empty:
        pass
    return None

# Load trained ML engine
pass

# global variables
BESTMOVE = "e7e6"
NODES = 0
CURRENT_POSITION = [4, 2, 3, 5, 6, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 10, 8, 9, 11, 12, 9, 8, 10, -1]
START_POSITION = CURRENT_POSITION

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
    'movetime': 0, # in ms
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
    result += " b" if CURRENT_POSITION[-1] == 1 else " w"
    result += " - - 0 0" # This should really not be hardcoded fwiw but should be good enough
    return result

def make_move(move):
    CURRENT_POSITION[64] *= -1
    match move:
        case 'e1c1':
            CURRENT_POSITION[0] = 0
            CURRENT_POSITION[2] = 6
            CURRENT_POSITION[3] = 4
            CURRENT_POSITION[4] = 0
        case 'e1g1':
            CURRENT_POSITION[4] = 0
            CURRENT_POSITION[6] = 6
            CURRENT_POSITION[5] = 4
            CURRENT_POSITION[7] = 0
        case 'e8c8':
            CURRENT_POSITION[56] = 0
            CURRENT_POSITION[58] = 12
            CURRENT_POSITION[59] = 10
            CURRENT_POSITION[60] = 0
        case 'e8g8':
            CURRENT_POSITION[62] = 0
            CURRENT_POSITION[62] = 12
            CURRENT_POSITION[61] = 10
            CURRENT_POSITION[60] = 0
        case _:
            row_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h':7}
            piecemap = {"p": 7,"r": 10,"n": 9, "b": 8,"q": 11,"k": 12, "P": 1,"R": 4,"N": 3,"B": 2,"Q": 5,"K": 6}
            start_square = move[:2]
            start_square_index = row_map[start_square[0]] + (int(start_square[1]) - 1) * 8
            end_square = move[2:4]
            end_square_index = row_map[end_square[0]] + (int(end_square[1]) - 1) * 8
            CURRENT_POSITION[end_square_index] = CURRENT_POSITION[start_square_index] if len(move) != 5 else piecemap[move[4]]
            CURRENT_POSITION[start_square_index] = 0

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

def valid_move(stringmove):
    alphabet = 'abcdefgh'
    numbet = '12345678'
    return stringmove[0] in 'alphabet' and stringmove[1] in numbet and stringmove[2] in alphabet and stringmove[3] in numbet 

def main_loop():
    print("info string eaglefish unr Build 0")
    while True:
        option = input()
        match option:
            case "uci":
                print("id name eaglefish")
                print("id author HarikaStudios")
                print("option name forcedEnpassant type check default false")
                print("uciok")
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
                return
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
                                continue
                            case "quit":
                                return BESTMOVE
                                break
                    i += 1
                # get all possible moves as array in ['e2e4', 'f3g5'] format
                poss = get_current_possible()

                # do thinking stuff (or just pick a random move for now)
                BESTMOVE = random.choice(poss)
                movetime = internal['movetime'] if internal['movetime'] != 0 else 200
                if internal['infinite']: movetime = 0
                while internal['infinite'] or movetime > int(1000*(time.time() - start_time)):
                    # we should do background processing instead of just waiting here
                    cmd = input_with_timeout("Commands:", max((movetime/1000 - time.time() - start_time), 0.1))
                    match cmd:
                        case "quit":
                            return
                        case "stop":
                            print("info nodes " + str(NODES) + " time " + str(int(1000*(time.time() - start_time))))
                            print('bestmove ' + BESTMOVE)
                            internal['infinite'] = False
                if movetime != 0:
                    print("info nodes " + str(NODES) + " time " + str(int(1000*(time.time() - start_time))) + " pv " + BESTMOVE)
                    print('bestmove ' + BESTMOVE)

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
                        continue
                    if length == 3: continue
                if args[1] == 'startpos':
                    if length == 2: continue
                    i = 2
                    CURRENT_POSITION = START_POSITION
                else: continue
                if not args[i] == 'moves':
                    continue
                i += 1
                while(i < length):
                    make_move(args[i])
                    i += 1
            case _:
                pass
                # print("no command matched")
        

main_loop()


