from random import randint, choice
from .tools import randExpo

items = {}
class Item():
    def __init__(self):
        self.name = "item"

class Weapon(Item):
    def __init__(self):
        Item.__init__(self)
        self.type = "weapon"
        self.name = "weapon"
        self.ranged = False
        self.verb = "equip"
# RANGED
class PenDispenser(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "bunch of pens"
        self.damage = 1
        self.intelect = 1
        self.ranged = True
items["pendispenser"] = PenDispenser

class StapleGun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "staple gun"
        self.damage = 2
        self.intelect = 2
        self.ranged = True
items["staplegun"] = StapleGun

class Flamethrower(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "makeshift flamethrower"
        self.damage = 4
        self.intelect = 3
        self.ranged = True
items["flamethrower"] = Flamethrower

class NailGun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "nail-gun"
        self.damage = 5
        self.intelect = 2
        self.ranged = True
items["nailgun"] = NailGun

class Handgun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        names = "Revolver", "Desert Eagle", "Beretta", "Glock"
        self.name = choice(names)
        self.damage = 6
        self.intelect = 5
        self.ranged = True
items["handgun"] = Handgun

class Shotgun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "Shotgun"
        self.damage = 7
        self.intelect = 6
        self.ranged = True
items["shotgun"] = Shotgun

class MachineGun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "Machine Gun"
        self.damage = 8
        self.intelect = 7
        self.ranged = True
items["machinegun"] = MachineGun

# MELEE
class RandomWeak(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        names = "letter-opener", "screwdriver", "pair of scissors", "suitcase"
        self.name = choice(names)
        self.damage = 1
        self.intelect = 1
items["randomweak"] = RandomWeak

class RandomMed(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        names = "hammer", "broom", "perforator"
        self.name = choice(names)
        self.damage = 3
        self.intelect = 1
items["randommed"] = RandomWeak

class Boxcutter(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "boxcutter"
        self.damage = 4
        self.intelect = 1
items["boxcutter"] = Boxcutter

class PapercutterSword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "papercutter sword"
        self.damage = 5
        self.intelect = 1
items["papercutter"] = PapercutterSword

# CONSUMABLES
class Consumables(Item):
    def __init__(self):
        Item.__init__(self)
        self.type = "consumable"
        self.name = "consumable"
        self.verb = "use"
    def use(self, stats):
        game.hud.output.append("You use the " + self.name)

class Thermos(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "thermos"
        self.contents = choice(("coffee", "tea", "chocolate"))
        self.verb = "quaff"
items["thermos"] = Thermos

class Softdrink(Item):
    def __init__(self):
        Item.__init__(self)
        self.contents = choice(("red", "yellow" "orange", "green", "blue", "purple"))
        self.name = self.contents + " softdrink"
        self.verb = "quaff"
items["softdrink"] = Softdrink

class Snack(Item):
    def __init__(self):
        Item.__init__(self)
        self.snacktypes = ("candybar","bag of chips","cookie","box of raisins","bag of nuts","sandwich")
        self.snacktype = randExpo(0,len(self.snacktypes))
        self.contents = self.snacktypes[self.snacktype]
        self.name = self.contents
        self.verb = "eat"
items["snack"] = Snack
