from panda3d.core import NodePath
from .data import wire, makeInstance

colors = {
    "white" : (1,1,1,1),
    "lred" : (1,0.5,0.5,1),
    "red" : (1,0,0,1),
    "dred" : (0.5,0,0,1),
}

def loadFont(fontname="toompoost", solid=True):
    font = {}
    for color in colors:
        font[color] = wire("data/models/egg/font_"+fontname+"/font_"+fontname, color=colors[color], s=1)
    return font

def makeText(font, color, text, width, letter_space=0.5, line_space=(0.2)):
    special = {"(":"parenthesis_l",")":"parenthesis_r","_":"underscore"}
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

            letter_model_node = font[color][0].find("l_"+letter)
            letter_model_node.setPos(0,0,0)
            i = NodePath(letter)
            letter_model_node.instanceTo(i)
            i.setPos(l,0.2,-(line+(line*line_space)))
            i.reparentTo(textnode)

            letter_model_node = font[color][1].find("l_"+letter)
            letter_model_node.setPos(0,0,0)
            i = NodePath(letter)
            letter_model_node.instanceTo(i)
            i.setPos(l,0.21,-(line+(line*line_space)))
            i.reparentTo(textnode)

            l += 2+letter_space
        l += 2 #for the space after every word, sweet!
    textnode.flattenMedium()
    return textnode
