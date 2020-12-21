from parse import parse

data = open("input.txt").read()
passports = data.split("\n\n")
passports = [p.split() for p in passports]
passports = [dict(part.split(":") for part in p) for p in passports]

req_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"] #, "cid"]

def check_pp(p):
    return all(k in p for k in req_keys)

def check_pp2(p):
    if not check_pp(p): return False
    byr = p.get("byr")
    if len(byr) != 4 or byr < "1920" or byr > "2002": return False

    iyr = p.get("iyr")
    if len(iyr) != 4 or iyr < "2010" or iyr > "2020": return False

    eyr = p.get("eyr")
    if len(eyr) != 4 or eyr < "2020" or eyr > "2030": return False
    
    hgt = p.get("hgt")
    parts = parse("{:d}{}", hgt)
    if parts[1] != "cm" and parts[1] != "in": return False
    if parts[1] == "cm" and (parts[0] < 150 or parts[0] > 193): return False
    if parts[1] == "in" and (parts[0] < 59 or parts[0] > 76): return False

    hcl = p.get("hcl")
    if len(hcl) != 7 or hcl[0] != "#" or any([c not in "abcdef0123456789" for c in hcl[1:]]): return False

    ecl = p.get("ecl")
    if ecl not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]: return False

    pid = p.get("pid")
    if len(pid) != 9 or any(c not in "0123456789" for c in pid): return False

    return True

print("Part 1: ", sum(1 if check_pp(p) else 0 for p in passports))
print("Part 2: ", sum(1 if check_pp2(p) else 0 for p in passports))

