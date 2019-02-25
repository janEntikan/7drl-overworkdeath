from random import randint, choice

class Tile():
    def __init__(self, c="#"):
        self.c = c

class Map():
    def __init__(self, size=32):
        self.grid = []
        #make it
        for y in range(size):
            self.grid.append([])
            for x in range(size):
                self.grid[y].append([])
                self.grid[y][x].append(Tile())
        self.grid = classic_rogue(self.grid)
        self.grid = simple_maze(self.grid)
        self.print()

    def print(self):
        for y, row in enumerate(self.grid):
            s = ""
            for x in row:
                s += x[0].c
            print(s)

# classic rogue mapgen
def classic_rogue(grid):
    size = len(grid)
    part = int(size/3)
    min = 4
    max = part - 2
    rooms = []
    for gy in range(3):
        for gx in range(3):
            w = randint(min, max)
            h = randint(min, max)
            x = randint(2, (part - w)) + (gx*part)-1
            y = randint(2, (part - h)) + (gy*part)-1
            rooms.append([x-(x%2)+1,y-(y%2)+1,w-(w%2)-1,h-(h%2)-1])
    for room in rooms:
        for y in range(room[3]):
            for x in range(room[2]):
                grid[room[1]+y][room[0]+x][0].c = "+"
    #TODO: connect rooms?
    return grid

#braided recursive backtracking maze
def simple_maze(grid, start=[1,1], steps=2, braids=4):
    size = len(grid)
    direction = 3 #0123 - NESW
    directions = [[0,-1], [1,0], [0,1], [-1,0]]
    stack = []
    loc = start[:]
    stack.append(loc)
    while True:
        trying = True
        tried = []
        while trying:
            d = directions[direction]
            next_tiles = [
                loc[0]+d[0],
                loc[1]+(d[1]),
                loc[0]+(d[0]*2),
                loc[1]+(d[1]*2),
            ]
            cant = False
            try:
                tile_a = grid[next_tiles[1]][next_tiles[0]][0]
                tile_b = grid[next_tiles[3]][next_tiles[2]][0]
                if tile_a.c == "#" and tile_b.c == "#":
                    tile_a.c = "."
                    tile_b.c = "."
                    loc = [next_tiles[2],next_tiles[3]]
                    stack.append(loc[:])
                else:
                    if randint(0, braids) == 0: #when to braid
                        if not tile_b.c == "+":
                            tile_a.c = "."
                            tile_b.c = "."
                    cant = True
            except IndexError:
                cant = True
            if randint(0, 5) == 0: #random turn
                cant = True
            if cant:
                tried.append(direction)
                possible_directions = []
                for i in range(4):
                    if not i in tried:
                        possible_directions.append(i)
                if not len(possible_directions) == 0:
                    direction = choice(possible_directions)
                else:
                    trying = False
        if len(stack) > 0:
            loc = stack[-1:][0]
            stack = stack[:-1]
        else:
            return grid

map = Map()
