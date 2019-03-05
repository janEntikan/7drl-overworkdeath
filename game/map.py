from random import randint, choice, seed
from panda3d.core import NodePath
from .tools import makeInstance, randExpo, getDistance
from .mapgen import classicRogue, simpleMaze, closeUpAndCrop
from .data import getParts
from .ai import Enemy

class Tile():
	def __init__(self, x, y, c="#"):
		self.c = c
		self.place = x,y
		self.node = None
		self.item = None
		self.neighbors = []

class Map():
	def __init__(self, game, level, size=32):
		self.game = game
		self.size = size
		self.level = level
		self.seed = randint(0, 120000000000000)
		self.start = (0,0)
		self.end = (0,0)
		self.grid = []
		self.enemies = []
		self.node = render.attachNewNode("map")
		self.loadParts()
		self.generate()
		self.buildMapModel()
		self.setNeighors()
		self.sprinkleEnemies(32)

	def loadParts(self):
		self.parts = self.game.parts_models
		self.enemy_models = self.game.enemy_models
		self.item_models = self.game.item_models

	def generate(self):
		seed(self.seed)
		for y in range(self.size):
			self.grid.append([])
			for x in range(self.size):
				self.grid[y].append(Tile(x, y))
		self.grid, self.start, self.end = classicRogue(self.grid)
		self.grid = simpleMaze(self.grid)
		self.grid = closeUpAndCrop(self.grid)

	def setNeighors(self):
		dirs = [[0,-1], [1,0], [0,1], [-1,0]]
		solids = "#W><$"
		for y, row in enumerate(self.grid):
			for x, tile in enumerate(row):
				tile.neighbors = []
				for dir in dirs:
					try:
						n = self.grid[y+dir[1]][x+dir[0]]
						if not n.c in solids:
							tile.neighbors.append(n)
					except IndexError:
						pass

	def printMap(self):
		print("THE MAP:")
		for y, row in enumerate(self.grid):
			s = ""
			for x in row:
				s += x.c
			print(s)

	def sprinkleEnemies(self, n=8):
		while len(self.enemies) < n:
			x = randint(1,self.size-2)
			y = randint(1,self.size-2)
			dist_to_start = getDistance([x,y], self.start)
			if dist_to_start > 5:
				t = self.grid[y][x]
				if t.c == "." or t.c == "+":
					cc = choice(("WORKER", "DRONE_SEC"))
					e = Enemy(cc, self, [x,y])
					self.enemies.append(e)
					e.load(self.enemy_models)
					e.node.reparentTo(self.node)
					e.node.setBillboardPointEye()

	def buildMapModel(self):
		wall_orns_all = [
			"CHAIRS_A", 	"POSTER_D",		"POSTER_A",
			"CHAIRS_B", 	"PLANT_B",		"POSTER_B",
			"CHAIRS_C", 	"PLANT_C",		"POSTER_C",
			"BENCH", 		"ARCHIVE_A",	"CLOCK",
			"WATERCOOLER",	"ARCHIVE_B", 	"CAMERA",
		]
		item_weapons_ranged = [
			"pendispenser", "staplegun", "flamethrower",
			"nailgun", "handgun", "shotgun", "machinegun"
		]
		item_weapons_melee = [
			"randomweak", "randommed", "boxcutter", "papercutter"
		]
		item_cons = [
			"softdrink", "snack", "thermos"
		]
		seed(self.seed)
		empty_tile = Tile(0,0, c="")
		s = len(self.grid)
		for y,row in enumerate(self.grid):
			for x,tile in enumerate(row):
				node = NodePath("tile_"+str(x)+"_"+str(y))
				if tile.c == "+" or tile.c == "." or tile.c == "=":
					nvm = False
					for neighbor in tile.neighbors:
						if neighbor.c == "<" or neighbor.c == ">":
							nvm = True
					if tile.c == "+":
						n = makeInstance(
							"FLOOR_A", self.parts["FLOOR_WOODEN"],
							(-x,-y,0),((0),0,0))
						n.reparentTo(node)
					if y%2 == 0 and x%2 == 0 and tile.c == "+" and not nvm:
						n = makeInstance(
							"LIGHT_B", self.parts["LIGHT_B"],
							(-x,-y,0),((0),0,0))
						n.reparentTo(node)
						if randint(0, 2) > 0:
							parts = [
								"DESK_CENTER_A", "TABLE", "DESK_CENTER_B","CHAIRS_CLUSTER"
							]
							cp = randExpo(0, len(parts)-1)
							n = makeInstance(
								parts[cp], self.parts[parts[cp]],
								(-x,-y,0),((0),0,0))
							n.reparentTo(node)
						elif randint(0, 1) == 0:
							solid_center_parts = [
								"CUBICLE", "CUBICLE_CLUSTER"
							]
							cp = randExpo(0, len(solid_center_parts)-1)
							n = makeInstance(
								solid_center_parts[cp], self.parts[solid_center_parts[cp]],
								(-x,-y,0),((0),0,0))
							n.reparentTo(node)
							tile.c = "$"
						else:
							if randint(0, 3) > 0:
								todrop = choice(item_cons)
							elif randint(0, 3) > 0:
								rr = randExpo(0, len(item_weapons_melee)-1)
								todrop = item_weapons_melee[rr]
							else:
								rr = randExpo(0, len(item_weapons_ranged)-1)
								todrop = item_weapons_ranged[rr]
							n = makeInstance(todrop, self.item_models[todrop], pos=(-x,-y,0))
							n.reparentTo(node)
							n.setBillboardPointEye()
							tile.item = [n, todrop]

					elif y%2 == 1 and x%2 == 1 and tile.c == ".":
							n = makeInstance(
								"LIGHT_A", self.parts["LIGHT_A"],
								(-x,-y,0),((0),0,0))
							n.reparentTo(node)

					struct = {}
					struct["#"] = "WALL"
					struct["="] = "DOOR_WALL"
					struct["W"] = "WINDOW"
					dirs = [
						[y-1, x],
						[y, x+1],
						[y+1, x],
						[y, x-1],
					]
					for d, dir in enumerate(dirs):
						if dir[0] >= 0 and dir[0] <= s and dir[1] >= 0 and dir[1] <= s:
							ntile = self.grid[dir[0]][dir[1]]
							if  ntile.c in struct:
								n = makeInstance(struct[ntile.c], self.parts[struct[ntile.c]],
									(-x,-y,0),((d*90),0,0))
								n.reparentTo(node)
								if not ntile.c == "=" and not ntile.c ==  "W":
									p = randExpo(0,len(wall_orns_all)-1)
									if randint(0,2) == 0:
										n = makeInstance("prop", self.parts[wall_orns_all[p]],
											(-x,-y,0),((d*90)+randint(0,2),0,0))
										n.reparentTo(node)
									elif tile.c == "+":
										if randint(0,1) == 0:
											wall_orns_room = ["ARCHIVE_A", "ARCHIVE_B"]
											if randint(0, 3) ==0:
												n = makeInstance("prop", self.parts[choice(wall_orns_room)],
													(-x,-y,0),((d*90)+randint(0,2),0,0))
												n.reparentTo(node)
											else:
												wall_orns_room = ["DESK_WALL_A", "DESK_WALL_B"]
												n = makeInstance("prop", self.parts[choice(wall_orns_room)],
													(-x,-y,0),((d*90)+randint(0,2),0,0))
												n.reparentTo(node)
				elif tile.c == "<":
					n = makeInstance("stairs_down", self.parts["STAIRS_DOWN"],
						(-x,-y,0),((d*90),0,0))
					n.reparentTo(node)
					n = makeInstance("exit", self.parts["EXIT_SIGN"],
						(-x,-y,0),((d*90),0,0))
					n.reparentTo(node)
				elif tile.c == ">":
					if  self.level > 1:
						n =  makeInstance("stairs_up", self.parts["STAIRS_UP"],
							(-x,-y,0),((d*90),0,0))
						n.reparentTo(node)
					else:
						n = makeInstance(
							"FLOOR_A", self.parts["FLOOR_WOODEN"],
							(-x,-y,0),((0),0,0))
						n.reparentTo(node)
						n = makeInstance(
							"DESK_CENTER_A", self.parts["DESK_CENTER_A"],
							(-x,-y,0),((-90),0,0))
						n.reparentTo(node)
						tile.c = "+"

				node.reparentTo(self.node)
		self.node.flattenMedium()
