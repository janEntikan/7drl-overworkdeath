from .tools import towardSpeed, makeInstance
from .stats import Statset

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
	def __init__(self, model, pos=[0,0]):
		self.mov_speed = 0.1
		self.pos = pos
		self.prev_pos = pos
		self.model = model
		self.destination = None
		self.speed = [0,3]
		self.stats = Statset()

	def load(self, models):
		self.node = makeInstance(self.model, models[self.model])
		self.node.setPos(-self.pos[0], -self.pos[1], 0)

	def plan(self, game, ei):
		self.speed[0] -= 1
		if self.speed[0] <= 0:
			self.speed[0] = self.speed[1]
			return False

		sx, sy = self.pos
		self.prev_pos = [sx, sy]
		px, py = game.player.pos
		tspeed = towardSpeed(sx, sy, px, py)
		for i in range(64):
			sx -= tspeed[0]
			sy -= tspeed[1]
			checkTile = game.map.grid[round(sy)][round(sx)]
			if checkTile.c == "W" or checkTile.c == "#":
				break
			elif round(sx) == px and  round(sy) == py:
				self.destination = [px, py]
		if not self.destination == None:
			start = game.map.grid[int(self.pos[1])][int(self.pos[0])]
			target = game.map.grid[self.destination[1]][self.destination[0]]
			self.next_tile = flow_field(start, target)
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
		return False

	def move(self, game):
		enemythere = False
		player = game.player
		mx = self.prev_pos[0]+self.move_speed[0]
		my = self.prev_pos[1]+self.move_speed[1]
		s = self.move_speed
		pt = game.map.grid[player.pos[1]][player.pos[0]]
		if self.next_tile == pt:
			self.next_tile = None
			return 1
		for enemy in game.map.enemies:
			if not enemy == self:
				try:
					if enemy.next_tile == self.next_tile:
						self.next_tile = None
						return 1
				except AttributeError:
					pass
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
				return 1
