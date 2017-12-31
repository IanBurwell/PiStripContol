from ast import literal_eval as make_tuple

def getColorPresetNames():
    found = False
    n = []
    with open('static/data.txt') as f:
        for line in f:
            if found and '[end]' in line:
                return n
            elif '[presetColors]' in line:
                found = True
            elif found:
                (name, data) = line.split(sep=':')
                n.append((name, name))

def getColorPresetDict():
    found = False
    d = {}
    with open('static/data.txt') as f:
        for line in f:
            if found and '[end]' in line:
                return d
            elif '[presetColors]' in line:
                found = True
            elif found:
                (name, data) = line.split(sep=':')
                d[name] = data.split(sep='|')

def getCurrentColors():
    found = False
    c = []
    with open('static/data.txt') as f:
        for line in f:
            if found and '[end]' in line:
                return c
            elif '[currentColors]' in line:
                found = True
            elif found:
                try:
                    c.append(make_tuple(line))
                except Exception as e:
                    c.append((-1,-1,-1))

def setColor(index, color):
    with open('static/data.txt','r') as f:
            data = f.readlines()
    for idx, val in enumerate(data):
        if '[currentColors]' in val:
            if idx+1+index > len(data) or '[end]' in data[idx+1]:
                 return False
            data[idx+1+index] = str(color)+"\n"
            with open('static/data.txt', 'w') as file:
                file.writelines(data)
            return True
    return False


def setSelected(selected):
    with open('static/data.txt','r') as f:
            data = f.readlines()
    for idx, val in enumerate(data):
        if '[selected]' in val:
            data[idx+1] = str(selected)+"\n"
            with open('static/data.txt', 'w') as file:
                file.writelines(data)


def getSelected():
    found = False
    with open('static/data.txt') as f:
        for line in f:
            if '[selected]' in line:
                found = True
            elif found:
                return line
        return None
