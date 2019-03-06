import asyncio
from math import sin
from sys import exit
from random import choice
from direct.showbase.ShowBase import *
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import ClockObject, WindowProperties, DirectionalLight
from .readfile import cfgdict
from .map import Map
from .inputs import Inputs
from .wireframify import makeWireframe
from .player import Player
from .hud import HUD
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
		props = WindowProperties()
		props.setSize(tuple(self.cfg["general"]["resolution"]))
		props.setFullscreen(int(self.cfg["general"]["fullscreen"]))
		props.setCursorHidden(True)
		#props.setMouseMode(WindowProperties.M_relative)
		base.win.requestProperties(props)
		base.disableMouse()
		base.win.setClearColor((0,0,0,0))
		self.inputs = Inputs(self.cfg["key"])

		#cats=["mainmenu", "font_daego", "font_toompoost", "parts", "enemies", "items"]
		#for cat in cats: makeWireframe(cat)

		self.hud = HUD(self)

		self.transition = Transitions(loader)
		self.parts_models = getParts("data/models/egg/parts/parts")
		self.enemy_models = getParts("data/models/egg/enemies/enemies")
		self.item_models = getParts("data/models/egg/items/items")

		sounds = [
			"break", "error", "explosion", "hit_a", "hit_b", "hit_c", "scare",
			"select_a", "select_b", "splurt_a", "splurt_b", "swallow",
			"step_enemy_a", "step_enemy_b", "step_enemy_c", "step_player", "turn"
		]
		self.sounds = {}
		for sound in sounds:
			self.sounds[sound] = loader.loadSfx("data/sound/"+sound+".wav")
		self.sounds["step_player"].setVolume(0.3)

		if self.cfg["general"]["fx"] == 1:
			render.setShaderAuto()
			aspect2d.setShaderAuto()
			filters = CommonFilters(base.win, base.cam)
			filters.setBloom(blend=(0.1,0.1,0.1,0.0), mintrigger=0.0, maxtrigger=0.1, desat=0.0, intensity=0.6, size="small")
		#self.startGame()

	def startGame(self):
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
			if self.inputs.buttons["start_game"]:
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

		self.buildingmodel = getParts("data/models/egg/mainmenu/mainmenu", color=None)
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
			if self.inputs.buttons["quit"]:
				self.running = False
			if self.mode == "game":
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
			elif self.mode == "inventory":
				answer = self.hud.ask("inventory:", self.player.stats.inventory)
				if not answer == None:
					self.mode = "game"
			elif self.mode == "restart":
				self.startGame()
			return task.cont
		print("bye!")
		exit()

	def input(self):
		act = False
		tile = self.map.grid[self.player.pos[1]][self.player.pos[0]]
		if self.inputs.buttons["forward"]:
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
		elif self.inputs.buttons["wait"]:
			act = True
			self.sounds["turn"].play()
			self.delay = 10
			self.hud.output.append("You wait.")
		elif self.inputs.buttons["turn_left"]:
			self.sounds["turn"].play()
			self.player.turn(1)
			self.actions.append((self.player.turn, 1))
		elif self.inputs.buttons["turn_right"]:
			self.sounds["turn"].play()
			self.player.turn(-1)
			self.actions.append((self.player.turn, -1))
		elif self.inputs.buttons["take"]:
			if not tile.item == None:
				self.sounds["select_b"].play()
				tile.item[0].removeNode()
				i = items[tile.item[1]]()
				self.player.stats.inventory.append(i)
				self.hud.output.append("You found a " + i.name)
				tile.item = None
				act = True
		elif self.inputs.buttons["inventory"]:
			self.mode = "inventory"
		elif self.inputs.buttons["stairs_down"]:
			if tile.c == "<":
				self.nextLevel()
			self.inputs.buttons["stairs_down"] = False

		if act:
			self.player.stats.turn()
			for e, enemy in enumerate(self.map.enemies):
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
