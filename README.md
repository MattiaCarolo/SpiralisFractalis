# Fractalis Spiralis - Bio-Inspired AI Project UNITN a.y. 2021/2022

## What is this project

We wanted to delve into the generative art field and Fractalis Spiralis is what we got. Fractalis Spiralis combines fractal theory with Evolutionary Algorithms in order to create fractal images that mantains the inner properties of a fractal while creating new patterns without the need of a human to intervene.
Here the only action the user can do is the one of giving a score to each image according to their own preference

## Structure :monorail:

The source code can be found at `src` folder. There you can find all the files that help building the software.
More specifically:

- Inside `src/components` we can find the frontend of our application represented by `App.py`
- Still inside the same folder `ga.py` will take care of the evolutionary part
- The backend part can be found at root level represented by `SpiralisFractalis.py` that will take care of the rendering of both fractals

Another important folder is the `datasets` one where we can initialize the population from which we create the new images.

## How to run

The general basic terminal input to start the project is

``` bash
python main.py <path to transformation dataset>
```

if using the normal structure of the project it can be written as

``` bash
python main.py datasets/dataset_*.json
```

Following this 

credits to https://github.com/rodrigosetti/ifs