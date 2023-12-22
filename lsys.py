# L-sys, a scripting language for L-systems

from sys import argv
from os import path

from src import *


WND_WIDTH = int(640 * 1.5)
WND_HEIGHT = int(480 * 1.5)


def main(args):
    if len(args) < 2:
        Log.error("Expected 1 argument got none.")
        print("lsys.py <script_path>")
        return 1

    script_path = args[1]

    if not path.isfile(script_path):
        Log.error(f"File '{script_path}' doesn't exist")
        return 1

    source = None
    with open(script_path, "r") as f: source = f.read()

    if source == None:
        Log.error("Couldn't open file.")
        return 1

    # parsing
    parsed = parse(source)
    Log.info(parsed)

    structure = generate_structure(parsed, 4)

    # drawing
    wnd = Window(WND_WIDTH, WND_HEIGHT)
    render(wnd, structure)
    wnd.mainloop()

    return 0


if __name__ == "__main__":
    code = main(argv)
    print("Exited with exit code:", code)
