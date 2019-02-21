from panda3d.core import NodePath
from .colors import colors
from .data import wire, makeInstance

def load_font(root, fontname="toompoost", solid=True):
    font = {}
    for color in colors:
        font[color] = wire(
            root, "data/models/fonts/"+fontname+"/"+fontname, color=colors[color])
    return font

def makeText(root, text, color, width, letter_space=0.5, line_space=(0.2)):
    special = {"{":"bracket_l","}":"bracket_r","_":"underscore"}
    textnode = NodePath(text[:10])
    words = text.split(" ")
    l = 0
    line = 0
    for word in words:
        if l + len(word) > width*2:
            line += 3+line_space
            l = 0
        for letter in word:
            if letter in special:
                letter = special[letter]
            letter = letter.lower()
            letter_model_node = root.fonts["toompoost"][color][0].find("l_"+letter)
            letter_model_node.setPos(0,0,0)
            i = makeInstance(letter, letter_model_node, pos=(l,0,-(line+(line*line_space))))
            i.reparentTo(textnode)
            l += 2+letter_space
        l += 1 #for the space after every word, sweet!
    textnode.flattenLight()
    return textnode
