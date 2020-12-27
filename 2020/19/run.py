from copy import deepcopy
from parse import parse
import regex

def parse_base(buf):
    res = parse("{:d}: \"{}\"", buf)
    return {res[0]: res[1]}

def parse_and(buf):
    parts = [int(s.strip(":")) for s in buf.split(" ")]
    return {parts[0]: parts[1:]}

def parse_or(buf):
    halves = buf.split(":")
    i = int(halves[0])
    arms = halves[1].strip().split("|")
    parts = [[int(s) for s in arm.strip().split(" ")] for arm in arms]
    return {i: tuple(parts)}

def parse_line(buf):
    if "|" in buf:
        return parse_or(buf)
    elif "\"" in buf:
        return parse_base(buf)
    else:
        return parse_and(buf)

def raw_rules(f):
    raw = {}
    for d in (parse_line(l.strip()) for l in open(f)):
        raw.update(d)
    return raw

def parse_rules(raw):
    raw = deepcopy(raw)
    parsed = dict((k,v) for (k,v) in raw.items() if isinstance(v, str))
    for k in parsed.keys():
        del raw[k]

    while raw:
        known = set()
        for i, rule in raw.items():
            if isinstance(rule, list) and all(r in parsed for r in rule):
                parsed[i] = "".join("({})".format(parsed[r]) for r in rule)
                known.add(i)
            if isinstance(rule, tuple) and all(all(r in parsed or r == i for r in rr) for rr in rule):
                if any(i in rr for rr in rule):
                    # recursive!
                    pat = "pat{:d}".format(i)
                    inner = "|".join("".join("({})".format(parsed[r] if r != i else "(?&{})".format(pat)) for r in rr) for rr in rule)
                    full = "(?P<{}>{})".format(pat, inner)
                else:
                    full = "|".join("".join("({})".format(parsed[r]) for r in rr) for rr in rule)
                parsed[i] = full
                known.add(i)
        for i in known:
            del raw[i]
    return parsed 

parsed = parse_rules(raw_rules("rules.txt"))
pat = regex.compile(parsed[0])
msgs = open("messages.txt").read().splitlines()
print("Part 1:", len([m for m in msgs if regex.fullmatch(pat, m)]))

# Part 2

mod_rules = raw_rules("rules.txt")
mod_rules[8] = ([42], [42, 8])
mod_rules[11] = ([42, 31], [42, 11, 31])

parsed = parse_rules(mod_rules)
pat = regex.compile(parsed[0])
print("Part 2:", len([m for m in msgs if regex.fullmatch(pat, m)]))


