from panda3d.core import NodePath, Camera, TextFont, TextNode
from .text import loadFont, makeText
from .tools import makeInstance

class HUD():
	def __init__(self, game):
		self.game = game
		self.font = loader.loadFont('data/fonts/arizone.ttf')
		self.font.render_mode = TextFont.RM_wireframe
		self.font.setPixelsPerUnit(8)
		self.title = self.addText("Overwork Death", 6.5, 10, 3)
		self.subtitle = self.addText("7drl 2019", 6.5, 8)
		self.options = self.addText("press S to start \npress ESCAPE to quit", 19, 16)
		self.options[0].setAlign(TextNode.ACenter)

		a = "code/graphics/sound/music by\nmomojohobo (hendrik-jan/hjh)\nteam momojo - momojo@rocketship.com"
		self.creditsa = self.addText(a, 0, -1, 0.9)

		a = (
			"special thanks to:\n"+
			"   RDB, SCHWARZBAER and the other panda3d peoples\n"+
			"   willie/chuloboy, sky/momojotweedestencil, koen/ghettokiwi\n"+
			"   purpledaughter/momojomono, scarywindow/momojoeoj, momojopogo\n"+
			"   and the roguelike community")
		self.creditsb = self.addText(a, 0, 32.5, 0.7)

	def loadGameHud(self):
		self.title[1].removeNode()
		self.subtitle[1].removeNode();self.subtitle=None
		self.options[1].removeNode();self.options=None
		self.creditsa[1].removeNode();self.credits=None
		self.creditsb[1].removeNode();self.credits=None
		self.title = self.addText("Overwork Death", 38, -1, 2)
		self.title[0].setAlign(TextNode.ARight)
		self.help = self.addText("press ? for help", 38, -0.4, 0.8)
		self.help[0].setAlign(TextNode.ARight)
		self.lu = self.addText("...", 0,-1)
		self.ld = self.addText("", 0, 31.9)
		self.out = self.addText("...\n...\n...\n...", 38, 31)
		self.out[0].setAlign(TextNode.ARight)
		self.output = ["...", "...", "...", "..."]
		self.inventory = self.addText("", 0, 7)
		self.choices = []
		self.verb = None
		self.input = ""

	def inv(self, player, t="inventory"):
		q=False
		abc = "abcdefghijklmnopqrstuvwxyz"
		self.verb = t
		for item in player.stats.inventory:
			item.update()
		if t == "inventory":
			if len(player.stats.inventory) == 0:
				self.output.append("your pockets are empty")
				q = True
			else:
				o = "inventory (escape to close)\n\n"
				for i, item in enumerate(player.stats.inventory):
					o += item.name
					if item.ranged:
						o += " (ranged) "
					if item == player.stats.weapon:
						o += " (wielding)"
					o += "\n"
				self.inventory[0].setText(o)
		elif t == "throw":
			if len(player.stats.inventory) == 0:
				self.output.append("you have nothing to throw")
				q = True
			else:
				o = "throw what? (escape to close)\n\n"
				for i, item in enumerate(player.stats.inventory):
					o += "(" + abc[i] + ") "
					o += item.name
					if item.ranged:
						o += " (ranged) "
					if item == player.stats.weapon:
						o += " (wielding)"
					o += "\n"
					self.choices.append(item)
				self.inventory[0].setText(o)
		elif t == "drop":
			if len(player.stats.inventory) == 0:
				self.output.append("you have nothing to throw")
				q = True
			else:
				o = "drop what? (escape to close)\n\n"
				for i, item in enumerate(player.stats.inventory):
					print(i)
					o += "(" + abc[i] + ") "
					o += item.name
					if item.ranged:
						o += " (ranged) "
					if item == player.stats.weapon:
						o += " (wielding)"
					o += "\n"
					self.choices.append(item)
				self.inventory[0].setText(o)
		elif t == "stats":
			s = player.stats
			o = "stats (escape to close)\n\n"
			o += (
				"strength:"+str(s.strength)+"\n"+
				"accuracy:"+str(s.accuracy)+"\n"+
				"intelect:"+str(s.intelect)+"\n"+
				"endurance:"+str(s.endurance)+"\n"+
				"speed:"+str(s.speed)+"\n"+
				"luck:"+str(s.luck)+"\n\n"+
				"level: "+str(s.level)+"\n"+
				"xp: "+str(s.xp)+"\n"+
				"next level: "+str(s.next_level)+"\n"
			)
			self.inventory[0].setText(o)
		elif t == "help":
			k = game.cfg["key"]
			o = "help (escape to close)\n\n"
			keys = (
				"forward", "backward", "turn_left", "turn_right", "wait",
			)
			for key in keys:
				o += key + ": " + k[key]+"\n"
			o += "\n"
			keys = ("take", "drop","throw", "wield", "quaff", "eat", "fire")
			for key in keys:
				o += key + ": " + k[key]+"\n"
			o += "go down stairs: <\n\n"

			o += "stats: s\nthis screen: ?\n"
			o += "return: escape\n"
			self.inventory[0].setText(o)
		else:
			o = t + " what? (escape to cancel)\n\n"
			i = 0
			for item in player.stats.inventory:
				if item.verb == t:
					o += "(" + abc[i] + ") "
					o += item.name
					if item.ranged:
						o += " (ranged) "
					if item == player.stats.weapon:
						o += " (wielding)"
					o += "\n"
					self.choices.append(item)
					i += 1
			if i == 0:
				self.output.append("you have nothing to " + t)
				q = True
		if q == True:
			self.inventory[0].setText("")
			self.game.mode = "game"
		else:
			self.inventory[0].setText(o)
		self.update()

	def addText(self, str, x, y, s=1):
		l = TextNode('textnode')
		l.setFont(self.font)
		l.setText(str)
		textNodePath = render2d.attachNewNode(l)
		textNodePath.setScale(0.025*s)
		textNodePath.setPos(-0.95+(x/20),0,0.83-(y/20))
		return l, textNodePath

	def update(self):
		stats = self.game.player.stats
		weap = stats.weapon
		if weap == None:
			weap = "None"
		else:
			weap = weap.name
		if stats.thirst >= 29:
			thirst = "dying of thirst"
		elif stats.thirst > 20:
			thirst = "dehydrated"
		elif stats.thirst > 10:
			thirst = "parched"
		elif stats.thirst > 5:
			thirst = "slight cottonmouth"
		else: thirst = "quenched"

		if stats.hunger >= 29:
			hunger = "dying of hunger"
		elif stats.hunger > 20:
			hunger = "starving"
		elif stats.hunger > 10:
			hunger = "heartburn"
		elif stats.hunger > 5:
			hunger = "healthy appetite"
		else: hunger = "fed"

		s = (
			"floor: "+str(20-game.map.level)+"\n"
			"hp: "+str(int(stats.hp))+"/"+str(int(stats.max_hp)) + "\n\n"+
			"weapon: "+weap+"\n"+
			"hunger: "+hunger+"\n"+
			"thirst: "+thirst+"\n"+
			"status: "+stats.status+"\n")
		self.lu[0].setText(s.upper())
		self.output = self.output[-8:]
		s = ""
		for output in self.output:
			s += output + "\n"
		self.out[0].setText(s.upper())
