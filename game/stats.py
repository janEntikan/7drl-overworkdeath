class Statset():
    def __init__(self):
        self.name = "hendrik"
        self.age = 18

        self.inventory = []
        self.spells = []
        self.skills = []

        self.level = 1
        self.experience = 0
        self.next_level = 200

        self.hp = 10
        self.sp = 10
        self.armor = 0
        self.attack = 0
        self.condition = ["Good"]
        self.gem = (0,1,0)
        self.status = []

        self.strength = 10
        self.accuracy = 10
        self.intelligence = 10
        self.personality = 10
        self.endurance = 10
        self.speed = 10
        self.luck = 10


    def attack(self, target):
        #TODO: change all the values based on current and target values
        pass
