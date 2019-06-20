from tkinter import filedialog
from tkinter import *
import PIL
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import data_converter

colours = [(255,0,125), (252,252,0), (255,217,131), (255,254,239)]

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.mouse_x = 0
        self.mouse_y = 0
        self.x_off = 0
        self.y_off = 0

        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("labeltest")

        #self.grid(row=0, column=0, rowspan=2, columnspan=3)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Open", command=self.open_dialogue)
        file.add_command(label="Save", command=self.save_dialogue)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)
        
        self.label_list = Listbox(self.master, width=40)
        self.label_list.grid(row=0, column=2, sticky=N+E+S)
        
        file_list = Listbox(self.master, width=40)
        file_list.insert(END, "This is a file")
        file_list.insert(END, "This is another file")
        file_list.grid(row=1, column=2, sticky=S+E+N)
        
        class_list = Listbox(self.master, width=40)
        class_list.insert(END, "This is a class")
        class_list.grid(row=1, column=0, sticky=S+W+N)
        
        self.image_view = Canvas(root)

        self.image_view.bind("<Configure>", self.resize_image)
        self.image_view.bind("<Motion>", self.mouse_move)

    def mouse_move(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        self.draw_image()

    def redraw_shapes(self, img):
        draw = ImageDraw.Draw(self.resized_image)

        for idx, bb in enumerate(self.detection_data["detection_boxes"]):
            if self.detection_data["detection_scores"][idx] > 0.5:
                draw.rectangle((bb[1]*self.resized_image.width,bb[0]*self.resized_image.height,bb[3]*self.resized_image.width,bb[2]*self.resized_image.height), outline=colours[int(self.detection_data["detection_classes"][idx])], width=2)

        #draw.rectangle((self.mouse_x - self.x_off, self.mouse_y - self.y_off, self.mouse_x+10-self.x_off, self.mouse_y+10-self.y_off), fill=256)

    def draw_image(self):
        self.resized_image = self.original_image.copy().resize((self.new_w, self.new_h))

        self.redraw_shapes(self.resized_image)

        self.img = ImageTk.PhotoImage(self.resized_image)
        wat = self.image_view.create_image(self.x_off, self.y_off, image=self.img, anchor=NW)
        self.image_view.image = self.img

    def resize_image(self, event):
        w = 1920
        h = 1080
        aspect_ratio = w/h
        i_ratio = h/w

        if event.width/event.height < aspect_ratio:
            #Constrain height
            self.new_w = event.width
            self.new_h = int(event.width * i_ratio)
            self.y_off = int((event.height - self.new_h) / 2)
        else:
            #Constrain width
            self.new_w = int(event.height * aspect_ratio)
            self.new_h = event.height
            self.x_off = int((event.width - self.new_w) / 2)

        self.draw_image()
        
    def open_dialogue(self):
        self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("numpy files","*.npy"),("all files","*.*")))
        self.detection_data = np.load(self.filename).item()

        self.original_image = Image.open(self.filename.split(".")[0] + ".jpg")
        self.img = ImageTk.PhotoImage(self.original_image)
        
        wat = self.image_view.create_image(0,0,image=self.img, anchor=NW)
        self.image_view.image = self.img
        self.image_view.grid(row=0, column=1, rowspan=2, sticky=S+W+N+E)

        for idx, bb in enumerate(self.detection_data["detection_boxes"]):
            if self.detection_data["detection_scores"][idx] > 0.5:
                self.label_list.insert(END, self.detection_data["detection_classes"][idx])

    def save_dialogue(self):
        dc = data_converter.DataConverter()
        dc.load_npy(self.filename)
        dc.save_pascalvoc(self.filename.split(".")[0] + ".xml")

    def client_exit(self):
        exit()

root = Tk()
root.geometry("1280x720")

root.columnconfigure(0)
root.columnconfigure(1, weight=1)
root.columnconfigure(2)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

test = Window(root)
root.minsize(640, 360)
root.mainloop()
