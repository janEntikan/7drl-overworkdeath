import sys
import os

def make_wireframe(folder):
    filename = "data/models/egg/" + folder+"/"+folder+".egg"
    print("wireframifying " + filename)
    filename_wire = filename[:-4]+"_wire.egg"
    filename_model = filename[:-4]+"_model.egg"
    eggfile = open(filename, "r")
    wirefile = open(filename_wire, "w")
    modelfile = open(filename_model, "w")
    m = """<CoordinateSystem> { Z-up }"""
    modelfile.write(m + "\n")
    wirefile.write(m + "\n")

    with eggfile as ef:
        line = ef.readline()
        cnt = 0
        while line:
            line = ef.readline()
            strip = line.strip()
            if len(strip) > 0:
                if strip[:11] == "<VertexRef>":
                    modelfile.write(strip + "\n")
                    split = strip.split(" ")
                    new = []
                    numbs = []
                    for word in split:
                        try:
                            numbs.append(int(word))
                        except:
                            new.append(word)
                    numbs.append(numbs[0])
                    new = new[:2] + numbs + new[2:]
                    s = ""
                    for i in new:
                        s += str(i) + " "
                    wirefile.write(s + "\n")
                elif strip[:9] == "<Polygon>":
                    modelfile.write(strip + "\n")
                    new = "<Line> " + strip[9:]
                    wirefile.write(new + "\n")
                elif strip[:6] == "<MRef>":
                    wirefile.write(strip + "\n")
                    new = "<MRef> { pitch }"
                    modelfile.write(new + "\n")
                else:
                    modelfile.write(strip + "\n")
                    wirefile.write(strip + "\n")
            else:
                modelfile.write(strip + "\n")
                wirefile.write(strip + "\n")
            cnt += 1
    eggfile.close()
    wirefile.close()
    modelfile.close()
