# imports
pass

# Load trained ML engine
pass

# setname Options
forced_enpassant = False

def valid_move(stringmove):
    alphabet = 'abcdefgh'
    numbet = '12345678'
    return stringmove[0] in 'alphabet' and stringmove[1] in numbet and stringmove[2] in alphabet and stringmove[3] in numbet 

# Internal necessary options
internal = {
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

def main_loop():
    print("starting game")
    while True:
        option = input()
        match option:
            case "uci":
                print("id name eaglefish")
                print("id author daveed")

                print("uci ok")
            case "debug on":
                pass
            case "debug off":
                pass
            case "isready":
                pass
            case "register":
                pass
            case "ucinewgame":
                pass
            case "stop":
                pass
            case "ponderhit":
                pass
            case "quit":
                pass
            case _:
                pass
        args = option.split()
        length = len(args)
        i = 1
        match args[0]:
            case "go":
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
                                print()
                    i += 1
            case "setoption":
                pass
            case "position":
                pass
        print(internal['searchmoves'])
        print("no command matched")

main_loop()


