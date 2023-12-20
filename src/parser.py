import copy
import re

from .log import Log


class ParserData:
    def __init__(self) -> None:
        self.axiom = ""
        self.rules = {}
        self.angle = 0.0
        self.winc = 0.0
        self.ainc = 0.0
        self.lfac = 0.0

    def __str__(self) -> str:
        return f"(axiom:{self.axiom}, rules:{self.rules}, angle:{self.angle}, winc:{self.winc}, ainc:{self.ainc}, lfac:{self.lfac})"


def parse(text: str) -> ParserData:
    source = copy.deepcopy(text)

    source = re.sub(";.*$", "", source, flags=re.RegexFlag.MULTILINE)    # remove comments
    source = re.sub("[ \t]*[\n\r]+[ \t]*", "$", source, flags=re.RegexFlag.MULTILINE)    # replace new lines with $
    source = re.sub("\s+", " ", source, flags=re.RegexFlag.MULTILINE)    # compact spaces

    KEYWORD = "axiom|rules|angle|winc|lfac|ainc"
    CHARACTER = "[a-zA-Z+\-|[\]#!@{}<>&()]"
    VARIABLE = "\.[a-zA-Z]\w*"
    EXPRESSION = f"(?:{VARIABLE}|{CHARACTER})+"  # selects kinda everything

    # replacing variables
    vars = re.findall(f"\${VARIABLE} {EXPRESSION}", source)
    vars = [e for e in vars if re.search(KEYWORD, e) is None]
    for var in vars:
        name, value = var.split()
        name = name.replace("$", "")
        source = source.replace(var, "").replace(name, value)
 
    # parsing
    data = ParserData()
    data.axiom = re.search(f"\$(axiom) ({EXPRESSION})", source).group(2)

    # settings
    setting = re.search(f"\$(angle) (\d+(\.\d+)?)", source)
    data.angle = float(setting.group(2)) if setting is not None else 60.0
    setting = re.search(f"\$(winc) (\d+(\.\d+)?)", source)
    data.winc = float(setting.group(2)) if setting is not None else 0.0
    setting = re.search(f"\$(ainc) (\d+(\.\d+)?)", source)
    data.ainc = float(setting.group(2)) if setting is not None else 0.0
    setting = re.search(f"\$(lfac) (\d+(\.\d+)?)", source)
    data.lfac = float(setting.group(2)) if setting is not None else 1.0

    # rules
    src_rules = re.search(f"\$(rules)((\$?[a-zA-Z] -> {EXPRESSION}(, )?)+)", source).group(2)
    src_rules = re.split("(, ?)|\$", src_rules)
    for rule in src_rules:
        if rule == "" or rule is None:
            continue
        key, val = rule.split("->")
        data.rules[key.replace(" ", "")] = val.replace(" ", "")

    return data

