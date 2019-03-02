from panda3d.core import RenderModeAttrib, Material, ColorAttrib, NodePath
from panda3d.bullet import BulletTriangleMesh, BulletTriangleMeshShape, BulletBoxShape
from .tools import makeInstance

def wire(folder, color=None, s=3):
    w = loader.loadModel(folder + "_wire.egg")
    d=5
    for child in w.getChildren():
        m = child.findMaterial("*")
        if not color == None:
            c = color
        elif not m == None:
            d=1
            c = (1,1,1,1)
        else:
            if color == None:
                c = (1,1,1,1)
            else:
                c = color
        child.node().setAttrib(RenderModeAttrib.make(d, s, False, c))
    m = loader.loadModel(folder + "_model.egg")

    return w, m

def getParts(folder):
    objects = {}
    parts = wire(folder)
    parts_wire = parts[0].findAllMatches('**/+GeomNode')
    parts_model = parts[1].findAllMatches('**/+GeomNode')
    #print(parts_wire)
    for w, wireframe in enumerate(parts_wire):
        parts_wire[w].setPos(0,0,0)
        parts_model[w].setPos(0,0,0)
        parts_wire[w].flattenStrong()
        parts_model[w].flattenStrong()
        objects[wireframe.get_name()] = parts_wire[w], parts_model[w]
    return objects
