from panda3d.core import BitMask32
from random import choice
from .stats import Statset
from .tools import makeInstance
from .items import items

class Cam():
	def __init__(self, x, y, angle):
		base.camLens.setFov(90)
		base.camNode.setCameraMask(BitMask32.bit(0))
		base.camLens.setFar(20)
		base.camLens.setNear(0.01)
		self.node = render.attachNewNode("placement")
		self.camNode = self.node.attachNewNode("cam")
		self.camNode.set_pos((0,-0.4,0))
		base.camera.reparentTo(self.camNode)
		self.node.set_hpr(angle, 0, 0)
		self.node.set_pos(x+0.5,y+0.5,0.2)

	def update(self, place):
		self.node.set_hpr((place[2]*90)+180,0,0)
		self.node.set_pos(-place[0],-place[1],0.2)

class Player():
	def __init__(self, x, y, angle):
		self.camera = Cam(x,y,angle)
		self.rot_speed = 0.1
		self.mov_speed = 0.1
		self.place = [x,y,angle]
		self.prev_place = self.place[:]
		self.pos = self.place[0], self.place[1]
		self.target = None
		self.stats = Statset()
		w = items["randomweak"]()
		self.stats.name = "you"
		self.stats.inventory.append(w)
		self.stats.weapon = w
		self.stats.max_hp = 8
		self.stats.hp = 8
		self.stats.next_level = 100
		self.stats.updateStats()
		l = [[0,1], [-1,0], [0,-1], [1,0]]
		self.direction = l[int(round(self.place[2]))]

	def update(self):
		if self.stats.blind > 0:
			base.camLens.setFar(1)
		else:
			base.camLens.setFar(int(game.cfg["general"]["distance"]))
		self.camera.update(self.place)

	def turn(self, d):
		#increment angle
		self.place[2] += d*self.rot_speed
		self.place[2] = round(self.place[2], 2)
		#break when quarter turn made
		if self.place[2] == self.prev_place[2]+d:
			self.place[2] = self.place[2]%4
			self.prev_place = self.place[:]
			l = [[0,1], [-1,0], [0,-1], [1,0]]
			self.direction = l[int(round(self.place[2]))]
			return 1

	def move(self, d):
		#get angle
		x, y, angle = self.prev_place
		l = [[0,-d], [d,0], [0,d], [-d,0]]
		s = l[int(self.place[2])]
		current = game.map.grid[int(y)][int(x)]
		mx = int(x+s[0])
		my = int(y+s[1])
		enemythere = False
		self.target = None
		for enemy in game.map.enemies:
			if enemy.pos[0] == mx and enemy.pos[1] == my:
				self.target = enemy
				if not self.target.stats.status == "Dead" and not self.target.stats.status == "Dying":
					return "melee"
		self.pos = mx, my
		try:
			dest = game.map.grid[my][mx]
		except:
			pass
		#hittesting
		if dest.c == "." or dest.c == "+" or dest.c == "=" or dest.c == "<":
			move = True
			if move:
				#increment movement
				self.place[0] += s[0]*self.mov_speed
				self.place[1] += s[1]*self.mov_speed
				self.place[0] = round(self.place[0],2)
				self.place[1] = round(self.place[1],2)
				#and break when full step made
				if self.place[0] == self.prev_place[0]+s[0]:
					if self.place[1] == self.prev_place[1]+s[1]:
						self.prev_place = self.place[:]
						game.sounds["step_player"].play()
						return 1
			else:
				return 1
		else:
			return "cancel"

	def throw(self, item):
		game.hud.output.append("you throw the " + item.name)
		if self.stats.weapon == item:
			self.stats.weapon = None
		self.stats.inventory.remove(item)
		x, y = self.pos[0], self.pos[1]
		for i in range(int((self.stats.strength+self.stats.accuracy)/4)+1):
			tile = game.map.grid[y+self.direction[1]][x+self.direction[0]]
			solids = "#W$"
			if tile.c in solids:
				game.hud.output.append("the " + item.name + " hits the wall")
				tile = game.map.grid[y][x]
				if not tile.item == None:
					tile.item[0].removeNode()
				n = makeInstance(item.cat, game.item_models[item.cat], pos=(-x,-y,0))
				n.reparentTo(game.map.node)
				n.setBillboardPointEye()
				tile.item = [n, item]
				return
			else:
				for enemy in game.map.enemies:
					if int(enemy.pos[0]) == x and int(enemy.pos[1]) == y:
						item.hit(self.stats, enemy.stats)
				x += self.direction[0]
				y += self.direction[1]

		tile = game.map.grid[y][x]
		if not tile.item == None:
			tile.item[0].removeNode()
		n = makeInstance(item.cat, game.item_models[item.cat], pos=(-x,-y,0))
		n.reparentTo(game.map.node)
		n.setBillboardPointEye()
		tile.item = [n, item]
		game.hud.output.append("the " + item.name + " drops on the floor")

	def drop(self, item):
		tile = game.map.grid[self.pos[1]][self.pos[0]]
		if tile.item == None:
			if self.stats.weapon == item:
				self.stats.weapon = None
			self.stats.inventory.remove(item)
			n = makeInstance(item.cat, game.item_models[item.cat], pos=(-self.pos[0],-self.pos[1],0))
			n.reparentTo(game.map.node)
			n.setBillboardPointEye()
			tile.item = [n, item]
			game.hud.output.append("you drop the " + item.name)
			return True
		else:
			game.hud.output.append("there's something here already")
			return False

	def fire(self):
		game.delay = 10
		if not self.stats.weapon == None:
			if not self.stats.weapon.ranged:
				game.hud.output.append("you can't fire a " + self.stats.weapon.name)
				return False
		else:
			game.hud.output.append("you're not holding a weapon to fire")
			return False
		game.hud.output.append("you fire the " + self.stats.weapon.name)
		a = choice("abc")
		game.sounds["projectile_"+a].play()
		game.transition.setFadeColor(0.1,0.1,0.1)
		game.transition.fadeOut(0.1)
		game.transition.fadeIn(0.01)
		x, y = self.pos[0], self.pos[1]
		for i in range(int((self.stats.accuracy*2))):
			tile = game.map.grid[y+self.direction[1]][x+self.direction[0]]
			solids = "#W$"
			if tile.c in solids:
				game.hud.output.append("you didn't hit anything")
				return True
			else:
				for enemy in game.map.enemies:
					if enemy.pos[0] == x and enemy.pos[1] == y:
						self.stats.attack(enemy.stats, False, True)
						return True
				x += self.direction[0]
				y += self.direction[1]
		game.hud.output.append("you didn't hit anything")
		return True
