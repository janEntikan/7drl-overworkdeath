from panda3d.core import BitMask32
from .stats import Statset

class Cam():
    def __init__(self, x, y, angle):
        base.camLens.setFov(90)
        base.camNode.setCameraMask(BitMask32.bit(0))
        base.camLens.setFar(20)
        base.camLens.setNear(0.01)
        self.node = render.attachNewNode("placement")
        self.camNode = self.node.attachNewNode("cam")
        self.camNode.set_pos((0,-0.4,0))
        base.camera.reparentTo(self.camNode)
        self.node.set_hpr(angle, 0, 0)
        self.node.set_pos(x+0.5,y+0.5,0.2)

    def update(self, place):
        self.node.set_hpr((place[2]*90)+180,0,0)
        self.node.set_pos(-place[0],-place[1],0.2)

class Player():
    def __init__(self, x, y, angle):
        self.camera = Cam(x,y,angle)
        self.rot_speed = 0.1
        self.mov_speed = 0.1
        self.place = [x,y,angle]
        self.prev_place = self.place[:]
        self.pos = self.place[0], self.place[1]
        self.target = None
        self.stats = Statset()
        self.stats.next_level = 100
        self.stats.endurance += 2
        self.stats.updateStats()

    def update(self):
        self.camera.update(self.place)

    def turn(self, d):
        #increment angle
        self.place[2] += d*self.rot_speed
        self.place[2] = round(self.place[2], 2)
        #break when quarter turn made
        if self.place[2] == self.prev_place[2]+d:
            self.place[2] = self.place[2]%4
            self.prev_place = self.place[:]
            return 1

    def move(self, d):
        #get angle
        x, y, angle = self.prev_place
        l = [[0,-d], [d,0], [0,d], [-d,0]]
        s = l[int(self.place[2])]
        current = game.map.grid[int(y)][int(x)]
        mx = int(x+s[0])
        my = int(y+s[1])
        enemythere = False
        self.target = None
        for enemy in game.map.enemies:
            if enemy.pos[0] == mx and enemy.pos[1] == my:
                self.target = enemy
                if not self.target.stats.status == "Dead" and not self.target.stats.status == "Dying":
                    return "melee"
        self.pos = mx, my
        try:
            dest = game.map.grid[my][mx]
        except:
            pass
            #print(mx, my)
        #hittesting
        if dest.c == "." or dest.c == "+" or dest.c == "=" or dest.c == "<":
            move = True
            if move:
                #increment movement
                self.place[0] += s[0]*self.mov_speed
                self.place[1] += s[1]*self.mov_speed
                self.place[0] = round(self.place[0],2)
                self.place[1] = round(self.place[1],2)
                #and break when full step made
                if self.place[0] == self.prev_place[0]+s[0]:
                    if self.place[1] == self.prev_place[1]+s[1]:
                        self.prev_place = self.place[:]
                        game.sounds["step_player"].play()
                        return 1
            else:
                return 1
        else:
            return "cancel"
