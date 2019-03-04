from .stats import Statset

enemy_stats = {}

class Drone_sec(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "Security droid"
        self.clas = "DRONE_SEC"
        self.xp = 20
        self.strength = 3
        self.accuracy = 4
        self.endurance = 5
        self.max_hp = 20
        self.updateStats()
enemy_stats["DRONE_SEC"] = Drone_sec

class Worker(Statset):
    def __init__(self):
        Statset.__init__(self)
        self.name = "Office worker"
        self.clas = "WORKER"
        self.xp = 5
        self.speed = 5
        self.strength = 1
        self.accuracy = 5
        self.endurance = 1
        self.max_hp = 5
        self.updateStats()
enemy_stats["WORKER"] = Worker
