from random import randint, choice, seed
from panda3d.core import NodePath
from .tools import makeInstance
from .mapgen import classicRogue, simpleMaze, closeUpAndCrop
from .data import getParts

class Tile():
	def __init__(self, c="#"):
		self.c = c
		self.node = None

class Enemy():
	def __init__(self, model, pos=[0,0]):
		self.pos = pos
		self.model = model

	def load(self, models):
		self.node = makeInstance(self.model, models[self.model])
		self.node.setPos(-self.pos[0], -self.pos[1], 0)

class Map():
	def __init__(self, size=32):
		self.size = size
		self.seed = randint(0, 1200)
		self.grid = []
		self.enemies = []
		self.node = render.attachNewNode("map")
		self.loadParts()
		self.generate()
		self.buildMapModel()


	def loadParts(self):
		self.parts = getParts("data/models/egg/parts/parts")
		self.enemy_models = getParts("data/models/egg/enemies/enemies")

	def generate(self):
		seed(self.seed)
		for y in range(self.size):
			self.grid.append([])
			for x in range(self.size):
				self.grid[y].append(Tile())
		self.grid = classicRogue(self.grid)
		self.grid = simpleMaze(self.grid)
		self.grid = closeUpAndCrop(self.grid)
		self.sprinkleEnemies(32)
		self.printMap()

	def printMap(self):
		print("THE MAP:")
		for y, row in enumerate(self.grid):
			s = ""
			for x in row:
				s += x.c
			print(s)

	def sprinkleEnemies(self, n=32):
		while len(self.enemies) < n:
			x = randint(1,self.size-2)
			y = randint(1,self.size-2)
			t = self.grid[y][x]
			if t.c == "." or t.c == "+":
				e = Enemy("DRONE_SEC", [x,y])
				self.enemies.append(e)

	def buildMapModel(self):
		seed(self.seed)
		empty_tile = Tile(c="")
		s = len(self.grid)
		for y,row in enumerate(self.grid):
			for x,tile in enumerate(row):
				node = NodePath("tile_"+str(x)+"_"+str(y))
				if tile.c == "+" or tile.c == "." or tile.c == "=":
					if tile.c == "+":
						n = makeInstance(
							"FLOOR_A", self.parts["FLOOR_WOODEN"],
							(-x,-y,0),((0),0,0))
						n.reparentTo(node)
					if y%2 == 0 and x%2 == 0 and tile.c == "+":
						n = makeInstance(
							"LIGHT_B", self.parts["LIGHT_B"],
							(-x,-y,0),((0),0,0))
						n.reparentTo(node)
						if randint(0, 1) == 0:
							n = makeInstance(
								"TABLE", self.parts["TABLE"],
								(-x,-y,0),((0),0,0))
							n.reparentTo(node)
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
								if not ntile.c == "=":
									c = "CHAIRS_A", "CHAIRS_B", "CAMERA"
									if randint(0,20) == 0:
										n = makeInstance("chair", self.parts[choice(c)],
											(-x,-y,0),((d*90),0,0))
										n.reparentTo(node)
				elif tile.c == "<":
					n = makeInstance("stairs_down", self.parts["STAIRS_DOWN"],
						(-x,-y,0),((d*90),0,0))
					n.reparentTo(node)
					n = makeInstance("exit", self.parts["EXIT_SIGN"],
						(-x,-y,0),((d*90),0,0))
					n.reparentTo(node)
				elif tile.c == ">":
					n = makeInstance("stairs_up", self.parts["STAIRS_UP"],
						(-x,-y,0),((d*90),0,0))
					n.reparentTo(node)
				node.reparentTo(self.node)
		self.node.flattenMedium()

		for enemy in self.enemies:
			enemy.load(self.enemy_models)
			enemy.node.reparentTo(self.node)
			enemy.node.setBillboardPointEye()
