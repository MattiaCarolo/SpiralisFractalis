from __future__ import division

import json
from json import load
from PIL import Image, ImageDraw
from random import uniform
from numba import njit
import numpy as np
import os.path

import os
import tarfile

IMAGES_PATH = "./IMGres/"


def get_name_index(index):
    # choose from all lowercase letter
    return IMAGES_PATH + str(index) + ".png"

def weightedmatrix2function(definition):
    fract = dict()
    for x in definition['fract']:
        formulas = dict()
        for y in x['matrixes']:
            formulas["x"]= str(y[0][0]) + "" 



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

@njit
def makeNewPoint(x, y, transform):
    x1 = (x * transform[0]) + (y * transform[2]) + transform[4]
    y1 = (x * transform[1]) + (y * transform[3]) + transform[5]
    return (x1,y1)

def process_file(fractal, width, height, iterations=1, outputfile='out.png'):

    probability_join = sum(x[-1] for x in fractal.transformations)

    #OLD: probability_join = sum(fractal['weights'])

    points = set([(0,0)])

    # for each iteration
    for i in range(iterations):
        new_points = set()

        # for each point
        for point in points:
            # decide on which transformation to apply
            rnd = uniform(0, probability_join)
            p_sum = 0

            for transform in fractal.transformations:
                p_sum += transform[-1]
                if rnd <= p_sum:
                    new_points.add(makeNewPoint(*point, np.array(transform)))
                    break
                i = i + 1

            """ OLD
            i = 0
            while(i < len(fract['weights'])):
                p_sum += fract['weights'][i] # sum the single weights
                if rnd <= p_sum:
                    new_points.add(makeNewPoint(*point,fract['matrixes'][i]))
                    break
                i = i + 1
            """

        points.update(new_points)

    # find out image limits determine scaling and translating
    min_x = min(points, key=lambda p:p[0])[0]
    max_x = max(points, key=lambda p:p[0])[0]
    min_y = min(points, key=lambda p:p[1])[1]
    max_y = max(points, key=lambda p:p[1])[1]
    p_width = max_x - min_x
    p_height = max_y - min_y

    #width_scale = (width/p_width)

    if p_width == 0.0:
        width_scale = width
    elif width == 0.0:
        width_scale = 0.0001
    else:
        width_scale = (width/p_width)

    if p_height == 0.0:
        height_scale = width
    elif height == 0.0:
        height_scale = 0.0001
    else:
        height_scale = (height/p_height)

    #height_scale = (height/p_height)
    scale = min(width_scale, height_scale)

    # create new image
    image = Image.new( 'RGB', (width, height))
    draw = ImageDraw.Draw(image)
    """
    # plot points
    for point in points:
        x = (point[0] - min_x) * scale
        y = height - (point[1] - min_y) * scale
        draw.point((x,y))
    """
    """
    WARNING

    CREA BOIS MOLTO CICCIONI / bello
    """
    for point in points:
        x = (point[0] - min_x) * width_scale
        y = height - (point[1] - min_y) * height_scale
        draw.point((x,y))
    

    # save image file
    image.save( outputfile, "PNG" )


def zipGeneration(width, height, numIterations, fractals):
    
    geison = { "iterations": numIterations, "width":width, "height":height}

    fracs = list()
    for fractal in fractals:
        matrixes = list()
        frac = {"weights": [x[-1] for x in fractal.transformations]}
        for transformations in fractal.transformations:
            row1 = [transformations[0],transformations[1],transformations[2]]
            row2 = [transformations[3],transformations[4],transformations[5]]
            rows = [row1,row2,[0,0,1.0]]
            matrixes.append(rows)
        frac["matrixes"] = matrixes
        fracs.append(frac)
    geison["fract"] = fracs

    json_object = json.dumps(geison, indent=4)
    with open("./IMGres/dataset_md.json", "w") as outfile:
        outfile.write(json_object)

    with tarfile.open("generation.tar.gz", "w:gz") as tar:
        tar.add(IMAGES_PATH, arcname=os.path.basename(IMAGES_PATH))

    #os.remove("/IMGres/dataset_md.json")
