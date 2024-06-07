# Spiralis Fractalis - Bio-Inspired AI Project UNITN a.y. 2021/2022

## What is this project :question:

We wanted to delve into the *generative art field* and Fractalis Spiralis is what we got. Fractalis Spiralis combines fractal theory with *Evolutionary Algorithms* in order to create fractal images that mantains the inner properties of a fractal while creating new patterns without the need of a human to intervene.
Here the only action the user can do is giving a score to each image according to their own preference

## Structure :package:

The source code can be found at `src` folder. There you can find all the files that help building the software.
More specifically:

- Inside `src/components` we can find the frontend of our application represented by `App.py`
- Still inside the same folder `ga.py` will take care of the evolutionary part
- The backend part can be found at root level represented by `SpiralisFractalis.py` that will take care of the rendering and coloring the fractals

Another important folder is `datasets`, where we can find the json from which you can reinitialize the population.

## How to run :computer:
Before running, we suggest to install the basic requirements that are found inside our `requirements.txt` file however you want.

The general basic terminal input to start the project is

``` bash
python src/main.py <path to transformation dataset>
```

if using the normal structure of the project it can be written as

``` bash
python src/main.py datasets/dataset_md.json
```

Following, a GUI should appear with the pre-rendered results of the starting population. Each fractal has a score to be assigned and then EVAL can be selected in order to start the generation of a new population. After clicking on EVAL, you should see the progress of the creation of the new fractals on the terminal.

## Credits

For the basic rendering algorithm credits goes to https://github.com/rodrigosetti/ifs that showed a basic point rendering type and gave us an initial idea / implentation of the rendering of IFS fractals and some insights on how to scale the points to the image size.
