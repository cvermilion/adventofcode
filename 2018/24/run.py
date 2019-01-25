immune_data = open("immune.txt").readlines()
infection_data = open("infection.txt").readlines()

# ugh, parsing the weakness/immunity would be a pain
from parse import parse
fmt = "{:d} units each with {:d} hit points ({:s}) with an attack that does {:d} {} damage at initiative {:d}\n"
fmt1 = "{:d} units each with {:d} hit points "
fmt2 = " with an attack that does {:d} {} damage at initiative {:d}\n"

class Group (object):
	def __init__(self, typ, units, hp, damage, attack_type, initiative, weaknesses=None, immunities=None):
		self.type = typ
		self.units = units
		self.hp = hp
		self.damage = damage
		self.attack_type = attack_type
		self.initiative = initiative
		self.weaknesses = weaknesses
		self.immunities = immunities
		self.target = None
		self.targeted_by = None

def parse_mod_string(s):
	weaknesses, immunities = set(), set()
	parts = s.split("; ")
	for p in parts:
		if p.startswith("immune to "):
			immunities = p[10:].split(", ")
		if p.startswith("weak to "):
			weaknesses = p[8:].split(", ")
	return set(weaknesses), set(immunities)

def power(attacker, boost):
	dmg = attacker.damage
	if attacker.type == "imm":
		dmg += boost
	return dmg * attacker.units
	
def damage(attacker, target, boost):
		if attacker.attack_type in target.immunities:
			return 0
		p = power(attacker, boost)
		if attacker.attack_type in target.weaknesses:
			return 2*p
		return p

parsed_immune_data = []
parsed_infection_data = []
for (typ, parsed_data, army_data) in [("imm", parsed_immune_data, immune_data), ("inf", parsed_infection_data, infection_data)]:
	for data in army_data:
		if "(" in data:
			part1, rest = data.split("(")
			mods, part2 = rest.split(")")
		else:
			part1, part2 = data.split("points")
			part1 += "points "
			mods = ""
		res1 = parse(fmt1, part1)
		res2 = parse(fmt2, part2)
		weak, imm = parse_mod_string(mods)
		parsed_data.append((res1, res2, weak, imm))

# returns margin of immune victory/loss
def immune_victory(boost):
	immune_army = []
	infection_army = []
	for (typ, army, parsed_data) in [("imm", immune_army, parsed_immune_data), ("inf", infection_army, parsed_infection_data)]:
		for (res1, res2, weak, imm) in parsed_data:
			units, hp = res1.fixed
			dmg, attack, initiative = res2.fixed
			army.append(Group(typ, units, hp, dmg, attack, initiative, weak, imm))
		
	while immune_army and infection_army:
		all_armies = immune_army + infection_army
		all_armies = list(reversed(sorted(all_armies, key=lambda g: (power(g,boost), g.initiative))))
		
		# reset targets
		for g in all_armies:
			g.target = None
			g.targeted_by = None
		
		# choose targets
		for attacker in all_armies:
			targets = [g for g in all_armies if g.type != attacker.type and g.targeted_by == None]
			
			if targets:
				targets = sorted(targets, key=lambda g: (damage(attacker,g,boost),power(g,boost),g.initiative))
				target = targets[-1]
				if damage(attacker, target, boost) != 0:
					attacker.target = target
					target.targeted_by = attacker
					#print("target:",attacker,target)
		
		total = sum([g.units for g in immune_army]), sum([g.units for g in infection_army])
		
		# ATTACK
		attackers = [g for g in all_armies if g.units and g.target]
		if not attackers:
			print("deadlock, no one can attack")
			return -1
		attackers = list(reversed(sorted(attackers, key=lambda g:g.initiative)))
		for attacker in attackers:
			target = attacker.target
			dmg = damage(attacker, target, boost)
			loss = int(dmg / target.hp)
			#print("loss:",loss)
			target.units = max([0, target.units-loss])
		
		immune_army = [g for g in immune_army if g.units]
		infection_army = [g for g in infection_army if g.units]
		
		total2 = sum([g.units for g in immune_army]), sum([g.units for g in infection_army])
		#print(total, total2)
		if total2 == total:
			print("didnt change!")
			# count a deadlock as an immune loss
			return -1
		
		#print(sum([g.units for g in immune_army]), sum([g.units for g in infection_army]))
	
	return sum([g.units for g in immune_army]) - sum([g.units for g in infection_army])

# part 1
print(-immune_victory(0))

# part 2

# double boost until we find an upper bound
boost=1
while True:
	x = immune_victory(boost)
	print(boost, x)
	if x > 0:
		break
	boost*=2

bmin,bmax = int(boost/2), boost
print(bmin,bmax)

while bmax - bmin > 1:
	mid = bmin + int((bmax-bmin)/2)
	x = immune_victory(mid)
	if x > 0:
		bmax = mid
	else:
		bmin = mid
	print(bmin,bmax,x)
	

print(x)
