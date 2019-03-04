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
		self.xp = 0
		self.next_level = 10000000000

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
		self.hp += (0.1)
		self.hunger += 0.02
		self.thirst += 0.05

	def updateStats(self):
		if not self.status == "Dead":
			if self.xp >= self.next_level:
				s = self.name + " gained a level!"
				game.hud.output.append(s)
				self.level += 1
				self.next_level *= 1.9
				self.nex_level = int(self.next_level)
				self.strength += 1
				self.accuracy += 1
				self.intelligence += 1
				self.personality += 1
				self.endurance += 1
				self.speed += 1
				self.luck += 1
				self.max_hp += self.level
				self.hp += self.level

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
		if not target.status == "Dying" and not target.status == "Dead":
			target.updateStats()
			atk = self.atk
			try:
				atk /= target.d
			except:
				pass
			if atk < 0: atk = 0
			atk = int(atk)
			if atk == 0: atk = 1
			target.hp -= atk
			output = self.name + " hits " + target.name + " for " + str(atk) + " d"
			game.hud.output.append(output)

			if target.hp < 1:
				self.xp += target.xp
			target.updateStats()
			self.updateStats()
