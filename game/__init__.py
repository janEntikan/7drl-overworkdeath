from sys import exit
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

class Game(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.cfg = cfgdict("data/default_config.cfg")
		globalClock.setMode(ClockObject.MLimited)
		globalClock.setFrameRate(int(self.cfg["general"]["framerate"]))
		base.setFrameRateMeter(int(self.cfg["general"]["debug"]))
		props = WindowProperties()
		props.setSize(tuple(self.cfg["general"]["resolution"]))
		props.setFullscreen(int(self.cfg["general"]["fullscreen"]))
		props.setCursorHidden(True)
		#props.setMouseMode(WindowProperties.M_relative)
		base.win.requestProperties(props)
		base.disableMouse()
		base.win.setClearColor((0,0,0,0))
		self.inputs = Inputs(self.cfg["key"])

		cats=["font_daego", "font_toompoost", "parts", "enemies", "items"]
		for cat in cats: makeWireframe(cat)
		self.delay = 0
		self.parts_models = getParts("data/models/egg/parts/parts")
		self.enemy_models = getParts("data/models/egg/enemies/enemies")
		self.item_models = getPartsColors("items")

		self.map = Map(self)
		self.player = Player(self.map.start[0], self.map.start[1]-1, 2)
		self.hud = HUD(self)

		if self.cfg["general"]["fx"] == 1:
			render.setShaderAuto()
			aspect2d.setShaderAuto()
			filters = CommonFilters(base.win, base.cam)
			filters.setBloom(blend=(0.1,0.1,0.1,0.0), mintrigger=0.0, maxtrigger=0.1, desat=0.0, intensity=0.6, size="small")
			#filters = CommonFilters(base.win, base.cam2d)
			#filters.setBloom(blend=(0.1,0.1,0.1,0.0), mintrigger=0.0, maxtrigger=0.1, desat=0.0, intensity=0.6, size="small")
			#filters.setBlurSharpen(amount=0.4)

		d = DirectionalLight("d")
		dn = render.attachNewNode(d)
		render.setLight(dn)

	def load(self):
		self.running = True
		self.actions = []
		self.taskMgr.add(self.loop, "main_loop")

	def loop(self, task):
		if self.running:
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
			return task.cont
		print("bye!")
		exit()

	def input(self):
		act = False
		if self.inputs.buttons["kill"]:
			self.running = False
		else:
			if self.inputs.buttons["forward"]:
				en = self.player.move(-1)
				if not en == "cancel":
					if en == "melee":
						self.delay = 10
						self.player.stats.attack(self.player.target.stats)
						self.player.target.switchFrame("hurt")
						self.flashwhite = 1
						act = True
					else:
						self.actions.append((self.player.move,-1))
						act = True
			elif self.inputs.buttons["backward"]:
				self.player.turn(1)
				self.actions.append((self.player.turn, 1))
				self.player.turn(1)
				self.actions.append((self.player.turn, 1))
			elif self.inputs.buttons["turn_left"]:
				self.player.turn(1)
				self.actions.append((self.player.turn, 1))
			elif self.inputs.buttons["turn_right"]:
				self.player.turn(-1)
				self.actions.append((self.player.turn, -1))
		if act:
			self.player.stats.turn()
			for e, enemy in enumerate(self.map.enemies):
				en = enemy.plan(self, e)
				if en:
					enemy.stats.turn()
					self.actions.append((enemy.move, self))
			self.player.stats.updateStats()
			self.hud.update()
		if self.inputs.buttons["stuff"]:
			render.ls()

	def update(self):
		self.player.update()
		for enemy in self.map.enemies:
			enemy.update(self)
