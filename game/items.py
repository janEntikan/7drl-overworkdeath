from random import randint, choice
from .tools import randExpo

items = {}
class Item():
	def __init__(self):
		self.cat = "item"
		self.name = "item"
	def use(self, user):
		game.hud.output.append("you use the item")
	def update(self):
		pass

class Weapon(Item):
	def __init__(self):
		Item.__init__(self)
		self.cat = "weapon"
		self.type = "weapon"
		self.name = "weapon"
		self.ranged = False
		self.verb = "wield"
		self.intelect = 1
		self.damage = 0
		self.defence = 0

	def hit(self, user, target):
		acc = int(user.accuracy - (target.speed/2))
		if acc > 0 or randint(0,1) == 0:
			if self.ranged:
				d = int(self.damage/2)
			else:
				d = int(self.damage*2)
			if d <= 0:
				d = 1
			target.hp -= d
			game.hud.output.append("it hits " + target.name + " for " + str(d) + " d")
			if target.hp < 0:
				output = target.name + " is killed."
				game.hud.output.append(output)
				self.xp += target.xp
		else:
			d = choice((" by a hair.", " by an inch.", " by a bit."))
			game.hud.output.append("it misses " + target.name + d)

	def use(self, user):
		if user.stats.intelect < self.intelect:
			game.hud.output.append("you're not smart enough to wield the " + self.name)
		else:
			if not user.stats.weapon == None:
				if user.stats.weapon == self:
					game.hud.output.append("already wielding the " + user.stats.weapon.name)
					return False
				else:
					game.hud.output.append("you unwield the " + user.stats.weapon.name)
			user.stats.weapon = self
			game.hud.output.append("you wield the " + user.stats.weapon.name)
			return True
		return False
# RANGED
class PenDispenser(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "pendispenser"
		self.name = "pocketprotector"
		self.damage = 1
		self.intelect = 1
		self.ranged = True
items["pendispenser"] = PenDispenser

class StapleGun(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "staplegun"
		self.name = "staple gun"
		self.damage = 2
		self.intelect = 1
		self.ranged = True
items["staplegun"] = StapleGun

class Flamethrower(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "flamethrower"
		self.name = "makeshift flamethrower"
		self.damage = 4
		self.intelect = 5
		self.ranged = True
items["flamethrower"] = Flamethrower

class NailGun(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "nailgun"
		self.name = "nail-gun"
		self.damage = 5
		self.intelect = 3
		self.ranged = True
items["nailgun"] = NailGun

class Handgun(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "handgun"
		names = "Revolver", "Desert Eagle", "Beretta", "Glock"
		self.name = choice(names)
		self.damage = 6
		self.intelect = 5
		self.ranged = True
items["handgun"] = Handgun

class Shotgun(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "shotgun"
		self.name = "Shotgun"
		self.damage = 7
		self.intelect = 7
		self.ranged = True
items["shotgun"] = Shotgun

class MachineGun(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "machinegun"
		self.name = "Machine Gun"
		self.damage = 8
		self.intelect = 9
		self.ranged = True
items["machinegun"] = MachineGun

# MELEE
class RandomWeak(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "randomweak"
		names = "letter-opener", "screwdriver", "pair of scissors", "suitcase"
		self.name = choice(names)
		self.damage = 2
		self.intelect = 1
items["randomweak"] = RandomWeak

class RandomMed(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "randommed"
		names = "hammer", "broom", "perforator"
		self.name = choice(names)
		self.damage = 6
		self.intelect = 2
items["randommed"] = RandomMed

class Boxcutter(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "boxcutter"
		self.name = "boxcutter"
		self.damage = 4
		self.intelect = 2
items["boxcutter"] = Boxcutter

class PapercutterSword(Weapon):
	def __init__(self):
		Weapon.__init__(self)
		self.cat = "papercutter"
		self.name = "papercutter sword"
		self.damage = 5
		self.intelect = 4
items["papercutter"] = PapercutterSword

# CONSUMABLES
class Consumable(Item):
	def __init__(self):
		Item.__init__(self)
		self.cat = "consumable"
		self.type = "consumable"
		self.name = "consumable"
		self.verb = "use"
		self.ranged = False
	def use(self, user):
		game.hud.output.append("You consume the " + self.name)

	def hit(self, user, target):
		acc = int(user.accuracy - (target.speed/2))
		if acc > 0 or randint(0,1) == 0:
			d = int(2)
			target.hp -= d
			game.hud.output.append("it hits " + target.name + " for " + str(d) + " d")
			game.transition.setFadeColor(0.1,0.1,0.1)
			game.transition.fadeOut(0.1)
			game.transition.fadeIn(0.01)
			if target.hp < 0:
				output = target.name + " is killed."
				game.hud.output.append(output)
				self.xp += target.xp

class Thermos(Consumable):
	def __init__(self):
		Consumable.__init__(self)
		self.cat = "thermos"
		self.contents = choice(("coffee", "tea", "chocolate"))
		self.name = "thermos (" + self.contents + ")"
		self.verb = "quaff"

	def use(self, user):
		user.stats.thirst = 0
		user.stats.inventory.remove(self)
		game.hud.output.append("you drank from the " + self.name)
		game.hud.output.append("it was filled with " + self.contents)
		dif = 20
		if self.contents == "coffee":
			user.stats.speedboost = dif
			game.hud.output.append("you feel super fast")
		elif self.contents == "tea":
			user.stats.hp = user.stats.max_hp
			game.hud.output.append("you feel revitalized")
		elif self.contents == "chocolate":
			if randint(0, 5) == 0:
				user.stats.poison = dif
				user.stats.status = "Poisoned"
				game.hud.output.append("it burns in your stomach")
			elif randint(0, 5) == 0:
				user.stats.blind = dif
				user.stats.status = "Blinded"
				game.hud.output.append("your eyes suddenly don't work")
			elif randint(0, 5) == 0:
				user.stats.status = "warm"
				game.hud.output.append("you feel nice and warm")
			elif randint(0, 5) == 0:
				user.stats.poison = 0
				user.stats.blind = 0
				user.stats.status = "Normal"
				game.hud.output.append("you feel cured")
			elif randint(0, 5) == 0:
				user.stats.xp = user.stats.nextLevel+50
				game.hud.output.append("you feel improved")
			else:
				user.stats.hp = user.stats.max_hp
				game.hud.output.append("you feel revitalized")
		return True
items["thermos"] = Thermos

class Softdrink(Consumable):
	def __init__(self):
		Consumable.__init__(self)
		self.cat = "softdrink"
		self.contents = choice(("red", "yellow", "orange", "green", "blue", "purple"))
		self.name = self.contents + " softdrink"
		self.verb = "quaff"

	def update(self):
		if game.drinks[self.contents][1]:
			self.name = self.contents + " softdrink (" +  game.drinks[self.contents][0] + ")"

	def use(self, user):
		dif = 20
		user.stats.inventory.remove(self)
		user.stats.thirst = 0
		if user.stats.thirst < 0:
			user.stats.thirst = 0
		game.hud.output.append("you drank the " + self.name)
		drink = game.drinks[self.contents]
		drink[1] = True
		if drink[0] == "health":
			user.stats.hp = user.stats.max_hp
			game.hud.output.append("you feel revitalized")
		elif drink[0] == "cure":
			user.stats.poison = 0
			user.stats.blind = 0
			user.stats.status = "Normal"
			game.hud.output.append("you feel cured")
		elif drink[0] == "poison":
			user.stats.poison = dif
			user.stats.status = "Poisoned"
			game.hud.output.append("it burns in your stomach")
		elif drink[0] == "blind":
			user.stats.blind = dif
			user.stats.status = "Blinded"
			game.hud.output.append("your eyes suddenly don't work")
		elif drink[0] == "improve":
			user.stats.xp = user.stats.next_level+50
			game.hud.output.append("you feel improved")
		elif drink[0] == "warmth":
			user.stats.status = "warm"
			game.hud.output.append("you feel nice and warm")
		return True
items["softdrink"] = Softdrink

class Snack(Consumable):
	def __init__(self):
		Consumable.__init__(self)
		self.cat = "snack"
		self.snacktypes = ("candybar","bag of chips","cookie","box of raisins","bag of nuts","sandwich")
		self.snacktype = randExpo(0,len(self.snacktypes)-1)
		self.contents = self.snacktypes[self.snacktype]
		self.name = self.contents
		self.verb = "eat"

	def use(self, user):
		user.stats.inventory.remove(self)
		user.stats.hunger -= (self.snacktype*5)
		user.stats.hp += self.snacktype
		if user.stats.hunger < 0:
			user.stats.hunger = 0
		game.hud.output.append("you ate the " + self.name)
		d = choice(("mmm, such rich texture and flavor!", "mmm, so succulent and savory!", "mmm, saline but not salty"))
		game.hud.output.append(d)
		return True
items["snack"] = Snack
