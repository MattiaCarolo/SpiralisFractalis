from __future__ import division

from json import load
from PIL import Image, ImageDraw
from random import uniform
import random
import string

IMAGES_PATH = "./IMGres/"


def get_name_index(index):
    # choose from all lowercase letter
    return IMAGES_PATH + str(index) + ".png"

def weightedmatrix2function(definition):
    fract = dict()
    #print(definition['fract'][0]['weights'])
    for x in definition['fract']:
        formulas = dict()
        #print(x['weights'])
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

def makeNewPoint(x,y, mat):
    x1 = (x * mat[0][0]) + (y * mat[0][1]) + mat[0][2]
    y1 = (x * mat[1][0]) + (y * mat[1][1]) + mat[1][2]
    return (x1,y1)

def process_file(fract, width, height, iterations=1, outputfile='out.png'):

    probability_join = sum(fract['weights'])

    points = set([(0,0)])

    # for each iteration
    for i in range(iterations):
        new_points = set()

        # for each point
        for point in points:

            # decide on which transformation to apply
            rnd = uniform(0, probability_join)
            p_sum = 0
            i = 0
            while(i < len(fract['weights'])):
                p_sum += fract['weights'][i] # sum the single weights
                if rnd <= p_sum:
                    new_points.add(makeNewPoint(*point,fract['matrixes'][i]))
                    break
                i = i + 1

        points.update(new_points)

    # find out image limits determine scaling and translating
    min_x = min(points, key=lambda p:p[0])[0]
    max_x = max(points, key=lambda p:p[0])[0]
    min_y = min(points, key=lambda p:p[1])[1]
    max_y = max(points, key=lambda p:p[1])[1]
    p_width = max_x - min_x
    p_height = max_y - min_y

    width_scale = (width/p_width)
    height_scale = (height/p_height)
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



if __name__ == "__main__":

    import sys

    # if there is one argument and it's not "-"
    if len(sys.argv) > 1 and sys.argv[1] != '-':
        # process each filename in input
        for filename in sys.argv[1:]:
            result = parse(filename)
            process_file(result['fract'], result['width'],
                         result['height'], result['iterations'],
                         filename.split('.')[0] + '.png')
    else:
        # read contents from stdin
        eval( sys.stdin.read() )
        process_file( fract, width, height, iterations)
