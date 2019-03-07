from random import randint

class Statset():
	def __init__(self):
		self.name = "wolverine"
		self.clas = "acountant"
		self.age = 18
		self.money = 0
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

		self.hp = 5
		self.max_hp = 5
		self.sp = 10
		self.d = 0
		self.atk = 0
		self.status = "Normal"
		self.poison = 0
		self.blind = 0
		self.speedboost = 0
		self.strength = 1
		self.accuracy = 1
		self.intelect = 1
		self.endurance = 1
		self.speed = 1
		self.luck = 1
		self.updateStats()

	def turn(self):
		self.hp += (0.05)
		self.hunger += 0.02
		self.thirst += 0.05

	def updateStats(self):
		if not self.status == "Dead":
			if self.thirst == 10:
				game.hud.output.append("your mouth feels dry")
			if self.thirst == 20:
				game.hud.output.append("you feel very thirsty")
			if self.thirst > 30:
				self.thirst = 30
				self.hp -= 1
				game.transition.setFadeColor(0.0,0.0,0.1)
				game.transition.fadeOut()
				game.transition.fadeIn(0.2)
				game.hud.output.append("water...water...thirst!")

			if self.hunger == 10:
				game.hud.output.append("your stomach makes a noise")
			if self.hunger == 20:
				game.hud.output.append("you are quite hungry")
			if self.hunger > 30:
				self.hunger = 30
				self.hp -= 1
				game.transition.setFadeColor(0.1,0.0,0.1)
				game.transition.fadeOut()
				game.transition.fadeIn(0.2)
				game.hud.output.append("food...roomservice...hunger!")
			if self.speedboost > 0:
				self.status = "Caffeinated"
				self.speedboost -= 1
				if self.speedboost == 0:
					game.hud.output.append("the coffee stopped working")
					self.status = "Normal"
			else:
				self.speedboost = 0

			if self.blind > 0:
				self.status = "Blind"
				self.blind -= 1
				if self.blind == 0:
					game.hud.output.append("you can see once again")
					self.status = "Normal"
			else:
				self.blind = 0

			if self.poison > 0:
				self.status = "Poisoned"
				self.poison -= 1
				if self.poison <= 0 or self.hp <= 3:
					game.hud.output.append("the burning stopped")
					self.status = "Normal"
				else:
					self.hp -= 2
					game.transition.setFadeColor(0,0.1,0)
					game.transition.fadeOut(0.1)
					game.transition.fadeIn(0.1)
					game.hud.output.append("you are hurt by a burning sensation")
			else:
				self.poison = 0

			if self.xp >= self.next_level:
				s = self.name + " gained a level!"
				game.hud.output.append(s)
				self.level += 1
				self.next_level += self.level*100
				self.nex_level = int(self.next_level)
				dif = 1
				self.strength += randint(0, dif)
				self.accuracy += randint(0, dif)
				self.intelect += randint(0, dif)
				self.endurance += randint(0, dif)
				self.speed += randint(0, dif)
				self.luck += randint(0, dif)
				self.max_hp += int(self.level/4)+1
				self.hp += self.level
			if self.hp > self.max_hp:
				self.hp = self.max_hp
			self.atk = int(self.strength/4)+1
			self.d = int(self.endurance/2)
			if not self.weapon == None:
				self.atk += self.weapon.damage
				self.d += self.weapon.defence
			if not self.armor == None:
				self.d += self.armor.defence
			if self.hp < 1:
				self.status = "Dying"

	def get_hit(self, firer, weapon):
		self.updateStats()
		target.updateStats()
		atk = weapon.damage/self.d

	def attack(self, target, is_player=False, ranged=False):
		self.updateStats()
		target.updateStats()
		if not target.status == "Dying" and not target.status == "Dead":
			acc = int(self.accuracy - (target.speed/2))
			if acc > 0 or randint(0,1) == 0:
				atk = self.atk
				if ranged == False:
					if not self.weapon == None:
						if self.weapon.ranged == True:
							atk = int(self.atk/2)

				try:
					atk /= target.d
				except:
					pass
				if atk < 0: atk = 0
				atk = int(atk)
				if atk == 0: atk = 1
				target.hp -= atk
				if is_player:
					output = "You hit " + target.name + " for " + str(atk) + " damage"
				else:
					output = self.name + " hits " + target.name + " for " + str(atk) + " damage"
				game.hud.output.append(output)
				if target.hp < 1:
					output = target.name + " is killed."
					game.hud.output.append(output)
					self.xp += target.xp
			else:
				output = self.name + " missed!"
				game.hud.output.append(output)
		target.updateStats()
		self.updateStats()
