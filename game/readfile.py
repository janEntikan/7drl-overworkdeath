from os import listdir

def folderToTextures(folder):
    dic = {}
    files = listdir(folder)
    for file in files:
        if file[-4:] == ".png":
            dic[file[:-4]] = game.loader.loadTexture(folder+"/"+file)
    return dic


def string_file_list(filename, splitChar=" "):
    with open(filename, "r") as ins:
        lines = []
        for string in ins:
            if not string[0] == "#":
                string = string.strip("\n")
                string = string.split(splitChar)
                for w in string:
                    w = w.expandtabs()
                while "" in string: string.remove("")
                for w, word in enumerate(string):
                    if word == "True":
                        string[w] = True
                    elif word == "False":
                        string[w] = False
                    else:
                        try:
                            word = float(word)
                            if word.is_integer(): word = int(word)
                            string[w] = word
                        except ValueError:
                            pass
                if not string == []:
                    lines.append(string)
    return lines

def cfgdict(filename=None):
    lines = string_file_list(filename)
    options = {}
    for line in lines:
        if line[0][0] == "_" and line[0][1] == "_":
            cat = line[0][:-2]
            cat = cat[2:]
            options[cat] = {}
        else:
            options[cat][line[0]] = line[1:]
            if len(options[cat][line[0]]) == 1:
                options[cat][line[0]] = options[cat][line[0]][0]
    return options

def gplpalette(name):
    lines = string_file_list("data/pal/"+name+".gpl")
    palette = {"colors":{}, "values":[], "names":[]}
    for line in lines:
        if len(line) == 4:
            rgb = [line[0], line[1], line[2]]
            name = line[3]
            palette["colors"][name] = rgb
            palette["values"].append(rgb)
            palette["names"].append(name)
    return palette

def csvdict(filename):
    lines = string_file_list(filename, ",")
    current_keys = []
    output_dict = {}
    for line in lines:
        if line[0][0] == "_":
            l = line[0][1:]
            output_dict[l] = {}
            keys = line[1:]
            while "" in keys: keys.remove("")
            if len(keys) > 0:
                current_keys = []
                for key in keys:
                    current_keys.append(key)
        else:
            g = line[0]
            output_dict[l][g] = {}
            for v, val in enumerate(line[1:]):
                output_dict[l][g][current_keys[v]] = val
    return output_dict
