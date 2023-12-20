from .parser import ParserData
from .vec2 import Vec2
from .log import Log


class Structure:
    def __init__(self, string, data: ParserData) -> None:
        self.string = string
        self.data = data


def generate_structure(data: ParserData, complexity: int) -> Structure:
    string = data.axiom
    for _ in range(complexity):
        for key in data.rules.keys():
            string = string.replace(key, data.rules[key])
    return Structure(string, data)

