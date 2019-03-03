from panda3d.core import NodePath
from .tools import towardSpeed, makeInstance, getDistance
from .stats import Statset
from .enemies import enemy_stats

def flow_field(start_tile, target_tile):
	marks = {target_tile: 0}
	last_step_marked = [target_tile]
	current_mark = 0
	number_tries = 0
	while start_tile not in marks:
		current_mark += 1
		newly_marked_tiles = []
		new_neighbors = set()
		for tile in last_step_marked:
			for new_neighbor in tile.neighbors:
				new_neighbors.add(new_neighbor)
		for new_neighbor in new_neighbors:
			marks[new_neighbor] = current_mark
			newly_marked_tiles.append(new_neighbor)
		last_step_marked = newly_marked_tiles
		number_tries += 1
		if number_tries > 32:
			break
	lower = start_tile
	for neighbor in start_tile.neighbors:
		try:
			if marks[neighbor] == marks[lower]:
				if randint(0,1) == 0:
					lower = neighbor
			elif marks[neighbor] < marks[lower]:
				lower = neighbor
		except:
			pass
	return lower

class Enemy():
	def __init__(self, type, map, pos=[0,0]):
		self.map = map
		self.mov_speed = 0.1
		self.pos = pos
		self.prev_pos = pos
		self.type = type
		self.destination = None
		self.next_tile = None
		self.stats = enemy_stats[self.type]()
		self.node = NodePath("enemy_"+self.stats.name)
		self.speed = [0,self.stats.speed]

	def load(self, models):
		self.frames = {}
		self.frames["idle"] = makeInstance(self.type+"_IDLE", models[self.type+"_IDLE"])
		self.frames["hurt"] = makeInstance(self.type+"_HURT", models[self.type+"_HURT"])
		self.frames["dying"] = makeInstance(self.type+"_DYING", models[self.type+"_DYING"])
		self.frames["stepa"] = makeInstance(self.type+"_STEPA", models[self.type+"_STEPA"])
		self.frames["stepb"] = makeInstance(self.type+"_STEPB", models[self.type+"_STEPB"])
		self.frames["attack"] = makeInstance(self.type+"_ATTACK", models[self.type+"_ATTACK"])
		self.switchFrame("idle")
		self.node.setPos(-self.pos[0], -self.pos[1], 0)

	def switchFrame(self, framename):
		for frame in self.frames:
			if not frame == framename:
				self.frames[frame].detachNode()
			else:
				self.frames[frame].reparentTo(self.node)

	def update(self, game):
		if self.stats.status == "Dying":
			self.switchFrame("dying")
			game.delay = 10
			self.stats.status = "Dead"
			return 0
		if self.stats.status == "Dead":
			self.node.hide()
			game.map.enemies.remove(self)
			return 0

	def plan(self, game, ei):
		self.speed[0] -= 1
		if self.speed[0] <= 0:
			self.speed[0] = self.speed[1]
			return False

		sx, sy = self.pos
		self.prev_pos = [sx, sy]
		px, py = game.player.pos
		tspeed = towardSpeed(sx, sy, px, py)
		look=True
		while look:
			sx -= tspeed[0]
			sy -= tspeed[1]
			checkTile = game.map.grid[round(sy)][round(sx)]
			if checkTile.c == "W" or checkTile.c == "#":
				look=False
			elif round(sx) == px and  round(sy) == py:
				self.destination = [px, py]


		if not self.destination == None:
			start = game.map.grid[int(self.pos[1])][int(self.pos[0])]
			target = game.map.grid[self.destination[1]][self.destination[0]]
			self.next_tile = flow_field(start, target)
			enemy_tiles = []
			for enemy in game.map.enemies:
				if not enemy is self:
					if not enemy.next_tile == None:
						enemy_tiles.append(enemy.next_tile.place)
					else:
						enemy_tiles.append(enemy.pos)
			allow = True
			for tile in enemy_tiles:
				if int(tile[0]) == int(self.next_tile.place[0]) and int(tile[1]) == int(self.next_tile.place[1]):
					allow = False
					break

			player = game.player
			pt = game.map.grid[player.pos[1]][player.pos[0]]
			if self.next_tile == pt:
				self.next_tile = None
				allow = False
				self.switchFrame("attack")
				self.stats.attack(player.stats)

			if allow:
				self.move_speed = [0,0]
				if self.next_tile.place[0] > self.pos[0]:
					self.move_speed[0] = 1
				elif self.next_tile.place[0] < self.pos[0]:
					self.move_speed[0] = -1
				if self.next_tile.place[1] > self.pos[1]:
					self.move_speed[1] = 1
				elif self.next_tile.place[1] < self.pos[1]:
					self.move_speed[1] = -1
				return True
			else:
				self.next_tile = None
		return False

	def move(self, game):
		if ((self.pos[0]+self.pos[1])%1) >= 0.5:
			self.switchFrame("stepa")
		else:
			self.switchFrame("stepb")
		mx = self.prev_pos[0]+self.move_speed[0]
		my = self.prev_pos[1]+self.move_speed[1]
		s = self.move_speed
		#increment movement
		self.pos[0] += s[0]*self.mov_speed
		self.pos[1] += s[1]*self.mov_speed
		self.pos[0] = round(self.pos[0],2)
		self.pos[1] = round(self.pos[1],2)
		self.node.setPos(-self.pos[0], -self.pos[1], 0)
		#and break when full step made
		if self.pos[0] == round(self.prev_pos[0]+s[0],2):
			if self.pos[1] == round(self.prev_pos[1]+s[1],2):
				self.pos[0] = int(self.pos[0])
				self.pos[1] = int(self.pos[1])
				self.move_speed = [0,0]
				self.prev_pos = self.pos[:]
				self.switchFrame("idle")
				return 1
