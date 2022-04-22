# Generative-Art

I have only tested this on Ubuntu 20.04.

copied from https://github.com/JakobGlock cuz i'm a lazy piece of shit

You can get these scripts without the python module integration by cloning the 0.1.1 tag, go here: https://github.com/JakobGlock/Generative-Art/tree/0.1.1


### Setup

These scripts have been made using Python 3.8.2

Install some dependencies, on Linux this very simple you just run the following command in a terminal window:

`sudo apt install python-cairo libcairo2-dev`

Create a Python virtual environment and activate it:

```
cd /to/the/repo/directory/on/your/computer/Generative-art
python3 -m venv venv
source venv/bin/activate
```

You will also need to install some packages for Python which can be done using the following command:

`pip3 install -r requirements.txt`


### Running Scripts

You can use the generate tool to run the scripts, to get more information run the following command:

`./generate --help`


To generate an artwork:

`./generate artwork new Line_Grid.py`

To generate the same artwork, but 10 of them and in SVG format:

`./generate artwork new Line_Grid.py -n 10 --svg`

This will save 10 files in SVG format into the `Images/Line_Grid` folder, see `./generate --help` for more options and information.


To create a new script/project, run the following command:

`./generate project new my_cool_script.py`

This will create a basic script from a template file to get you started.

#### Things to check

https://www.youtube.com/watch?v=YO-F3pPzVxw 


Credits to : https://github.com/JakobGlock/Generative-Art