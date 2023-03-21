from __future__ import division

from Stealer import StealerIFS
import json
from json import load
from tkinter import Y
from PIL import Image, ImageDraw
from utils import getJSONFromFractalList
from random import uniform
from numba import jit, cuda, vectorize, guvectorize, float32
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
    return f"{IMAGES_PATH}{index}.png" 


def weightedmatrix2function(definition):
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
    return im[x, y]

#@guvectorize(['(float32, float32, float32[:], float32[:])'],'(),(),(n)->(n)', target='cuda')
#@vectorize([float32[:](float32,float32,float32[:])])
def makeNewPoint(x, y, transform):
    # w(x,y) = (ax+by+e, cx+dy+f) = (x1, y1)
    # transform = [a, b, c, d, e, f]
    #x1 = (x * transform[0]) + (y * transform[1]) + transform[4]
    #y1 = (x * transform[2]) + (y * transform[3]) + transform[5]
    #return x1, y1
    return (
        (x * transform[0]) + (y * transform[1]) + transform[4],
        (x * transform[2]) + (y * transform[3]) + transform[5]
    )
# 
# @cuda.jit
# def makeNewPointX(x, y, transform):
#     return x * transform[0] + (y * transform[1]) + transform[4]
# 
# @cuda.jit
# def makeNewPointY(x, y, transform):
#     return x * transform[2] + y * transform[3] + transform[5]
# 

@jit
def getWidthScale(p_width:float, width:float): 
    if p_width == 0.0:
        return width
    elif width == 0.0:
        return 0.0001
    else:
        return width / p_width

@jit
def getHeightScale(p_height:float, height:float):
    if p_height == 0.0:
        return height
    elif height == 0.0:
        return 0.0001
    else:
        return height / p_height
    
@jit
def getCwidthScale(cp_width:float, width:float):
    if cp_width == 0.0:
        return width
    elif width == 0.0:
        return 0.0001
    else:
        return width / cp_width

@jit
def getCheightScale(cp_height:float, width:float, height:float):
    if cp_height == 0.0:
        return width
    elif height == 0.0:
        return 0.0001
    else:
        return height / cp_height

def getPointsAndColors(fractal, f_color, probability_join, iterations):
    points = set([(0, 0)])
    # by using a list for colors, we are sure that # of colors element 
    # will never be less than # of points elements
    colors = [(0, 0)]
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
                    #transform = np.array(transform)
                    #f_color_idx = np.array(f_color[idx])
                    # I make a new binary point from previous binary points
                    
                    
                    new_points.add(makeNewPoint(point[0], point[1], np.array(transform)))
                    #new_points.add((
                    #    makeNewPointX(point[0], point[1], transform),
                    #    makeNewPointY(point[0], point[1], transform)
                    #))
                    # I make a new color point from previous color points
                    colors.append(makeNewPoint(colors[index][0], colors[index][1], np.array(f_color[idx])))
                    #colors.append((
                    #    makeNewPointX(colors[index][0], colors[index][1], f_color_idx),
                    #    makeNewPointY(colors[index][0], colors[index][1], f_color_idx)
                    #))
                    
                    break
                i = i + 1

        # here we will probably drop some points as it is a set
        points.update(new_points)
        
    return points, colors

# min = (mix_x, min_y), same for cmin
def generateImage(src_image, width, height, colors, points, min, cmin, scale, cscale):
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)
    
    # src_image = np.array(src_image, dtype=np.float32)
    src_image = src_image.load()
        
    for count, point in tqdm(enumerate(points)):
        x = (point[0] - min[0]) * scale
        y = height - (point[1] - min[1]) * scale

        x_col = (colors[count][0] - cmin[0]) * cscale
        y_col = height - (colors[count][1] - cmin[1]) * cscale

        try:
            fill = stealColor(x_col, y_col, src_image)
            draw.point((x, y), fill)
            
        except IndexError:
            print("X of image equal to {} while Y equals to {}".format(x_col, y_col))
       

    return image

def process_file(fractal, width, height, img_index, iterations=1, outputfile="out.png"):

    probability_join = sum(x[-1] for x in fractal.transformations)
    f_color = StealerIFS()

    if img_index == 0:
        random.shuffle(GRADIENT_INDEX)

    im = Image.open(STEAL.replace("*", str(GRADIENT_INDEX[img_index])))
    im = im.resize(SIZE)

    points, colors = getPointsAndColors(fractal, f_color, probability_join, iterations)

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
    width_scale = getWidthScale(p_width, width)

    # height_scale = (height/p_height)
    height_scale = getHeightScale(p_height, height)

    # cwidth_scale = (width/cp_width)
    cwidth_scale = getCwidthScale(cp_width, width)

    # cheight_scale = (height/cp_height)
    cheight_scale = getCheightScale(cp_height, width, height)
    
    scale = min(width_scale, height_scale)
    cscale = min(cwidth_scale, cheight_scale)

    # create new image
    image = generateImage(im, width, height, colors, points, (min_x, min_y), (cmin_x, cmin_y), scale, cscale)
   
    # save image file
    image.save(outputfile, "PNG")




def zipGeneration(width, height, numIterations, fractals, generation_number):
    getJSONFromFractalList(fractals, width, height, numIterations)

    with tarfile.open(f"generation_{generation_number}.tar.gz", "w:gz") as tar:
        tar.add(IMAGES_PATH, arcname=os.path.basename(IMAGES_PATH))

    # os.remove("/IMGres/dataset_md.json")
