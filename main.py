import builtins
from game import Game



class GameApp():
    def __init__(self):
        builtins.game = Game()
        game.load()
        game.run()
        print("bye!")
gameApp = GameApp()
