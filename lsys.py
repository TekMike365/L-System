# L-sys, a scripting language for L-systems

from sys import argv
from os import path
from colorama import Fore, Style

import re
import math
import tkinter
import copy

from src import Vec2

# TODO combine calculation of size with generating points (liear scaling when drawing)
# TODO add iterations setting
# TODO add a possibility to change the window size
# TODO add more settings
# TODO fix issues
#?      fractal doesn't fit on screen (triangle.lsys, koch_snowflake.lsys)
#?              in the case of (tree.lsys), iteration 4 doesn't fit on the screet
#?      fractal crashes (quad_gosper.lsys)
#?      fractal doesn't work (dragon_curve.lsys)
#?      Mango Leaf is looking weird (mango_lead.lsys)


WND_WIDTH = int(640 * 1.5)
WND_HEIGHT = int(480 * 1.5)
WND_PADDING_W = WND_WIDTH * 0.05
WND_PADDING_H = WND_HEIGHT * 0.05


class Log:
    @staticmethod
    def info(msg) -> None:
        print(f"{Style.DIM}[INFO]: {str(msg)}{Style.RESET_ALL}")

    @staticmethod
    def warning(msg) -> None:
        print(f"{Fore.YELLOW}[WARNING]: {str(msg)}{Fore.RESET}")

    @staticmethod
    def error(msg) -> None:
        print(f"{Fore.RED}[ERROR]: {str(msg)}{Fore.RESET}")


class Cell:
    class Data:
        DRAW = "draw"
        DOT = "dot"
        WIDTH = "width"
        POLYGON = "polygon"

        def __init__(self) -> None:
            self.data = {
                self.DRAW: True,
                self.DOT: False,
                self.WIDTH: 1,
                self.POLYGON: False
            }

        def __str__(self) -> str:
            return str(self.data)

        def set(self, key, value) -> None:
            self.data[key] = value

        def get(self, key):
            return self.data[key]

    def __init__(self, points, data: Data) -> None:
        self.points = points
        self.data = data

    def __str__(self) -> str:
        return f"Cell<{[str(e) for e in self.points]}, {self.data}>"


def print_help():
    print("lsys.py <script_path>")


# comment
# ; starts with semicolon continues till end of line

# keywords:
# axiom, rules

# settings:
# angle, winc, lfac, ainc

# characters:
# F (any uppercase letter), f (any lowercase letter),
# +, -, |, [, ], #, !, @, {, }, <, >, &, (, )

# rules:
# <exp> = set of characters and <variable>
# <variable> starts with a dot
#       .<name> <exp>
# <rule> = <upper or lowercase letter> -> <exp>
# keyword rules:
#       axiom <exp>
#       rules <rules separated with coma>
#       <setting> value

def main(args):
    if len(args) < 2:
        Log.error("Expected 1 argument got none.")
        print_help()
        return 1

    script_path = args[1]

    if not path.isfile(script_path):
        Log.error(f"File '{script_path}' doesn't exist")
        return 1

    source = None
    with open(script_path, "r") as f: source = f.read()

    if source == None:
        Log.warning("Couldn't open file.")
        return 1

    # parsing
    axiom = ""
    rules = {}
    settings = {
        "angle": 60.0,
        "winc": 0,
        "lfac": 1.0,
        "ainc": 0
    }

    source = re.sub(";.*$", "", source, flags=re.RegexFlag.MULTILINE)   # remove comments
    source = re.sub("\s+", " ", source, flags=re.RegexFlag.MULTILINE)   # compact spaces

    # useful shit
    re_keywords = "axiom|rules|angle|winc|lfac|ainc"
    re_character = "[a-zA-Z+\-|[\]#!@{}<>&()]"
    re_variable = "\.[a-zA-Z_]\w*"
    expression = f"(?:{re_variable}|{re_character})+"  # selects kinda everything

    # substituting variables
    vars = re.findall(f" {re_variable} {expression}", source)
    vars = [e for e in vars if re.search(re_keywords, e) is None]
    for var in vars:
        name, value = var.split()
        source = re.sub(var, "", source)
        source = re.sub(f"\{name}", value, source)

    # tokenisation or smthn

    # getting the axiom
    axiom = re.search(f"(axiom) ({expression})", source).group(2)

    # getting the rules
    src_rules = re.search(f"(rules )(([a-zA-Z] -> {expression}(, )?)+)", source).group(2)
    src_rules = re.split(", ", src_rules)
    for rule in src_rules:
        key, val = rule.split(" -> ")
        rules[key] = val

    # getting the settings
    for setting in settings.keys():
        sett = re.search(f"({setting}) (\d+(\.\d+)?)", source)
        if sett is not None:
            settings[setting] = float(sett.group(2))

    Log.info(f"axiom: {axiom}")
    Log.info(f"rules: {rules}")
    Log.info(f"settings: {settings}")

    # generating structure
    iterations = 9
    structure = axiom
    for _ in range(iterations):
        for rule in rules.keys():
            structure = structure.replace(rule, rules[rule])

    # generating points
    stack = []
    top_most = 0.0
    bottom_most = 0.0
    right_most = 0.0
    left_most = 0.0

    data = {
        "turning_angle": settings["angle"],
        "angle": 0.0,
        "length": 1.0,
        "swap": 1,
        "point": Vec2(0.0, 0.0)
    }

    for cmd in structure:
        if cmd == "F" or cmd == "f":      # move forward
            change = Vec2(data["length"], 0.0)
            change.rotate((90.0 + data["angle"]) * math.pi / 180)
            data["point"].add(change)

            top_most = max(top_most, data["point"].y)
            bottom_most = min(bottom_most, data["point"].y)
            right_most = max(right_most, data["point"].x)
            left_most = min(left_most, data["point"].x)
        elif cmd == "+":    # increments by an angle
            data["angle"] += data["swap"] * data["turning_angle"]
        elif cmd == "-":    # decrements by an angle
            data["angle"] -= data["swap"] * data["turning_angle"]
        elif cmd == "|":    # reverse direction (turn 180)
            data["angle"] += 180
        elif cmd == "[":    # save to stack
            stack.append(copy.deepcopy(data))
        elif cmd == "]":    # pop load from stack
            data = stack.pop()
        elif cmd == ">":    # multiply line length
            data["length"] *= settings["lfac"]
        elif cmd == "<":    # devide line length
            data["length"] /= settings["lfac"]
        elif cmd == "&":    # swap the meaning of + and -
            data["swap"] *= -1
        elif cmd == "(":    # decrement turning angle
            data["turning_angle"] += settings["ainc"]
        elif cmd == ")":    # increase turning angle
            data["turning_angle"] -= settings["ainc"]

    # calculate size
    normal_height = top_most - bottom_most
    normal_width = right_most - left_most

    scale_factor = 1
    if normal_height > normal_width:
        scale_factor = (WND_HEIGHT - 2 * WND_PADDING_H) / normal_height
    else:
        scale_factor = (WND_WIDTH - 2 * WND_PADDING_W) / normal_width

    # generate drawing data
    stack = []
    cells = []

    data = {
        "point": Vec2(0.0, 0.0),
        "cell_points": [Vec2(0.0, 0.0)],
        "cell_data": Cell.Data(),
        "length": scale_factor,
        "angle": 0.0,
        "turning_angle": settings["angle"],
        "swap": 1
    }

    data["cell_points"] = [copy.deepcopy(data["point"])]
    data["cell_data"].set(Cell.Data.WIDTH, 3)
    for cmd in structure:
        if cmd == "F":      # move forward, draw a line
            data["cell_data"].set(Cell.Data.DRAW, True)
            change = Vec2(data["length"], 0.0)
            change.rotate((90.0 + data["angle"]) * math.pi / 180)
            data["point"].add(change)
            data["cell_points"].append(copy.deepcopy(data["point"]))
            # save shit
            if not data["cell_data"].get(Cell.Data.POLYGON):
                cells.append(Cell(copy.deepcopy(data["cell_points"]), copy.deepcopy(data["cell_data"])))
                data["cell_points"] = [copy.deepcopy(data["point"])]
        elif cmd == "f":    # move forward, no line
            data["cell_data"].set(Cell.Data.DRAW, False)
            change = Vec2(data["length"], 0.0)
            change.rotate((90.0 + data["angle"]) * math.pi / 180)
            data["point"].add(change)
            data["cell_points"].append(copy.deepcopy(data["point"]))
            # save shit
            if not data["cell_data"].get(Cell.Data.POLYGON):
                cells.append(Cell(copy.deepcopy(data["cell_points"]), copy.deepcopy(data["cell_data"])))
                data["cell_points"] = [copy.deepcopy(data["point"])]
        elif cmd == "+":    # increments by an angle
            data["angle"] += data["swap"] * data["turning_angle"]
        elif cmd == "-":    # decrements by an angle
            data["angle"] -= data["swap"] * data["turning_angle"]
        elif cmd == "|":    # reverse direction (turn 180)
            data["angle"] += 180
        elif cmd == "[":    # save to stack
            stack.append(copy.deepcopy(data))
        elif cmd == "]":    # pop load from stack
            data = stack.pop()
            data["cell_points"].pop()
            data["cell_points"].append(copy.deepcopy(data["point"]))
        elif cmd == "#":    # increment width
            data["cell_data"].set(Cell.Data.WIDTH, int(data["cell_data"].get(Cell.Data.WIDTH) + settings["winc"]))
        elif cmd == "!":    # decrement width
            data["cell_data"].set(Cell.Data.WIDTH, int(data["cell_data"].get(Cell.Data.WIDTH) - settings["winc"]))
        elif cmd == "@":    # draw a dot r = line_width
            # save shit
            data["cell_data"].set(Cell.Data.DOT, True)
            cells.append(Cell([data["point"]], copy.deepcopy(data["cell_data"])))
            data["cell_data"].set(Cell.Data.DOT, False)
            pass
        elif cmd == "{":    # Open a polygon
            data["cell_data"].set(Cell.Data.POLYGON, True)
        elif cmd == "}":    # Close a polygon and fill with color (no setting for now)
            # save shit
            cells.append(Cell(copy.deepcopy(data["cell_points"]), copy.deepcopy(data["cell_data"])))
            data["cell_points"] = [copy.deepcopy(data["point"])]
            data["cell_data"].set(Cell.Data.POLYGON, False)
        elif cmd == ">":    # multiply line length
            data["length"] *= settings["lfac"]
            pass
        elif cmd == "<":    # devide line length
            data["length"] /= settings["lfac"]
        elif cmd == "&":    # swap the meaning of + and -
            data["swap"] *= -1
        elif cmd == "(":    # decrement turning angle
            data["turning_angle"] -= settings["ainc"]
        elif cmd == ")":    # increase turning angle
            data["turning_angle"] += settings["ainc"]

    TRANSFORM_X = int(-1 * left_most * scale_factor + WND_PADDING_W)
    TRANSFORM_Y = int(-1 * bottom_most * scale_factor + WND_PADDING_H - WND_HEIGHT)

    # drawing
    wnd = tkinter.Tk()
    wnd.minsize(WND_WIDTH, WND_HEIGHT)
    wnd.maxsize(WND_WIDTH, WND_HEIGHT)

    canvas = tkinter.Canvas(master=wnd, width=WND_WIDTH, height=WND_HEIGHT, background="white")
    canvas.pack()

    for cell in cells:
        for point in cell.points:
            point.to_ivec2()
        width = cell.data.get(Cell.Data.WIDTH)
        if cell.data.get(Cell.Data.DOT):
            canvas.create_oval(cell.points[0].x + TRANSFORM_X - width, -1 * (cell.points[0].y - width + TRANSFORM_Y),
                               cell.points[0].x + TRANSFORM_X + width, -1 * (cell.points[0].y + width + TRANSFORM_Y),
                               fill="lime", width=0)
        elif cell.data.get(Cell.Data.POLYGON):
            canvas.create_polygon([(e.x + TRANSFORM_X, -1 * (e.y + TRANSFORM_Y)) for e in cell.points], fill="cyan", width=0)
        else:
            canvas.create_line([(e.x + TRANSFORM_X, -1 * (e.y + TRANSFORM_Y)) for e in cell.points], width=width)

    wnd.mainloop()

    return 0


if __name__ == "__main__":
    code = main(argv)
    print("Exited with exit code:", code)
