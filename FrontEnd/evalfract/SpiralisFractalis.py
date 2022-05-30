from __future__ import division

from evalfract.Stealer import StealerIFS
import json
from json import load
from PIL import Image, ImageDraw

from random import uniform
from numba import njit
import numpy as np
import os.path
from evalfract.Stealer import *
from evalfract.ga import Fractal
import os
import tarfile


SIZE = (800,600)
STEAL = os.path.join("evalfract", "gradient.jpg")

def getJSONFromFractalList(fractalList: List[Fractal], width, height, numIterations):
    geison = {"iterations": numIterations, "width": width, "height": height}

    fracs = list()
    for fractal in fractalList:
        matrixes = list()
        frac = {"weights": [x[-1] for x in fractal.transformations]}
        for transformations in fractal.transformations:
            row1 = [transformations[0], transformations[1], transformations[2]]
            row2 = [transformations[3], transformations[4], transformations[5]]
            rows = [row1, row2, [0, 0, 1.0]]
            matrixes.append(rows)
        frac["matrixes"] = matrixes
        fracs.append(frac)
    geison["fract"] = fracs

    json_object = json.dumps(geison, indent=4)
    with open(os.path.join("..", "FractalFrontend", "FractalFrontend", "src","IMGres", "dataset_md.json"), "w") as outfile:
        outfile.write(json_object)

def get_name_index(index):
    # choose from all lowercase letter FractalFrontend\FractalFrontend\src\IMGres
    return os.path.join("..", "FractalFrontend", "FractalFrontend", "src","IMGres", f"{index}.png")


def weightedmatrix2function(definition):
    fract = dict()
    for x in definition["fract"]:
        formulas = dict()
        for y in x["matrixes"]:
            formulas["x"] = str(y[0][0]) + ""


def parse(filename):
    with open(filename) as f:
        definition = load(f)

    # check for errors
    if "width" not in definition:
        raise ValueError('"width" parameter missing')
    if "height" not in definition:
        raise ValueError('"height" parameter missing')
    if "iterations" not in definition:
        raise ValueError('"iterations" parameter missing')
    if "fract" not in definition:
        raise ValueError('"fract" parameter missing')
    # weightedmatrix2function(definition)
    return definition

def stealColor(x,y, im):
    pix = im.load()
    if(int(x) == 800):
        x  = 799
    else:
        x = int(x)
    if(int(y) == 600):
        y  = 599
    else:
        y = int(y)
    return pix[x,y] # return rgb value

@njit
def makeNewPoint(x, y, transform):
    x1 = (x * transform[0]) + (y * transform[2]) + transform[4]
    y1 = (x * transform[1]) + (y * transform[3]) + transform[5]
    return (x1, y1)


def process_file(fractal, width, height, iterations=1, outputfile='out.png'):
    
    probability_join = sum(x[-1] for x in fractal.transformations)
    f_color = StealerIFS()

    im = Image.open(STEAL)
    im = im.resize(SIZE)

    #OLD: probability_join = sum(fractal['weights'])

    points = set([(0,0)])
    colors = set([(0,0)])

    # for each iteration
    for i in range(iterations):
        new_points = set()
        new_colors = set()
        # for each point
        for point in points:
            # decide on which transformation to apply
            rnd = uniform(0, probability_join)
            p_sum = 0

            for idx, transform in enumerate(fractal.transformations):
                p_sum += transform[-1]
                if rnd <= p_sum:
                    new_points.add(makeNewPoint(*point, np.array(transform)))
                    new_colors.add(makeNewPoint(*point, np.array([item for sublist in f_color[idx] for item in sublist])))
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
        colors.update(new_colors)
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
    image = Image.new( 'RGB', (width, height), color="black")
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
    colors = list(colors)

    for count, point in enumerate(points):
        x = (point[0] - min_x) * scale
        y = height - (point[1] - min_y) * scale

        x_col = (colors[count][0] - min_x) * scale
        y_col = height - (colors[count][1] - min_y) * scale
        #print(point[2])
        #print(type(point[2]))
        try:
            draw.point((x,y),fill=stealColor(x_col,y_col,im))
        except IndexError:
            print("X of image equal to {} while Y equals to {}".format(x_col,y_col))
    
    # save image file
    image.save( outputfile, "PNG" )



def zipGeneration(width, height, numIterations, fractals, generation_number):
    getJSONFromFractalList(fractals, width, height, numIterations)

    with tarfile.open(f"generation_{generation_number}.tar.gz", "w:gz") as tar:
        tar.add(os.path.join("..", "FractalFrontend", "FractalFrontend", "src","IMGres"), arcname=os.path.basename(os.path.join("..", "FractalFrontend", "FractalFrontend", "src","IMGres")))

    # os.remove("/IMGres/dataset_md.json")
