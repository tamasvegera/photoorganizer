import threading
import tkinter as tk
from tkinter import *
from PIL import Image
import os, time, glob
import shutil
buffer_size = 3
from tkinter import filedialog

class Gui:
    def __init__(self, categories, base_path="./"):
        self.categories = categories

        self.root = tk.Tk()
        self.user_data_frame = Frame(self.root)

        if os.path.exists("./defdir.txt"):
            currdir = open("./defdir.txt", "r").read()
        else:
            currdir = os.getcwd()
        self.base_path = filedialog.askdirectory(parent=self.root, initialdir=currdir, title='Please select a directory') + '/'
        open("./defdir.txt", "w").write(self.base_path)

        print(self.base_path)
        self.root.grid_rowconfigure(1, weight=1)

        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        key_cnt = 0

        handlers = [self.handler_1, self.handler_2, self.handler_3, self.handler_4, self.handler_5, self.handler_6, self.handler_7, self.handler_8, self.handler_9]

        label_txt = ""

        for category in categories:
            self.root.bind(keys[key_cnt], handlers[key_cnt])

            label_txt += keys[key_cnt] + " = " + category + '\n'

            if not os.path.exists(self.base_path + category):
                os.makedirs(self.base_path + category)

            jpg_path = self.base_path + category + "/jpg"
            if not os.path.exists(jpg_path):
                os.makedirs(jpg_path)

            raw_path = self.base_path + category + "/raw"
            if not os.path.exists(raw_path):
                os.makedirs(raw_path)

            key_cnt += 1

        self.root.bind('r', self.rotate)

        temp_label = Label(self.root, text=label_txt)
        temp_label.config(font=("Arial", 12))
        temp_label.grid(row=1, column=1, padx=30)

        self.img_label = Label(self.root)
        self.img_label.grid(row=1, column=0)
        self.root.columnconfigure(0, minsize=700)

        self.current_filename = ""
        self.buffer_file_cnt = 0
        self.next_file_cnt = 0
        self.file_list = []
        self.init_filelist()

        self.image_buffer = []
        self.image_buffer_update()

        self.next_image()

    def init_filelist(self):
        list = glob.glob(self.base_path + "*.JPG")        # init file list in directory
        for file in list:
            self.file_list.append(file.split('\\')[-1])

    def rotate(self, event):
        self.update_img(self.img, rotate=True)

    def image_buffer_update(self):
        while len(self.image_buffer) < buffer_size:
            if len(self.file_list) == self.buffer_file_cnt:
                return

            path = self.base_path + self.file_list[self.buffer_file_cnt]
            self.buffer_file_cnt += 1
            self.image_buffer.append(Image.open(path))
            self.image_buffer[-1] = self.image_buffer[-1].resize((1200, 800), Image.ANTIALIAS)

    def get_image_from_buffer(self):
        while len(self.image_buffer) == 0:
            time.sleep(0.01)

        img = self.image_buffer[0]
        del self.image_buffer[0]
        return img

    def update_img(self, img, rotate=False):
        self.img_label.destroy()

        self.img = img
        if rotate:
            self.img = self.img.rotate(90, expand=True)

        self.img.save(r'./test.png')

        self.photoimg = PhotoImage(file=r"./test.png")
        self.img_label = Label(self.root, image=self.photoimg)
        self.img_label.grid(row=0, column=0, rowspan=5)

        threading.Thread(target=self.image_buffer_update).start()

    def copy(self, filename, category):
        path = self.base_path + filename.split('.')[0]
        for file in glob.glob(path + ".*"):
            if file.split('.')[-1] == "JPG":
                shutil.move(file, self.base_path + category + "/jpg/" + file.split('\\')[-1])
            else:
                shutil.move(file, self.base_path + category + "/raw/" + file.split('\\')[-1])

    def next_image(self):
        if len(self.file_list) == self.next_file_cnt:
            exit()

        # bufferből kivenni imaget
        self.update_img(self.get_image_from_buffer())

        self.current_filename = self.file_list[self.next_file_cnt]
        self.next_file_cnt += 1

    def handler_1(self, event):
        self.copy(self.current_filename, self.categories[0])
        self.next_image()

    def handler_2(self, event):
        self.copy(self.current_filename, self.categories[1])
        self.next_image()

    def handler_3(self, event):
        self.copy(self.current_filename, self.categories[2])
        self.next_image()

    def handler_4(self, event):
        self.copy(self.current_filename, self.categories[3])
        self.next_image()

    def handler_5(self, event):
        self.copy(self.current_filename, self.categories[4])
        self.next_image()

    def handler_6(self, event):
        self.copy(self.current_filename, self.categories[5])
        self.next_image()

    def handler_7(self, event):
        self.copy(self.current_filename, self.categories[6])
        self.next_image()

    def handler_8(self, event):
        self.copy(self.current_filename, self.categories[7])
        self.next_image()

    def handler_9(self, event):
        self.copy(self.current_filename, self.categories[8])
        self.next_image()


gui = Gui(categories=("instant_trash", "nyeh", "okay", "fuckyeah", "priv"), base_path="d:/test/") #base_path="d:/Photography/2021.10.14. PPK karibuli/")

gui.root.mainloop()