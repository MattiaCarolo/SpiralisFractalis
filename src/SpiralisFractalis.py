from __future__ import division

from Stealer import StealerIFS
import json
from json import load
from tkinter import Y
from PIL import Image, ImageDraw
from utils import getJSONFromFractalList
from random import uniform
from numba import njit
import numpy as np
import os.path
from Stealer import *
import random
from tqdm import tqdm
import os
import tarfile

IMAGES_PATH = "./IMGres/"
STEAL = "./gradient_img/gradient_*.jpeg"
# STEAL = "./gradient_img/natural.jpg"
SIZE = 1920, 1080
GRADIENT_INDEX = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def get_name_index(index):
    # choose from all lowercase letter
    return IMAGES_PATH + str(index) + ".png"


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


"""
:param x: x coordinate in image im
:param y: x coordinate in image im
:param im: image used to capture colors
:return RGB_Tuple: returns the RGB value as a tuple in the pixel with (x,y) coordinates

Function that given the coordinates of the pixel and an image, returns the color of the given pixel represented as
an RGB value
"""
def stealColor(x, y, im):
    if int(x) >= 1920:
        x = 1919
    else:
        x = int(x)
    if int(y) >= 1080:
        y = 1079
    else:
        y = int(y)
    return im[x, y]  # return rgb value


@njit
def makeNewPoint(x, y, transform):
    # w(x,y) = (ax+by+e, cx+dy+f) = (x1, y1)
    # transform = [a, b, c, d, e, f]
    x1 = (x * transform[0]) + (y * transform[1]) + transform[4]
    y1 = (x * transform[2]) + (y * transform[3]) + transform[5]
    return (x1, y1)



def process_file(fractal, width, height, img_index, iterations=1, outputfile="out.png"):

    probability_join = sum(x[-1] for x in fractal.transformations)
    f_color = StealerIFS()

    if img_index == 0:
        random.shuffle(GRADIENT_INDEX)
    im = Image.open(STEAL.replace("*", str(GRADIENT_INDEX[img_index])))
    im = im.resize(SIZE)

    points = set([(0, 0)])
    # by using a list for colors, we are sure that # of colors element 
    # will never be less than # of points elements
    colors = [(0, 0)]

    # for each iteration
    for i in tqdm(range(iterations)):
        new_points = set()
        # for each point
        for index, point in enumerate(points):
            # decide on which transformation to apply
            rnd = uniform(0, probability_join)
            p_sum = 0

            for idx, transform in enumerate(fractal.transformations):
                p_sum += transform[-1]
                if rnd <= p_sum:
                    # I make a new binary point from previous binary points
                    new_points.add(makeNewPoint(*point, np.array(transform)))
                    # I make a new color point from previous color points
                    colors.append(makeNewPoint(*colors[index], np.array(f_color[idx])))
                    
                    break
                i = i + 1

        # here we will probably drop some points as it is a set
        points.update(new_points)

    # find out image limits determine scaling and translating
    min_x = min(points, key=lambda p: p[0])[0]
    max_x = max(points, key=lambda p: p[0])[0]
    min_y = min(points, key=lambda p: p[1])[1]
    max_y = max(points, key=lambda p: p[1])[1]
    p_width = max_x - min_x
    p_height = max_y - min_y

    # find out color image limits determine scaling and translating
    cmin_x = min(colors, key=lambda p: p[0])[0]
    cmax_x = max(colors, key=lambda p: p[0])[0]
    cmin_y = min(colors, key=lambda p: p[1])[1]
    cmax_y = max(colors, key=lambda p: p[1])[1]
    cp_width = cmax_x - cmin_x
    cp_height = cmax_y - cmin_y

    # width_scale = (width/p_width)
    if p_width == 0.0:
        width_scale = width
    elif width == 0.0:
        width_scale = 0.0001
    else:
        width_scale = width / p_width

    # height_scale = (height/p_height)
    if p_height == 0.0:
        height_scale = height
    elif height == 0.0:
        height_scale = 0.0001
    else:
        height_scale = height / p_height

    # cwidth_scale = (width/cp_width)
    if cp_width == 0.0:
        cwidth_scale = width
    elif width == 0.0:
        cwidth_scale = 0.0001
    else:
        cwidth_scale = width / cp_width

    # cheight_scale = (height/cp_height)
    if cp_height == 0.0:
        cheight_scale = width
    elif height == 0.0:
        cheight_scale = 0.0001
    else:
        cheight_scale = height / cp_height

    
    scale = min(width_scale, height_scale)
    cscale = min(cwidth_scale, cheight_scale)

    # create new image
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)

    im = im.load()

    for count, point in tqdm(enumerate(points)):
        x = (point[0] - min_x) * scale
        y = height - (point[1] - min_y) * scale

        x_col = (colors[count][0] - cmin_x) * cscale
        y_col = height - (colors[count][1] - cmin_y) * cscale

        try:
            draw.point((x, y), fill=stealColor(x_col, y_col, im))
        except IndexError:
            print("X of image equal to {} while Y equals to {}".format(x_col, y_col))

    # save image file
    image.save(outputfile, "PNG")


def zipGeneration(width, height, numIterations, fractals, generation_number):
    getJSONFromFractalList(fractals, width, height, numIterations)

    with tarfile.open(f"generation_{generation_number}.tar.gz", "w:gz") as tar:
        tar.add(IMAGES_PATH, arcname=os.path.basename(IMAGES_PATH))

    # os.remove("/IMGres/dataset_md.json")
