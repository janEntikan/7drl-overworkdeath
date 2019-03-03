class Statset():
	def __init__(self):
		self.name = "wolverine"
		self.clas = "acountant"
		self.age = 18

		self.inventory = []
		self.spells = []
		self.skills = []
		self.weapon = None
		self.armor = None
		self.level = 1
		self.experience = 0
		self.next_level = 200

		self.hunger = 0
		self.thirst = 0

		self.hp = 10
		self.max_hp = 10
		self.sp = 10
		self.d = 0
		self.atk = 0
		self.status = "Normal"
		self.gem = (0,1,0)

		self.strength = 2
		self.accuracy = 2
		self.intelligence = 2
		self.personality = 2
		self.endurance = 2
		self.speed = 2
		self.luck = 2
		self.updateStats()

	def turn(self):
		self.hp += (0.04*self.endurance)
		self.hunger += 0.02
		self.thirst += 0.05

	def updateStats(self):
		if not self.status == "Dead":
			if self.hp > self.max_hp:
				self.hp = self.max_hp
			self.atk = self.strength
			self.d = int(self.endurance/2)
			if not self.weapon == None:
				self.atk += self.weapon.damage
				self.d += self.weapon.defence
			if not self.armor == None:
				self.d += self.armor.defence
			if self.hp < 1:
				self.status = "Dying"

	def attack(self, target):
		target.updateStats()
		atk = self.atk
		atk /= target.d
		if atk < 0: atk = 0
		atk = int(atk)
		target.hp -= atk
		output = self.name + " hits " + target.name + " for " + str(atk) + " d"
		game.hud.output.append(output)

		if target.hp < 1:
			output = target.name + " is killed."
			game.hud.output.append(output)
		target.updateStats()
