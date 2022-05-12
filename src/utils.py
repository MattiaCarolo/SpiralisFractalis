import cv2.cv2 as cv
import os
from PIL import ImageTk, Image
from components.ga import Fractal
from typing import List
import json

def get_img(path, shape):
    img = cv.imread(path)
    img = cv.resize(img, dsize=shape, interpolation=cv.INTER_LINEAR)
    (b, g, r) = cv.split(img)
    return ImageTk.PhotoImage(Image.fromarray(cv.merge((r,g,b))))

def get_images_paths(imgs_path):
    return [os.path.join(imgs_path, im) for im in os.listdir(imgs_path)]   

def getFractalsListFromParsedJson(parsedJSON):
    pop = list()
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
        pop.append(Fractal(transformations=transformations))
    return pop 

def getJSONFromFractalList(fractalList: List[Fractal], width, height, numIteration):
    data = {
        "iterations": numIteration,
        "width": width,
        "height": height,
        "fract": []
    }
    for fractal in fractalList:
        fract = {
            "weights": [],
            "matrixes": []
        }
        for transform in fractal.transformations:
            fract["weights"].append(transform[-1])
            fract["matrixes"].append([
                [transform[0], transform[2], transform[4]],
                [transform[1], transform[3], transform[5]]
            ])

        data["fract"].append(fract)
    
    with open('json_data.json', 'w') as outfile:
        json.dump(json.dumps(data), outfile)