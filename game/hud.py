from panda3d.core import NodePath, Camera, TextFont, TextNode
from .text import loadFont, makeText
from .tools import makeInstance

class HUD():
	def __init__(self, game):
		self.game = game
		self.font = loader.loadFont('data/fonts/arizone.ttf')
		self.font.render_mode = TextFont.RM_wireframe
		self.font.setPixelsPerUnit(8)
		self.title = self.addText("Overwork Death v0.2", 38, -1)
		self.title.setAlign(TextNode.ARight)
		self.lu = self.addText("...", 0,-1)
		self.ld = self.addText("...", 0, 29)
		self.out = self.addText("...\n...\n...\n...", 38, 32.4)
		self.out.setAlign(TextNode.ARight)
		self.output = ["...", "...", "...", "..."]

	def ask(self, question, options):
		pass

	def addText(self, str, x, y):
		l = TextNode('textnode')
		l.setFont(self.font)
		l.setText(str)
		textNodePath = render2d.attachNewNode(l)
		textNodePath.setScale(0.03)
		textNodePath.setPos(-0.95+(x/20),0,0.85-(y/20))
		return l

	def update(self):
		stats = self.game.player.stats
		weap = self.game.player.stats.weapon
		if weap == None: weap = "None"
		s = ("hp: "+str(int(stats.hp))+"/"+str(int(stats.max_hp)) + "\n"+
			"atk: "+str(int(stats.atk))+"\n"+
			"def: "+str(int(stats.d))+"\n\n"+
			"weapon: "+weap+"\n"+
			"hunger: "+str(int(stats.hunger))+"\n"+
			"thirst: "+str(int(stats.thirst))+"\n"+
			"status: "+stats.status+"\n")
		self.ld.setText(s.upper())
		s = "name: "+stats.name +"\n"+"class: "+stats.clas+"\nlevel: "+str(stats.level)
		self.lu.setText(s.upper())
		self.output = self.output[-4:]
		s = ""
		for output in self.output:
			s += output + "\n"
		self.out.setText(s.upper())
