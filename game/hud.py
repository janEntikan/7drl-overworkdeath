from panda3d.core import NodePath, Camera, TextFont, TextNode
from .text import loadFont, makeText
from .tools import makeInstance

class HUD():
	def __init__(self, game):
		self.game = game
		self.font = loader.loadFont('data/fonts/arizone.ttf')
		self.font.render_mode = TextFont.RM_wireframe
		self.font.setPixelsPerUnit(8)
		stats = self.game.player.stats
		self.title = self.addText("Overwork Death v0.2", 64, 0)
		self.title.setAlign(TextNode.ARight)
		self.lu = self.addText("...", 0,0)
		self.ld = self.addText("...", 0, 24.5)
		self.out = self.addText("...\n...\n...\n...", 64, 30)
		self.out.setAlign(TextNode.ARight)
		self.output = ["...", "...", "...", "..."]
		self.update()

	def addText(self, str, x, y):
		l = TextNode('textnode')
		l.setFont(self.font)
		l.setText(str)
		textNodePath = aspect2d.attachNewNode(l)
		textNodePath.setScale(0.05)
		textNodePath.setPos(-1.6+(x/20),0,0.85-(y/20))
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
