import copy
import re

from .log import Log


class ParserData:
    def __init__(self) -> None:
        self.axiom = ""
        self.rules = {}
        self.angle = 0.0
        self.width = 0.0
        self.lcolor = "#000000"
        self.pcolor = "#000000"
        self.dcolor = "#000000"
        self.winc = 0.0
        self.ainc = 0.0
        self.lfac = 0.0

    def __str__(self) -> str:
        return f"(axiom:{self.axiom}, rules:{self.rules}, angle:{self.angle}, winc:{self.winc}, ainc:{self.ainc}, lfac:{self.lfac})"


def parse(text: str) -> ParserData:
    NUMBER = "\d+(\.\d+)?"
    COLOR = "#[0-9a-fA-F]{6}"
    KEYWORD = "axiom|rules|angle|winc|lfac|ainc"
    CHARACTER = "[a-zA-Z+\-|[\]#!@{}<>&()]"
    VARIABLE = "\.[a-zA-Z]\w*"
    EXPRESSION = f"(?:{VARIABLE}|{CHARACTER})+"  # selects kinda everything

    source = copy.deepcopy(text)

    source = re.sub(";.*$", "", source, flags=re.RegexFlag.MULTILINE)    # remove comments

    # replacing variables
    vars = re.findall(f"{VARIABLE} {EXPRESSION}", source)
    vars = [e for e in vars if re.search(KEYWORD, e) is None]

    for var in vars:
        name, value = var.split()
        source = source.replace(var, "").replace(name, value)

    source = re.sub("\s+", " ", source)    # compact spaces
    # small stuff
    source = re.sub(" ?-> ?", "->", source)
    source = re.sub(" ?, ?", ",", source)
 
    # parsing
    data = ParserData()
    data.axiom = re.search(f"(axiom) ({CHARACTER}+)", source).group(2)

    # settings
    setting = re.search(f"(angle) ({NUMBER})", source)
    data.angle = float(setting.group(2)) if setting is not None else 60.0
    setting = re.search(f"(width) ({NUMBER})", source)
    data.width = float(setting.group(2)) if setting is not None else 3.0
    setting = re.search(f"(Fcol) ({COLOR})", source)
    data.lcolor = setting.group(2) if setting is not None else "#000000"
    setting = re.search(f"({{col) ({COLOR})", source)
    data.pcolor = setting.group(2) if setting is not None else "#0000ff"
    setting = re.search(f"(@col) ({COLOR})", source)
    data.dcolor = setting.group(2) if setting is not None else "#00ff00"
    setting = re.search(f"(winc) ({NUMBER})", source)
    data.winc = float(setting.group(2)) if setting is not None else 0.0
    setting = re.search(f"(ainc) ({NUMBER})", source)
    data.ainc = float(setting.group(2)) if setting is not None else 0.0
    setting = re.search(f"(lfac) ({NUMBER})", source)
    data.lfac = float(setting.group(2)) if setting is not None else 1.0

    # rules
    src_rules = re.search(f"(rules) ((,?[a-zA-Z]->{CHARACTER}+)+)", source).group(2)
    src_rules = src_rules.split(",")
    for rule in src_rules:
        if rule == "" or rule is None:
            Log.warning("rule was NULL")
            continue
        key, val = rule.split("->")
        data.rules[key] = val

    return data

