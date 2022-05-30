from typing import List
from json import load
import os

PATH = os.path.join("SaettaMcQueen", "datasets", "dataset_md.json")



def getFractalsListFromParsedJson(parsedJSON):
    pop = list()
    max = -1
    for fractal in parsedJSON['fract']:
        transformations = list()
        for i, x in enumerate(fractal["weights"]) :
            transform = fractal['matrixes'][i]
            transformations.append([
                transform[0][0],
                transform[1][0],
                transform[0][1],
                transform[1][1],
                transform[0][2],
                transform[1][2],
                x
            ])
        if(max< len(fractal['weights'])):
            max = len(fractal['weights'])
            matrixes = fractal['matrixes']
    return max, matrixes

def parse(filename):
    with open(filename) as f:
        definition = load(f)

    # check for errors
    if "width" not in definition: raise ValueError('"width" parameter missing')
    if "height" not in definition: raise ValueError('"height" parameter missing')
    if "iterations" not in definition: raise ValueError('"iterations" parameter missing')
    if "fract" not in definition: raise ValueError('"fract" parameter missing')
    #weightedmatrix2function(definition)
    return definition


def StealerIFS():
    parsedJSON = parse(PATH)

    max,fractals = getFractalsListFromParsedJson(parsedJSON)
    #print("Il frattale piu grande e {} con matrici {}".format(max,fractals))

    return fractals