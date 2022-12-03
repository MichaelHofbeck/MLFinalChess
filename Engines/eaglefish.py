# imports
pass

# Load trained ML engine
pass

def main_loop():
    print("starting game")
    while True:
        option = input()
        match option:
            case "uci":
                pass
            case "debug on":
                pass
            case "debug off":
                pass
            case "isready":
                pass
            case "setoption":
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
        length = len(option)
        if length < 2: continue
        if option[:2] == "go":
            pass
        if length < 8: continue
        if option[:8] == "position":
            pass
        if length < 14: continue
        if option[:14] == "setoption name":
            pass
        print("no command matched")

main_loop()


