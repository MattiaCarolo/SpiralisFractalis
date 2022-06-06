import os
from tkinter import ttk
from tkinter import *


from utils import get_img, get_images_paths
from SpiralisFractalis import *
import components.ga as ga


START_DIR = "./datasets/"
IMAGES_PATH = "./IMGres/"
MAX_ITER = 28


def update_val(text, value: Label):
    value.config(text=str(int(float(text))))


class App(Tk):
    def __init__(self, fractals, width, height, numIteration):
        super().__init__()
        self.generation_number = 1
        self.fractals = fractals
        self.title("Spiralis Fractalis")
        self.geometry("1440x900")
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
        self.start = True
        self.scalas = []
        self.images = []
        self.fill_image_frame()

        self.send_eval_btn = Button(
            self.main_frame,
            background="#40c4ff",
            text="EVAL",
            width=20,
            height=100,
            command=lambda: self.eval(width, height, numIteration),
        )
        self.send_eval_btn.pack(side=BOTTOM, fill=X)

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def open_popup(self):
        top = Toplevel(self)
        top.geometry("450x100")
        top.title("Error")
        Label(
            top,
            text="Please give a score to at least one fractal :(",
            font=("Times 15 bold"),
        ).place(x=50, y=50)

    def fill_image_frame(self):

        if self.start:
            self.image_paths = get_images_paths(START_DIR)
            
            if "./datasets/dataset_md.json" in self.image_paths:
                self.image_paths.remove("./datasets/dataset_md.json")
            if "./datasets/dataset_md.png" in self.image_paths:
                self.image_paths.remove("./datasets/dataset_md.png")
            if "./datasets/dataset_sm.json" in self.image_paths:
                self.image_paths.remove("./datasets/dataset_sm.json")
            if "./datasets/dataset_sm.png" in self.image_paths:
                self.image_paths.remove("./datasets/dataset_sm.png")
            if "./datasets/dataset.json" in self.image_paths:
                self.image_paths.remove("./datasets/dataset.json")
            
            self.start = False
        else: 
            self.image_paths = get_images_paths(IMAGES_PATH)
            # line to avoid opencv opening the dataset //needs to be cleaned
            if "./IMGres/dataset_md.json" in self.image_paths:
                self.image_paths.remove("./IMGres/dataset_md.json")

        self.image_paths.sort(key=lambda x: x, reverse=False)

        for i, pth in enumerate(self.image_paths):
            scala = Scale(self.images_frame, from_=0, to=100, orient=HORIZONTAL)
            img = get_img(pth, shape=(384, 216))
            label = ttk.Label(master=self.images_frame, image=img)
            if i < 5:
                label.grid(row=i, column=0)
                scala.grid(row=i, column=1)
            else:
                label.grid(row=i - 5, column=2, padx=(100, 0), pady=5)
                scala.grid(row=i - 5, column=3)
            self.scalas.append(scala)
            self.images.append(img)

    def eval(self, width, height, numIteration):

        evaluation = self.get_eval_dict()

        if sum([v for v in evaluation.values()]) == 0:
            self.open_popup()
            return

        population = self.getRankedPopulation(evaluation, self.fractals)

        self.delete_images()

        self.fractals = ga.evolve(population)

        # init images
        for i, x in enumerate(self.fractals):
            process_file(x, width, height, i, MAX_ITER, get_name_index(i))

        zipGeneration(
            width, height, numIteration, self.fractals, self.generation_number
        )

        self.generation_number += 1
        self.fill_image_frame()

    def delete_images(self):
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
        for key, rank in evaluation.items():
            index = int(os.path.basename(str(key)).split(".")[0])
            try:
                fractals[index].score = rank
            except IndexError:
                print("Indice che da errore: ", index)
        return fractals
