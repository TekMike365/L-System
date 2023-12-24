import copy
import math

from .vec2 import Vec2
from .log import Log

from .structure import Structure
from .parser import ParserData
from .window import Window


class IndexData:
    def __init__(self, width, indexes=[]):
        self.width = width
        self.indexes = indexes


class RenderData:
    def __init__(self, vertices, index_data: IndexData) -> None:
        self.vertices = vertices
        self.index_data = index_data


def generate_renderdata(struct: Structure) -> RenderData:
    data = {
        "pos": Vec2(0.0, 0.0),
        "posi": 0, # position index
        "alpha": 0.0,
        "len": 1.0,
        "width": copy.deepcopy(struct.data.width),
        "swap": 1,
        "angle": copy.deepcopy(struct.data.angle),
        "winc": copy.deepcopy(struct.data.winc),
        "ainc": copy.deepcopy(struct.data.ainc),
        "lfac": copy.deepcopy(struct.data.lfac),
    }

    prev_pos = 0
    curr_pos = 0
    stack = []
    polygon = False

    vertices = [Vec2(0.0, 0.0)]
    indexes_data = []

    for cmd in struct.string:
        if cmd == "F" or cmd == "f":
            prev_pos = data["posi"]
            change = Vec2(0.0, data["len"])
            change.rotate(data["alpha"] * math.pi / 180)
            data["pos"].add(change)
            vertices.append(copy.deepcopy(data["pos"]))
            curr_pos = len(vertices) - 1
            data["posi"] = curr_pos

        if cmd == "F": # move forward without drawing
            if polygon:
                indexes_data[-1].indexes.append(curr_pos)
                continue
            indexes_data.append(IndexData(data["width"], [prev_pos, curr_pos]))
        elif cmd == "f": # move forward without drawing
            if polygon:
                continue
        elif cmd == "+": # increments by an angle
            data["alpha"] +=data["swap"] * data["angle"]
        elif cmd == "-": # decrements by an angle
            data["alpha"] -= data["swap"] * data["angle"]
        elif cmd == "|": # reverse direction (turn 180)
            data["angle"] += 180.0
        elif cmd == "[": # save to stack
            stack.append(copy.deepcopy(data))
        elif cmd == "]": # pop from stack
            data = stack.pop()
        elif cmd == ">": # multiply line length
            data["len"] *= data["lfac"]
        elif cmd == "<": # devide line length
            data["len"] /= data["lfac"]
        elif cmd == "&": # swap the meaning of + and -
            data["swap"] *= -1
        elif cmd == "(": # decrement turning angle
            data["angle"] += data["ainc"]
        elif cmd == ")": # increase turning angle
            data["angle"] -= data["ainc"]
        elif cmd == "@":    # draw a dot r = line_width
            indexes_data.append(IndexData(data["width"], indexes=[curr_pos]))
        elif cmd == "{": # Open a polygon
            polygon = True
            indexes_data.append(IndexData(data["width"], [curr_pos]))
        elif cmd == "}": # Close a polygon and fill with color (no setting for now)
            polygon = False

    return RenderData(vertices, indexes_data)


def transform_renderdata(wnd: Window, renderdata: RenderData) -> RenderData:
    data = copy.deepcopy(renderdata)

    left = 0
    right = 0
    top = 0
    bottom = 0

    for pos in data.vertices:
        left = min(left, pos.x)
        right = max(right, pos.x)
        top = max(top, pos.y)
        bottom = min(bottom, pos.y)

    width = right + abs(left)
    height = top + abs(bottom)

    width_scalar = wnd.width / width
    height_scalar = wnd.height / height
    scalar = min(width_scalar, height_scalar)

    offset_x = wnd.width / 2 - scalar * (right + left) / 2
    offset_y = wnd.height / 2 - scalar * (top + bottom) / 2

    for pos in data.vertices:
        pos.scale(scalar)
        pos.add(Vec2(offset_x, offset_y))

    return data


def render(wnd: Window, struct: Structure) -> None:
    data = generate_renderdata(struct)
    data = transform_renderdata(wnd, data)

    for e in data.index_data:
        if len(e.indexes) == 1: # point
            point = data.vertices[e.indexes[0]]
            wnd.draw_point(point, e.width * 2, struct.data.dcolor)
        elif len(e.indexes) == 2: # line
            p1 = data.vertices[e.indexes[0]]
            p2 = data.vertices[e.indexes[1]]
            wnd.draw_line(p1, p2, e.width, struct.data.lcolor)
        elif len(e.indexes) > 2: # polygon
            points = [data.vertices[i] for i in e.indexes]
            wnd.draw_polygon(points, struct.data.pcolor)
        else:
            Log.warning(f"empty indexes")

