from panda3d.core import SamplerState
from .readfile import cfgdict

def genShapes(loader, cfg):
    models = {}
    shape_model = loader.loadModel("data/shapes.egg")
    shapes =
    for shape in shapes: models[shape.get_name()] = shape
    template = cfgdict("data/"+cfg)
    textures = {}
    for texture in template["textures"]:
        textures[texture] = loader.loadTexture("data/textures/"+template["textures"][texture]+".png")
        textures[texture].setMagfilter(SamplerState.FT_nearest)
        textures[texture].setMinfilter(SamplerState.FT_nearest)

    floors = {}
    for floor in template["floors"]:
        floors[floor] = models["floor"].__copy__()
        floors[floor].setTexture(textures[template["floors"][floor]],1)

    ceilings = {}
    for ceiling in template["ceilings"]:
        vals = template["ceilings"][ceiling]
        ceilings[ceiling] = models[vals[0]].__copy__()
        ceilings[ceiling].setTexture(textures[vals[1]],1)

    structures = {}
    for structure in template["structures"]:
        vals = template["structures"][structure]
        structures[structure] = models[vals[0]].__copy__()
        structures[structure].setTexture(textures[vals[1]], 1)
        structures[structure] = (structures[structure], vals[2])

    doors = {}
    for door in template["doors"]:
        vals = template["doors"][door]
        doors[door] = models[vals[0]].__copy__()
        vals[1] = textures[vals[1]]
        vals[2] = textures[vals[2]]
        doors[door].setTexture(vals[2], 1)
        # vals are shape, tex_open, tex_closed, state, strength

        doors[door] = (doors[door], vals[:])

    objects = {}
    for object in template["objects"]:
        objects[object] = models[template["objects"][object][0]].__copy__()
        objects[object].setTexture(textures[template["objects"][object][1]], 1)

    shapes = {}
    shapes["structures"] = structures
    shapes["floors"] = floors
    shapes["ceilings"] = ceilings
    shapes["doors"] = doors
    shapes["objects"] = objects
    return shapes
