from direct.showbase import DirectObject
from panda3d.core import WindowProperties, ModifierButtons

class Inputs(DirectObject.DirectObject):
    def __init__(self, keys):
        #BUTTONS
        self.raw_key = None
        self.commands = []
        for key in keys:
            self.commands.append([key, keys[key]])
        self.buttons = {}
        for command in self.commands:
            self.buttons[command[0]] = False
            self.accept(command[1], self.setKey, [command[0], True])
            self.accept(command[1]+"-up", self.setKey, [command[0], False])

        base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
        self.accept('keystroke', self.setraw)

        self.x = self.y = 0
        taskMgr.add(self.updateMouse, "update_mouse")

    def setraw(self, keyname):
        self.raw_key = keyname

    def setKey(self,key,state):
        self.buttons[key] = state

    def updateMouse(self, task):
        self.mouse = base.win.getPointer(0)
        self.lastX = self.x
        self.lastY = self.y
        self.x = self.mouse.getX()
        self.y = self.mouse.getY()
        self.xmovement = self.lastX - self.x
        self.ymovement = self.lastY - self.y
        return task.cont
