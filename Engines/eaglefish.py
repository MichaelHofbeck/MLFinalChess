# imports
pass

# Load trained ML engine
pass

# Default Options
depth = 1
forced_enpassant = False


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
        match args[0]:
            case "go":
                flags = {"searchmoves": False, "ponder": False, "wtime": False, "btime": False, "winc": False, "binc": False, "movestogo": False, "depth": 3, "nodes": False, "mate": False, "movetime": 10000, "infinite": False}
                while(True):
                    for i in range(len(args)):
                        if args[i] in flags:
                            flags[args[i]] = args[i + 1]
            case "setoption":
                pass
            case "position":
                pass
        print("no command matched")

main_loop()


