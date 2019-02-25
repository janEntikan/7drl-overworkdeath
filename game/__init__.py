from sys import exit
from direct.showbase.ShowBase import *
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import ClockObject, WindowProperties,
from .readfile import cfgdict
import wireframify

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
		props.setMouseMode(WindowProperties.M_relative)
		base.win.requestProperties(props)
		base.disableMouse()
		base.win.setClearColor((0,0,0,0))
		self.inputs = Inputs(self.cfg["key"])

	def load(self):
		self.running = True
		self.actions = []
		self.taskMgr.add(self.loop, "main_loop")

	def loop(self, task):
		if self.running:
			dt = globalClock.getDt()
			self.input()
			self.update()
			return task.cont
		print("bye!")
		exit()

	def input(self):
		if self.inputs.buttons["kill"]:
			self.running = False

def update(self):
		pass
