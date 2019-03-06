from panda3d.core import NodePath, Camera, TextFont, TextNode
from .text import loadFont, makeText
from .tools import makeInstance

class HUD():
	def __init__(self, game):
		self.game = game
		self.font = loader.loadFont('data/fonts/arizone.ttf')
		self.font.render_mode = TextFont.RM_wireframe
		self.font.setPixelsPerUnit(8)
		self.title = self.addText("Overwork Death", 4, 10, 3)
		self.subtitle = self.addText("7drl 2019", 4, 8)
		self.options = self.addText("press S to start \npress ESCAPE to quit", 19, 16)
		self.options[0].setAlign(TextNode.ACenter)

		a = "code/graphics/sound/music by\nmomojohobo (hendrik-jan/hjh)\nteam momojo - momojo@rocketship.com"
		self.creditsa = self.addText(a, 0, -1, 0.9)

		a = ("thanks to schwarzbaer for the flowfield\n"+
			"thanks to rdb for always having the panda3d answers\n"+
			"special thanks to:\n"+
			"   willie/chuloboy, sky/momojotweedestencil, koen/ghettokiwi\n"+
			"   purpledaughter/momojomono, scarywindow/momojoeoj, momojopogo\n"+
			"   the roguelike community and the folk at vintageaspies")
		self.creditsb = self.addText(a, 0, 32.5, 0.7)

	def loadGameHud(self):
		self.title[1].removeNode()
		self.subtitle[1].removeNode();self.subtitle=None
		self.options[1].removeNode();self.options=None
		self.creditsa[1].removeNode();self.credits=None
		self.creditsb[1].removeNode();self.credits=None

		self.title = self.addText("Overwork Death", 38, -1)
		self.title[0].setAlign(TextNode.ARight)
		self.lu = self.addText("...", 0,-1)
		self.ld = self.addText("...", 0, 29)
		self.out = self.addText("...\n...\n...\n...", 38, 32.4)
		self.out[0].setAlign(TextNode.ARight)
		self.output = ["...", "...", "...", "..."]

	def ask(self, question, options):
		pass

	def addText(self, str, x, y, s=1):
		l = TextNode('textnode')
		l.setFont(self.font)
		l.setText(str)
		textNodePath = render2d.attachNewNode(l)
		textNodePath.setScale(0.03*s)
		textNodePath.setPos(-0.95+(x/20),0,0.85-(y/20))
		return l, textNodePath

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
		self.ld[0].setText(s.upper())
		s = "name: "+stats.name +"\n"+"class: "+stats.clas+"\nlevel: "+str(stats.level)
		self.lu[0].setText(s.upper())
		self.output = self.output[-4:]
		s = ""
		for output in self.output:
			s += output + "\n"
		self.out[0].setText(s.upper())
