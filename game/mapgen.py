from random import randint, choice

# classic rogue mapgen
def classicRogue(grid):
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
    for r, room in enumerate(rooms):
        door = False
        for y in range(room[3]):
            for x in range(room[2]):
                grid[room[1]+y][room[0]+x].c = "+"
        # add a door to room
        sides = ["rd", "lrd", "ld", "urd", "urdl", "uld", "ur", "ulr", "ul"]
        s = sides[r]
        rs = choice(s)
        if rs == "u":
            x = (int(randint(1,room[2]-2)/2)*2)+1
            y = 0
            grid[y+room[1]-1][x+room[0]].c = "="
            grid[y+room[1]-2][x+room[0]].c = "."
        elif rs == "d":
            x = (int(randint(1,room[2]-2)/2)*2)+1
            y = 0
            grid[y+room[1]+room[3]][x+room[0]].c = "="
            grid[y+room[1]+room[3]+1][x+room[0]].c = "."
        if rs == "l":
            x = 0
            y = (int(randint(1,room[3]-2)/2)*2)+1
            grid[y+room[1]][x+room[0]-1].c = "="
            grid[y+room[1]][x+room[0]-2].c = "."
        elif rs == "r":
            x = 0
            y = (int(randint(1,room[3]-2)/2)*2)+1
            grid[y+room[1]][x+room[0]+room[2]].c = "="
            grid[y+room[1]][x+room[0]+room[2]+1].c = "."

    # add stairs down to a random room
    room = choice(rooms)
    x = randint(room[0]+1, room[0]+room[2]-2)
    y = randint(room[1]+1, room[1]+room[3]-2)
    grid[y][x].c = "<"
    print("down", room, x, y)

    room = choice(rooms)
    x = randint(room[0]+1, room[0]+room[2]-2)
    y = randint(room[1]+1, room[1]+room[3]-2)
    grid[y][x].c = ">"
    print("up", room, x, y)

    return grid

#braided recursive backtracking maze
def simpleMaze(grid, start=[1,1], steps=2, braids=4):
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
                tile_a = grid[next_tiles[1]][next_tiles[0]]
                tile_b = grid[next_tiles[3]][next_tiles[2]]
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

def closeUpAndCrop(grid):
    s = len(grid)
    for y in range(s):
        for x in range(s):
            if y == 0 or x == 0 or y >= s-2 or x >= s-2:
                grid[y][x].c = "W"
        grid[y] = grid[y][:-1]
    grid = grid[:-1]
    return grid
