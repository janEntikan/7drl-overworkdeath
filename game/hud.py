from panda3d.core import NodePath, Camera
from .text import loadFont, makeText

class HUD():
	def __init__(self, cam):
		self.fonts = {}
		self.fonts["daego"] = loadFont("daego")
		self.node = NodePath("hud")
		self.nodes = []
		self.bottom = 26
		self.right = 52

		displayRegion = base.win.makeDisplayRegion()
		camNode = Camera('cam')
		camNP = NodePath(camNode)
		displayRegion.setCamera(camNP)
		camNP.reparentTo(self.node)
		self.print("overwork death v1", self.right-16, 1, color="white")
		self.print("hjhilberding s", self.right-16.3, 0.5, color="white", scale=0.5)


		# player info
		strings = [
			"name = wolverine", "class = accountant",

		]
		self.printBlock(strings, 1, 1, color="white", scale=1)

		# player state
		strings = [
			"hp = 5", "atk = 1", "def = 1", "weapon = papercutter blade",
			" ",
			"hunger = 5", "thirst = 5",
			"status = sleepy",
		]
		self.printBlock(strings, 1, self.bottom-len(strings), color="white", scale=1)

		self.node.flattenMedium()

	def printBlock(self, strings, x, y, color="white", scale=1):
		for s, string in enumerate(strings):
			self.print(string, x, y+s, color, scale)

	def print(self, string, x, y, color="white", scale=1):
		t = makeText(self.fonts["daego"], color, string, 30, line_space=(0.2))
		t.setScale(0.004*scale,0.004*scale,0.004*scale)
		t.setPos((-0.26+(x*0.01),1,0.26-(y*0.02)))
		t.reparentTo(self.node)
		return t
