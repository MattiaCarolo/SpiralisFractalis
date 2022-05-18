from ast import Try
import os
from tkinter import ttk
from tkinter import *
from utils import get_img, get_images_paths
from SpiralisFractalis import *
import components.ga as ga
from components.ga import Fractal


IMAGES_PATH = "./IMGres/"


def update_val(text, value: Label):
    value.config(text=str(int(float(text))))

class App(Tk):
    def __init__(self, fractals, width, height, numIteration):
        super().__init__()
        self.generation_number = 1
        self.fractals = fractals
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self.main_frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scroll_bar = ttk.Scrollbar(
            self.main_frame, orient=VERTICAL, command=self.canvas.yview
        )
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind(
            "<Configure>",
            lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.images_frame = Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.images_frame, anchor="nw")
        
        self.image_paths = IMAGES_PATH

        self.scalas = []
        self.images = []
        self.fill_image_frame()

        self.send_eval_btn = Button(
            self.main_frame,
            background="#40c4ff",
            text="EVAL",
            width=5,
            height=2,
            command=lambda : self.eval(width, height, numIteration),
        )
        self.send_eval_btn.pack(side=BOTTOM, fill=X)


    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def fill_image_frame(self):
        self.image_paths = get_images_paths(IMAGES_PATH)

        #line to avoid opencv opening the dataset //needs to be cleaned
        if './IMGres/dataset_md.json' in self.image_paths: self.image_paths.remove('./IMGres/dataset_md.json')

        for i, pth in enumerate(self.image_paths[:-1]):

            scala = Scale(self.images_frame, from_=1, to=100, orient=HORIZONTAL)
            scala.grid(row=i, column=1)
            img = get_img(pth, shape=(100, 100))

            label = ttk.Label(master=self.images_frame, image=img)
            label.grid(row=i, column=0)

            self.scalas.append(scala)
            self.images.append(img)

    def eval(self, width, height, numIteration):

        evaluation = self.get_eval_dict()
        population = self.getRankedPopulation(evaluation, self.fractals)

        #TODO: zip images
        self.nuke_the_childrens()

        self.fractals = ga.evolve(population)   

        # init images
        for i, x in enumerate(self.fractals):
            process_file(x, width, height, numIteration, get_name_index(i))

        zipGeneration(width,height,numIteration,self.fractals, self.generation_number)

        self.generation_number += 1
        self.fill_image_frame()
        
    
    def nuke_the_childrens(self):
        for child in self.images_frame.winfo_children():
            child.destroy()
        self.images.clear()
        self.scalas.clear()
        self.image_paths.clear()

    def get_eval_dict(self):
        evaluations = {}
        for i in range(len(self.images)):
            evaluations[self.image_paths[i]] = self.scalas[i].get()
        return evaluations

    def getRankedPopulation(self, evaluation, fractals):
        for key,rank in evaluation.items():
            index = int(os.path.basename(str(key)).split('.')[0])
            try:
                fractals[index].setScore(rank)
            except IndexError: 
                print("Indice che da errore: ", index)
        return fractals