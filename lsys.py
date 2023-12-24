# L-sys, a scripting language for L-systems

from sys import argv
from os import path

from src import *


WND_WIDTH = int(640 * 1.5)
WND_HEIGHT = int(480 * 1.5)


def print_help():
    print("usage: lsys.py <file.lsys> <options>")
    print("options:")
    print("  -c  int   complexity")
    print("  -h  none  print this message")


E_OK = 0
E_WRONG_AMOUNT_OF_ARGS = 1
E_NOT_A_FILE = 2
E_CANT_OPEN_FILE = 3
E_WRONG_OPTIONS = 4


def get_error_msg(code) -> None:
    if code == E_WRONG_AMOUNT_OF_ARGS:
        print_help()
        return "Expected at least 1 argument got none."
    elif code == E_NOT_A_FILE:
        return "File doesn't exist."
    elif code == E_CANT_OPEN_FILE:
        return "Couldn't open file."
    elif code == E_WRONG_OPTIONS:
        print_help()
        return "Wrong options."


def main(args):
    if len(args) < 2:
        return E_WRONG_AMOUNT_OF_ARGS

    script_path = args[1]

    if not path.isfile(script_path):
        return E_NOT_A_FILE

    source = None
    with open(script_path, "r") as f: source = f.read()

    if source == None:
        return E_CANT_OPEN_FILE

    # command options
    complexity = 4

    if len(args) > 2:
        i = 2
        while i < len(args):
            if args[i] == "-h":
                print_help()
                return E_OK
            elif args[i] == "-c":
                i += 1
                if i > len(args) - 1:
                    return E_WRONG_OPTIONS
                complexity = int(args[i])
            i += 1

    # parsing
    parsed = parse(source)
    Log.info(parsed)

    structure = generate_structure(parsed, complexity)

    # drawing
    wnd = Window(WND_WIDTH, WND_HEIGHT)
    render(wnd, structure)
    wnd.mainloop()

    return 0


if __name__ == "__main__":
    code = main(argv)
    if code != 0:
        Log.error(get_error_msg(code))
    print("Exited with exit code:", code)
