from .readfile import folderToTextures

class Tile():
    def __init__(self, map, x, y):
        self.map = map
        self.x, self.y = x, y
        self.prefabs = [
            {"shape":"floor", "tex":"roman", "type":"floor"},
        ]
        self.move_cost  = 1

class Map():
    def __init__(self, size):
        self.size = size
        self.map_model = render.attachNewNode("map_model")
        self.map_objects = render.attachNewNode("map_objects")
        #get all shapes from single egg
        self.shapes = {}
        shape_model = loader.loadModel("data/shapes.egg")
        shapes = shape_model.findAllMatches('**/+GeomNode')
        for shape in shapes: self.shapes[shape.get_name()] = shape
        #load some test textures, automate later
        self.textures = {}
        self.textures["roman"] = folderToTextures("data/textures/map/roman")
        self.textures["creatures"] = folderToTextures("data/textures/creatures")
        #only copy shape if i need it in a different texture, instance those
        self.unique = {}
        for shape in self.shapes:
            self.unique[shape] = {}

        self.grid = []
        for y in range(self.size):
            self.grid.append([])
            for x in range(self.size):
                self.grid[y].append(Tile(self, x ,y))
        #TODO: ADD WALLS, DOORS AND OBJECTS TO TILES, THEN CALCULATE PREFABS
        self.build_map_model()

    def build_map_model(self):
        for y,row in enumerate(self.grid):
            for x,tile in enumerate(row):
                for prefab in tile.prefabs:
                    model = self.make_model(prefab,x,y)
        self.map_model.flattenStrong()

    def make_model(self, prefab, x, y):
        type = prefab["type"]
        try:
            model = self.unique[prefab["shape"]][prefab["tex"]+"_"+type]
        except:
            tex = self.textures[prefab["tex"]][type]
            shape = self.shapes[prefab["shape"]]
            model = shape.__copy__()
            model.setTexture(tex, 1)
            self.unique[prefab["shape"]][prefab["tex"]+"_"+type] = model
        node = self.map_model.attachNewNode(type+"_"+str(x)+"_"+str(y))
        model.instanceTo(node)
        node.setPos((x,y,0))
        if "dir" in prefab:
            model.setHpr((prefab["dir"]*90,0,0))
        if type == "object":
            model.setBillboardPointEye()
        return node
