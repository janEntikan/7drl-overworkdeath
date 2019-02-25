from math import hypot, sin, cos, radians
from panda3d.core import Vec3, Point3

def makeInstance(name, instance_model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1)):
	instance = NodePath(name)
	instance_model.instanceTo(instance)
	instance.setPos(pos)
	instance.setHpr(hpr)
	instance.setScale(scale)
	return instance

def fireRay(fromObject, toObject):
	pFrom = render.getRelativePoint(fromObject, Point3())
	pTo = render.getRelativePoint(toObject, Point3())
	result = _root.bulletworld.rayTestClosest(pFrom, pTo)
	if result.hasHit():
		return result

def flipFaces(model):
	geomNodeCollection = model.findAllMatches('**/+GeomNode')
	for nodePath in geomNodeCollection:
		geomNode = nodePath.node()
		for i in range(geomNode.getNumGeoms()):
			geom = geomNode.modifyGeom(i)
			geom.reverseInPlace()
	return model

# -*- coding: utf-8 -*-
def getByTag(node, tag):
	"""
	Given a name and value this returns a list of all objects in the structure that have this tag.
	"""
	if node == None: return []
	col = node.findAllMatches('**/=' + tag)
	ret = []
	for i in range(col.get_num_paths()):
		ret.append(col[i])
	return ret

def stringToTuple(string):
# Convert string of numbers seperated by comma to tuple
	t = tuple([float(s) for s in string.split(',')])
	return t

def stringToTupleInt(string):
# Convert string of numbers seperated by comma to tuple
	t = tuple([int(s) for s in string.split(',')])
	return t

def flipFaces(model):
	geomNodeCollection = model.findAllMatches('**/+GeomNode')
	for nodePath in geomNodeCollection:
		geomNode = nodePath.node()
		for i in range(geomNode.getNumGeoms()):
			geom = geomNode.modifyGeom(i)
			geom.reverseInPlace()
	return model

def getDistance(a, b):
	dist = hypot(b[0]-a[0], b[1]-a[1])
	return dist

def distance_angle(x,y,angle,length):
	x += sin(radians(angle))*length
	y += cos(radians(angle))*length
	return x, y

def limit_number(n, maximum, minimum):
	if n > maximum: n = maximum
	elif n < minimum: n = minimum
	return n

def merge_two_dicts(dict_a, dict_b):
	dict_c = dict_a.copy()
	dict_c.update(dict_b)
	return dict_c

def grid2(size=[1,1],default=None):
	w,h = size
	grid = []
	for y in range(h):
		grid.append([])
		for x in range(w):
			try:
				t = default()
			except:
				t = default
			grid[y].append(t)
	return grid

def grid3(size=[1,1,1],default=None):
	w,h,d = size
	grid = []
	for z in range(d):
		grid.append([])
		for y in range(h):
			grid[z].append([])
			for x in range(w):
				grid[z][y].append(default)
	return grid
