import tkinter
from tkinter import *
import tkinter as tk
from typing import Sized
from PIL import ImageTk, Image
import cv2
import numpy as np
import os
from tqdm import tqdm
import random

global_frames = []
vids_dir = os.getcwd() + "/"
video_nums = 10


def cv2image2pil(cv_image):
    # Rearrang the color channel
    b, g, r, a = cv2.split(cv_image)
    img = cv2.merge((r, g, b, a))

    # Convert the Image object into a TkPhoto object
    im = Image.fromarray(img)
    # imgtk = ImageTk.PhotoImage(image=im)

    return im


def read_video(path):

    cap = cv2.VideoCapture(path)
    if cap.isOpened() == False:
        print("Error opening video stream or file")

    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frames.append(frame)
        # Break the loop
        else:
            break

    cap.release()
    return frames


def remove_bg(frame):
    h = frame.shape[0]
    w = frame.shape[1]
    image = frame[0 : int(h / 2), :, :]
    mask = frame[int(h / 2) :, :, :]
    mask = cv2.split(mask)[0]
    image = cv2.merge((image, mask))
    return image


def videos_frames(path):
    videos = next(
        os.walk(os.path.join(os.getcwd(), path)),
        (None, None, []),
    )[2]
    videos = random.sample(videos, video_nums)
    for video_filename in tqdm(videos):
        video_filename = vids_dir + video_filename
        global global_frames
        if video_filename[-4:] != ".mp4":
            continue
        for frame in read_video(video_filename):
            global_frames.append(
                ImageTk.PhotoImage(image=cv2image2pil(remove_bg(frame)))
            )


class Win(tkinter.Tk):
    def __init__(self, master=None):
        tkinter.Tk.__init__(self, master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self._offsetx = 0
        self._offsety = 0
        self.bind("<Button-1>", self.clickwin)
        self.bind("<B1-Motion>", self.dragwin)
        self.bind("<space>w", self.closewin)
        # self.bind("<space>e", self.minimize)
        self.delay = 20
        videos_frames(vids_dir)

        self.frame_cnt = 0

        background_image = global_frames[0]

        self.background_label = Label(self, image=background_image, bg="black")
        self.lift()
        self.wm_attributes("-transparentcolor", "black")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.image = background_image
        self.background_label.after(self.delay, self.update)

        w = background_image.width()
        h = background_image.height()
        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def dragwin(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry("+{x}+{y}".format(x=x, y=y))

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def closewin(self, event):
        self.destroy()

    def update(self):
        img2 = global_frames[self.frame_cnt]
        self.background_label.configure(image=img2)
        self.background_label.image = img2
        self.frame_cnt += 1
        if len(global_frames) == self.frame_cnt:
            self.frame_cnt = 0
        self.background_label.after(self.delay, self.update)

    # def minimize(self, event):
    #     if self.state() == "iconic":
    #         self.attributes("-topmost", True)
    #     else:
    #         self.attributes("-topmost", False)
    #         self.wm_state("iconic")


win = Win()
win.mainloop()
