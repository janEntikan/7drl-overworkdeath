import asyncio
from math import sin
from sys import exit
from random import choice, randint
from direct.showbase.ShowBase import *
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import ClockObject, WindowProperties, DirectionalLight
from .readfile import cfgdict
from .map import Map
from .inputs import Inputs
from .wireframify import makeWireframe
from .player import Player
from .hud import HUD
from .tools import makeInstance
from .data import getParts, getPartsColors
from .items import items
from direct.showbase.Transitions import Transitions

class Game(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.cfg = cfgdict("data/default_config.cfg")
		globalClock.setMode(ClockObject.MLimited)
		globalClock.setFrameRate(int(self.cfg["general"]["framerate"]))
		#base.setFrameRateMeter(int(self.cfg["general"]["debug"]))
		self.props = WindowProperties()
		self.props.setSize(tuple(self.cfg["general"]["resolution"]))
		self.props.setFullscreen(int(self.cfg["general"]["fullscreen"]))
		self.props.setCursorHidden(True)
		self.fullscreen = int(self.cfg["general"]["fullscreen"])
		#props.setMouseMode(WindowProperties.M_relative)
		base.win.requestProperties(self.props)
		base.disableMouse()
		base.win.setClearColor((0,0,0,0))
		self.inputs = Inputs(self.cfg["key"])

		#cats=["mainmenu", "parts", "enemies", "items"]
		#for cat in cats: makeWireframe(cat)

		self.hud = HUD(self)

		self.transition = Transitions(loader)
		self.parts_models = getParts("data/models/egg/parts/parts")
		self.enemy_models = getParts("data/models/egg/enemies/enemies")
		self.item_models = getParts("data/models/egg/items/items")

		sounds = [
			"break", "error", "explosion", "hit_a", "hit_b", "hit_c", "scare",
			"select_a", "select_b", "splurt_a", "splurt_b", "swallow",
			"step_enemy_a", "step_enemy_b", "step_enemy_c", "step_player", "turn",
			"projectile_a", "projectile_b", "projectile_c",
		]
		self.sounds = {}
		for sound in sounds:
			self.sounds[sound] = loader.loadSfx("data/sound/"+sound+".wav")
		self.sounds["step_player"].setVolume(0.3)
		self.act = False
		if self.cfg["general"]["fx"] == 1:
			render.setShaderAuto()
			aspect2d.setShaderAuto()
			filters = CommonFilters(base.win, base.cam)
			filters.setBloom(blend=(0.1,0.1,0.1,0.0), mintrigger=0.0, maxtrigger=0.1, desat=0.0, intensity=0.6, size="small")
		#self.startGame()

	def startGame(self):
		self.hud.output.append("...")
		self.hud.output.append("You wake up, head on the keyboard.")
		self.hud.output.append("Where is everybody?")
		render.node().removeAllChildren()
		self.mode = "game"
		self.delay = 0
		self.map = Map(self, 1)
		self.player = Player(self.map.start[0], self.map.start[1], 2)
		self.transition.setFadeColor(0, 0, 0)
		self.transition.fadeIn(2)
		d = DirectionalLight("d")
		dn = render.attachNewNode(d)
		self.actions = []
		base.camera.setHpr(0,0,0)
		base.camera.setPos(0,0,0)
		drinks = ["red", "yellow", "orange", "green", "blue", "purple"]
		types = ["health", "cure", "poison", "blind", "improve", "warmth"]
		self.drinks = {}
		for drink in drinks:
			rt = choice(types)
			types.remove(rt)
			self.drinks[drink] = [rt, False]
		render.setLight(dn)

	def nextLevel(self):
		render.node().removeAllChildren()
		render.hide()
		self.transition.setFadeColor(0, 0, 0)
		self.transition.fadeOut(1)
		self.delay = 0
		self.actions = []
		self.map = Map(self, self.map.level+1)
		self.hud.output.append("You reach the " + str(20-self.map.level) + "th floor.")
		self.player.place = [self.map.start[0], self.map.start[1]-1, 2]
		self.player.prev_place = self.player.place[:]
		self.player.pos = [self.map.start[0], self.map.start[1]-1]
		render.show()
		self.player.camera.node.reparentTo(render)
		d = DirectionalLight("d")
		dn = render.attachNewNode(d)
		render.setLight(dn)
		self.transition.fadeIn(1)
		self.mode = "game"

	def mainMenu(self, task):
		if self.running:
			self.mcp[3]+=1
			self.mcp[2] = 8 + (sin(self.mcp[3]/50)*7)
			base.camera.setPos(self.mcp[0], self.mcp[1], self.mcp[2])
			self.buildingmodel["tower"][0].setHpr(self.mcp[3],0,0)
			self.buildingmodel["tower"][1].setHpr(self.mcp[3],0,0)
			if self.inputs.buttons["quit"]:
				self.running = False
			if self.inputs.buttons["stats"]:
				self.inputs.buttons["stats"] = False
				self.bgsong.stop()
				self.sounds["select_b"].play()
				base.camera.setPos(0,0,0)
				self.hud.loadGameHud()
				self.startGame()
				self.bgsong = loader.loadSfx("data/music/LEVEL1.ogg")
				self.bgsong.setVolume(0.3)
				self.bgsong.setLoop(True)
				self.bgsong.play()
				self.taskMgr.add(self.loop, "main_loop")
				return False
			return task.cont
		print("bye!")
		exit()

	def load(self):
		self.running = True
		self.actions = []
		self.bgsong = loader.loadSfx("data/music/THEME.ogg")
		self.bgsong.setVolume(0.5)
		self.bgsong.setLoop(True)
		self.bgsong.play()

		self.buildingmodel = getParts("data/models/egg/mainmenu/mainmenu")
		self.buildingmodel["tower"][0].reparentTo(render)
		self.buildingmodel["tower"][1].reparentTo(render)

		d = DirectionalLight("d")
		dn = render.attachNewNode(d)
		render.setLight(dn)
		self.mcp = [0,-20,8, 1200]
		self.taskMgr.add(self.mainMenu, "main_menu")

	def loop(self, task):
		if self.running:
			self.hud.update()
			if self.mode == "game":
				if self.inputs.buttons["quit"]:
					self.running = False
				if self.player.stats.status == "Dying":
					self.hud.output.append("You died.")
					self.mode = "gameover"
					self.sounds["explosion"].play()
					taskMgr.add(die())
				else:
					self.delay -= 1
					if self.delay <= 0:
						self.delay = 0
						if len(self.actions) > 0:
							for action in self.actions:
								a = action[0](action[1])
								if a == 1:
									self.actions.remove(action)
						else:
							self.input()
						self.update()
			elif self.mode == "gameover":
				base.camera.setH(base.camera.getH()+2)
				base.camera.setZ(base.camera.getZ()-0.001)
			# Hud input, choices, etc.
			elif self.mode == "inventory":
				close = False
				if self.inputs.buttons["return"]:
					close = True
				else:
					abc = "abcdefghijklmnopqrstuvwxyz0123456789"
					cc = 100
					if not self.inputs.raw_key == None:
						if self.inputs.raw_key in abc:
							for l, letter in enumerate(abc):
								if self.inputs.raw_key == letter:
									cc = l
						if cc < len(self.hud.choices):
							item = self.hud.choices[cc]
							if self.hud.verb == "inventory":
								pass
							elif self.hud.verb == "drop":
								f = self.player.drop(item)
								if f: self.act = True
							elif self.hud.verb == "throw":
								self.player.throw(item)
								self.act = True
							else:
								f = self.hud.choices[cc].use(self.player)
								if f: self.act = True
							close = True
				if close:
					self.mode = "game"
					self.hud.inventory[0].setText("")
					self.hud.choices = []
					self.inputs.buttons["return"] = False

			elif self.mode == "restart":
				self.startGame()
			self.inputs.raw_key = None
			return task.cont
		print("bye!")
		exit()

	def input(self):
		act = self.act
		tile = self.map.grid[self.player.pos[1]][self.player.pos[0]]
		if act == False:
			if self.inputs.buttons["turn_left"]:
				self.sounds["turn"].play()
				self.player.turn(1)
				self.actions.append((self.player.turn, 1))
			elif self.inputs.buttons["turn_right"]:
				self.sounds["turn"].play()
				self.player.turn(-1)
				self.actions.append((self.player.turn, -1))
			elif self.inputs.buttons["forward"]:
				en = self.player.move(-1)
				if not en == "cancel":
					if en == "melee":
						self.delay = 10
						self.player.stats.attack(self.player.target.stats, True)
						self.player.target.switchFrame("hurt")
						self.transition.setFadeColor(0.1,0.1,0.1)
						self.transition.fadeOut(0.1)
						self.transition.fadeIn(0.01)
						self.hud.update()
						l = "_a", "_b", "_c"
						self.sounds["hit"+choice(l)].play()
						act = True
					else:
						self.actions.append((self.player.move,-1))
						act = True
			elif self.inputs.buttons["backward"]:
				self.sounds["turn"].play()
				self.player.turn(1)
				self.actions.append((self.player.turn, 1))
				self.player.turn(1)
				self.actions.append((self.player.turn, 1))
			elif self.inputs.buttons["fire"]:
				f = self.player.fire()
				if f:
					act = True

			elif self.inputs.buttons["wait"]:
				act = True
				self.sounds["turn"].play()
				self.delay = 10
				self.hud.output.append("You wait.")
			elif self.inputs.buttons["take"]:
				if not tile.item == None:
					abc = "abcdefghijklmnopqrstuvwxyz"
					if len(self.player.stats.inventory) < len(abc):
						self.sounds["select_b"].play()
						tile.item[0].removeNode()
						i = tile.item[1]
						self.player.stats.inventory.append(i)
						self.hud.output.append("You found a " + i.name)
						tile.item = None
						act = True
					else:
						self.hud.output.append("You can't carry any more.")
						self.delay = 10
			elif self.inputs.buttons["stairs_down"]:
				if tile.c == "<":
					self.nextLevel()
				self.inputs.buttons["stairs_down"] = False
			elif self.inputs.buttons["fullscreen"]:
				if self.fullscreen:
					self.fullscreen = 0
				else:
					self.fullscreen = 1
				self.props.setFullscreen(int(self.fullscreen))
				base.win.requestProperties(self.props)
				self.inputs.buttons["fullscreen"] = False
			else:
				verbs = "inventory", "drop", "throw", "eat","quaff", "wield", "stats", "help"
				for i in self.inputs.buttons:
					if self.inputs.buttons[i]:
						if i in verbs:
							self.mode = "inventory"
							self.hud.inv(self.player, i)
							self.inputs.buttons[i] = False
		if act:
			self.act = False
			self.player.stats.turn()
			for e, enemy in enumerate(self.map.enemies):
				if self.player.stats.speedboost <= 0 or randint(0,2) == 0:
					en = enemy.plan(self, e)
					if en:
						enemy.stats.turn()
						self.actions.append((enemy.move, self))
			self.player.stats.updateStats()

	def update(self):
		self.player.update()
		for enemy in self.map.enemies:
			enemy.update(self)

async def die():
	game.transition.setFadeColor(1, 0, 0)
	await game.transition.fadeOut(2)
	game.startGame()
