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
items["weapons"] = {}

# RANGED
class PenDispenser(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "bunch of pens"
        self.damage = 1
        self.intelect = 1
        self.ranged = True
items["weapons"]["pendispenser"] = PenDispenser

class StapleGun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "staple gun"
        self.damage = 2
        self.intelect = 2
        self.ranged = True
items["weapons"]["staplegun"] = StapleGun

class Flamethrower(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "makeshift flamethrower"
        self.damage = 4
        self.intelect = 3
        self.ranged = True
items["weapons"]["staplegun"] = StapleGun

class NailGun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "nail-gun"
        self.damage = 5
        self.intelect = 2
        self.ranged = True
items["weapons"]["nailgun"] = NailGun

class Handgun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        names = "Revolver", "Desert Eagle", "Beretta", "Glock"
        self.name = choice(names)
        self.damage = 6
        self.intelect = 5
        self.ranged = True
items["weapons"]["handgun"] = Handgun

class Shotgun(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "Shotgun"
        self.damage = 7
        self.intelect = 6
        self.ranged = True
items["weapons"]["shotgun"] = Shotgun

class AutoRifle(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "Automatic Rifle"
        self.damage = 8
        self.intelect = 7
        self.ranged = True
items["weapons"]["autorifle"] = AutoRifle

# MELEE
class RandomWeak(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        names = "letter-opener", "screwdriver", "scissors", "suitcase"
        self.name = choice(names)
        self.damage = 1
        self.intelect = 1
items["weapons"]["randomweak"] = RandomWeak

class RandomMed(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        names = "hammer", "broom", "perforator"
        self.name = choice(names)
        self.damage = 3
        self.intelect = 1
items["weapons"]["randomweak"] = RandomWeak

class Boxcutter(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "boxcutter"
        self.damage = 4
        self.intelect = 1
items["weapons"]["boxcutter"] = Boxcutter

class PapercutterSword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = "papercutter sword"
        self.damage = 5
        self.intelect = 1
items["weapons"]["papercutter"] = PapercutterSword

# CONSUMABLES
class Consumables(Item):
    def __init__(self):
        Item.__init__(self)
        self.type = "consumable"
        self.name = "consumable"
        self.verb = "use"
    def use(self):
        game.hud.output.append("You use the " + self.name)
items["consumable"] = {}

class Thermos(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "thermos"
        self.contents = choice("coffee", "tea", "chocolate")
        self.verb = "quaff"
items["consumable"]["thermos"] = Thermos

class Softdrink(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "softdrink"
        self.contents = choice(("red", "yellow" "orange", "green", "blue", "purple"))
        self.verb = "quaff"
items["consumable"]["softdrink"] = Softdrink

class Snack(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "Food"
        self.snacktypes = ("candybar","chips","cookie","raisins","nuts","sandwich")
        self.snacktype = randExpo(0,len(self.snacktypes))
        self.contents = self.types[self.type]
        self.verb = "eat"
items["consumable"]["food"] = Snack
