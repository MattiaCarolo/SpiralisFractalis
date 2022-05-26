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

def getJSONFromFractalList(fractalList: List[Fractal], width, height, numIterations):
    geison = { "iterations": numIterations, "width":width, "height":height}

    fracs = list()
    for fractal in fractalList:
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


    # data = {
    #     "iterations": numIterations,
    #     "width": width,
    #     "height": height,
    #     "fract": []
    # }
    # for fractal in fractalList:
    #     fract = {
    #         "weights": [],
    #         "matrixes": []
    #     }
    #     for transform in fractal.transformations:
    #         fract["weights"].append(transform[-1])
    #         fract["matrixes"].append([
    #             [transform[0], transform[2], transform[4]],
    #             [transform[1], transform[3], transform[5]],
    #             [0., 0., 1.]
    #         ])

    #     data["fract"].append(fract)
    
    # json_object = json.dumps(data, indent=4)
    # with open('./IMGres/dataset_md.json', 'w') as outfile:
    #     outfile.write(json_object)