from tkinter import ttk
from tkinter import *
from utils import get_img, get_images_paths




IMAGES_PATH = ".\FractalsEA_FrontEnd\src\images"


def update_val(text, value: Label):
    value.config(text=str(int(float(text))))


class App(Tk):
    def __init__(self):
        super().__init__()
        

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

        self.send_eval_btn = Button(
            self.main_frame,
            background="#40c4ff",
            text="EVAL",
            width=5,
            height=2,
            command=self.eval,
        )
        self.send_eval_btn.pack(side=BOTTOM, fill=X)

        self.scalas = []
        self.images = []
        self.fill_image_frame()

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def fill_image_frame(self):
        self.image_paths = get_images_paths(IMAGES_PATH)
        for i, pth in enumerate(self.image_paths):

            scala = Scale(self.images_frame, from_=0, to=100, orient=HORIZONTAL)
            scala.grid(row=i, column=1)
            img = get_img(pth, shape=(100, 100))

            label = ttk.Label(master=self.images_frame, image=img)
            label.grid(row=i, column=0)

            self.scalas.append(scala)
            self.images.append(img)

    def eval(self):
        self.get_eval_dict()
        self.nuke_the_childrens()
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
        print(evaluations)
        return evaluations
