from panda3d.core import RenderModeAttrib, Material, ColorAttrib, NodePath
from panda3d.bullet import BulletTriangleMesh, BulletTriangleMeshShape, BulletBoxShape

def loadShapes(loader):
    data = {}
    data["shapes"] = {}
    shape_model = loader.loadModel("data/shapes.egg")
    shapes = shape_model.findAllMatches('**/+GeomNode')
    for shape in shapes: data["shapes"][shape.get_name()] = shape

def loadTexturesFromFolder(loader, folder):
    dict = {}

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

def bulletshape(root, folder, model, dynamic=False):
    if model == True:
        h = loader.loadModel(folder + "_hit.egg")
    else:
        h = model
    mesh = BulletTriangleMesh()
    geomNodeCollection = h.findAllMatches('**/+GeomNode')
    for nodePath in geomNodeCollection:
        geomNode = nodePath.node()
        for i in range(geomNode.getNumGeoms()):
            geom = geomNode.getGeom(i)
            state = geomNode.getGeomState(i)
            mesh.addGeom(geom)
    shape = BulletTriangleMeshShape(mesh, dynamic=dynamic)
    return shape

def loadWire(root, folder, color=None, dynamic=False, hitmodel=False):
    w, m = wire(root, folder, color)
    if hitmodel == False: hitmodel = m
    shape = bulletshape(root, folder, hitmodel, dynamic)
    return w,m,shape

def makeInstance(name, instance_model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1)):
    instance = NodePath(name)
    instance_model.instanceTo(instance)
    instance.setPos(pos)
    instance.setHpr(hpr)
    instance.setScale(scale)
    return instance

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
