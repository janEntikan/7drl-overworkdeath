from .stats import Statset
from .items import items


enemy_stats = {}
# SECURITY
class Drone_main_a(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "Maintenance droid"
        self.clas = "DRONE_MAIN_A"
        self.xp = 50
        self.speed = 2
        self.strength = 3
        self.accuracy = 5
        self.endurance = 5
        self.max_hp = 10
        self.updateStats()
enemy_stats["DRONE_MAIN_A"] = Drone_main_a

class Drone_main_b(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "Maintenance droid"
        self.clas = "DRONE_MAIN_B"
        self.xp = 80
        self.speed = 4
        self.strength = 6
        self.accuracy = 10
        self.endurance = 10
        self.max_hp = 20
        self.updateStats()
enemy_stats["DRONE_MAIN_B"] = Drone_main_b

class Drone_sec(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "Security droid"
        self.clas = "DRONE_SEC"
        self.xp = 250
        self.speed = 8
        self.strength = 12
        self.accuracy = 12
        self.endurance = 18
        self.max_hp = 40
        self.weapon = items["handgun"]()
        self.updateStats()
enemy_stats["DRONE_SEC"] = Drone_sec

class SWAT(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "SWAT unit"
        self.clas = "SWAT"
        self.xp = 500
        self.strength = 8
        self.accuracy = 12
        self.endurance = 32
        self.max_hp = 80
        self.speed = 20
        self.weapon = items["machinegun"]()
        self.updateStats()
enemy_stats["SWAT"] = SWAT

# ALIENS
class Worker(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "Office worker"
        self.clas = "WORKER"
        self.xp = 50
        self.speed = 4
        self.strength = 2
        self.accuracy = 5
        self.endurance = 3
        self.max_hp = 6
        self.updateStats()
enemy_stats["WORKER"] = Worker

class AlienA(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "alien"
        self.clas = "ALIEN_A"
        self.xp = 100
        self.speed = 6
        self.strength = 2
        self.accuracy = 10
        self.endurance = 6
        self.max_hp = 12
        self.updateStats()
enemy_stats["ALIEN_A"] = AlienA

class AlienB(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "hip looking alien"
        self.clas = "ALIEN_B"
        self.xp = 150
        self.speed = 12
        self.strength = 4
        self.accuracy = 20
        self.endurance = 12
        self.max_hp = 24
        self.updateStats()
enemy_stats["ALIEN_B"] = AlienB

class AlienC(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "classy alien"
        self.clas = "ALIEN_C"
        self.xp = 200
        self.speed = 10
        self.strength = 8
        self.accuracy = 10
        self.endurance = 10
        self.max_hp = 20
        self.weapon = items["handgun"]()
        self.updateStats()
enemy_stats["ALIEN_C"] = AlienC

class AlienD(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "alien gunner"
        self.clas = "ALIEN_D"
        self.xp = 300
        self.speed = 15
        self.strength = 16
        self.accuracy = 25
        self.endurance = 15
        self.max_hp = 30
        self.weapon = items["machinegun"]()
        self.updateStats()
enemy_stats["ALIEN_D"] = AlienD

class AlienE(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "alien spider"
        self.clas = "ALIEN_E"
        self.xp = 500
        self.speed = 30
        self.strength = 64
        self.accuracy = 64
        self.endurance = 64
        self.max_hp = 128
        self.updateStats()
enemy_stats["ALIEN_E"] = AlienE
