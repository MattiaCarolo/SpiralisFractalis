import cv2 as cv
import os
from PIL import ImageTk, Image

def get_img(path, shape):
    img = cv.imread(path)
    img = cv.resize(img, dsize=shape, interpolation=cv.INTER_LINEAR)
    (b, g, r) = cv.split(img)
    return ImageTk.PhotoImage(Image.fromarray(cv.merge((r,g,b))))

def get_images_paths(imgs_path):
    return [os.path.join(imgs_path, im) for im in os.listdir(imgs_path)]    