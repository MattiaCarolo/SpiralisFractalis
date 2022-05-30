"""
WSGI config for Fractals project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os



from django.core.wsgi import get_wsgi_application
from django.db import IntegrityError


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fractals.settings')

# from SaettaMcQueen.src.SpiralisFractalis import *
# from SaettaMcQueen.src.utils import *
from evalfract.ga import *
from evalfract.models import ImageModel, Settings

from json import load

def delete_images():
    imgs = ImageModel.objects.all().delete()


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
        pop.append(Fractal(transformations= transformations))
        if(max< len(fractal['weights'])):
            max = len(fractal['weights'])
            matrixes = fractal['matrixes']
    return pop

def StealerIFS():
    parsedJSON = parse(os.path.join("SaettaMcQueen", "datasets", "dataset_md.json"))

    fractals = getFractalsListFromParsedJson(parsedJSON)
    #print("Il frattale piu grande e {} con matrici {}".format(max,fractals))

    return fractals



def transformation_to_string(transformations):
    t = []
    for ts in transformations:
        t.append(f"{str(ts)[1:-1]}")
    return ';'.join(t)

def string_to_transformations(string):
    res = []
    for s in string.split(';'):
        res.append([float(x) for x in s.split(',')])
    return res

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

def load_fractals():
    parsedJSON = parse(os.path.join("SaettaMcQueen", "datasets", "dataset_md.json"))
    fractals = getFractalsListFromParsedJson(parsedJSON)

    try:
        settings = Settings.objects.create(
            width = parsedJSON["width"],
            height = parsedJSON["height"],
            num_iteration = parsedJSON["iterations"],
            dataset_filename = os.path.join("SaettaMcQueen", "datasets", "dataset_md.json")
        )
    except IntegrityError:
        pass
    
    for i, fractal in enumerate(fractals[:-1]):
        f = ImageModel.objects.create(
            id= i,
            image_path= os.path.join(".", "src", "IMGresStart", f"{i}.png"),
            transformations = transformation_to_string(fractal.transformations)
        )
        f.save()

delete_images()
load_fractals()


application = get_wsgi_application()
