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
E_NOT_A_FILE = 1
E_CANT_OPEN_FILE = 2
E_WRONG_OPTIONS = 3
E_NO_FILE_GIVEN = 4


def get_error_msg(code) -> None:
    if code == E_NOT_A_FILE:
        return "File doesn't exist."
    elif code == E_CANT_OPEN_FILE:
        return "Couldn't open file."
    elif code == E_WRONG_OPTIONS:
        print_help()
        return "Wrong options."
    elif code == E_NO_FILE_GIVEN:
        print_help()
        return "No file specified"


def main(args):
    script_path = None
    complexity = 4

    i = 1
    while i < len(args):
        if args[i] == "-h":
            print_help()
            return E_OK
        elif args[i] == "-c":
            i += 1
            if i > len(args) - 1:
                return E_WRONG_OPTIONS
            try:
                complexity = int(args[i])
            except:
                return E_WRONG_OPTIONS
        else:
            script_path = args[i]

        i += 1

    if script_path is None:
        return E_NO_FILE_GIVEN

    if not path.isfile(script_path):
        return E_NOT_A_FILE

    source = None
    with open(script_path, "r") as f: source = f.read()

    if source == None:
        return E_CANT_OPEN_FILE

    data = parse(source)
    structure = generate_structure(data, complexity)

    wnd = Window(WND_WIDTH, WND_HEIGHT)
    render(wnd, structure)
    wnd.mainloop()

    return 0


if __name__ == "__main__":
    code = main(argv)
    if code != 0:
        Log.error(get_error_msg(code))
    print("Exited with exit code:", code)
