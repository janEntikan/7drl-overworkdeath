from panda3d.core import RenderModeAttrib, Material, ColorAttrib, NodePath
from panda3d.bullet import BulletTriangleMesh, BulletTriangleMeshShape, BulletBoxShape
from .tools import makeInstance

def loadShapes(loader):
    data = {}
    data["shapes"] = {}
    shape_model = loader.loadModel("data/shapes.egg")
    shapes = shape_model.findAllMatches('**/+GeomNode')
    for shape in shapes: data["shapes"][shape.get_name()] = shape

def wire(root, folder, color=None):
    w = loader.loadModel(folder + "_wire.egg")
    for child in w.getChildren():
        m = child.findMaterial("*")
        if not color == None:
            c = color
        elif not m == None:
            c = m.getDiffuse()
        else:
            if color == None:
                c = (1,1,1,1)
            else:
                c = color
        child.node().setAttrib(RenderModeAttrib.make(root.line[0], root.line[1], False, c))
    m = loader.loadModel(folder + "_model.egg")
    m.flattenStrong()
    return w, m

def loadWire(root, folder, color=None):
    w, m = wire(root, folder, color)
    return w,m

def nodesToModel(instance_name, node_model, instance_model):
    nodepath = NodePath(instance_name + "_root")
    for c, child in enumerate(node_model.getChildren()):
        pos = child.getPos()
        hpr = child.getHpr()
        scale = child.getScale()
        i = makeInstance(
            instance_name + "_" +  str(c) + "_wire",
            instance_model[0], pos, hpr, scale)
        i.reparentTo(nodepath)
        i = makeInstance(
            instance_name + "_" +  str(c) + "_model",
            instance_model[1], pos, hpr, scale)
        i.reparentTo(nodepath)
    nodepath.flattenStrong()
    return nodepath
