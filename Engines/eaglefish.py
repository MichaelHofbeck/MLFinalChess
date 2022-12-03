# imports
pass

# Load trained ML engine
pass

# global variables
BESTMOVE = "e2e4"
CURRENT_POSITION = [4, 2, 3, 5, 6, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 10, 8, 9, 11, 12, 9, 8, 10, -1]


# setname Options
forced_enpassant = False

def valid_move(stringmove):
    alphabet = 'abcdefgh'
    numbet = '12345678'
    return stringmove[0] in 'alphabet' and stringmove[1] in numbet and stringmove[2] in alphabet and stringmove[3] in numbet 

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
def main_loop():
    print("starting game")
    while True:
        option = input()
        match option:
            case "uci":
                print("id name eaglefish")
                print("id author daveed")

                print("uci ok")
                continue
            case "debug on":
                pass
                continue
            case "debug off":
                pass
                continue
            case "isready":
                pass
                continue
            case "register":
                pass
                continue
            case "ucinewgame":
                pass
                continue
            case "stop":
                print(BESTMOVE)
                continue
            case "ponderhit":
                pass
                continue
            case "quit":
                break
        args = option.split()
        length = len(args)
        i = 1
        match args[0]:
            case "go":
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
                            case "quit":
                                break
                    i += 1
            case "setoption":
                pass
            case "position":
                pass
            case _:
                print("no command matched")
        

main_loop()


