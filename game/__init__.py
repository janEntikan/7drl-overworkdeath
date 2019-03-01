from sys import exit
from direct.showbase.ShowBase import *
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import ClockObject, WindowProperties, DirectionalLight
from .readfile import cfgdict
from .map import Map
from .inputs import Inputs
from .wireframify import make_wireframe
from .player import Player

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
		#base.disableMouse()
		base.win.setClearColor((0,0,0,0))
		self.inputs = Inputs(self.cfg["key"])

		cats=["font_daego", "font_toompoost", "parts", "enemies"]
		for cat in cats: make_wireframe(cat)

		self.map = Map()
		self.player = Player(3, 3, 1)

		if self.cfg["general"]["fx"] == 1:
			render.setShaderAuto()
			filters = CommonFilters(base.win, base.cam)
			filters.setBloom(blend=(0.1,0.1,0.1,0.0), mintrigger=0.0, maxtrigger=0.1, desat=0.0, intensity=0.2, size="small")
			filters.setBlurSharpen(amount=0.4)
		d = DirectionalLight("d")
		dn = render.attachNewNode(d)
		render.setLight(dn)

	def load(self):
		self.running = True
		self.actions = []
		self.taskMgr.add(self.loop, "main_loop")

	def loop(self, task):
		if self.running:
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
		if self.inputs.buttons["kill"]:
			self.running = False
		else:
			if self.inputs.buttons["forwards"]:
				self.actions.append((self.player.move,-1))
			elif self.inputs.buttons["turn_left"]:
				self.actions.append((self.player.turn, 1))
			elif self.inputs.buttons["turn_right"]:
				self.actions.append((self.player.turn, -1))

	def update(self):
		self.player.update()
