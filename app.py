###############################################################################
# Author: Fernanda Amaral Melo
# Contact: fernanda.amaral.melo@gmail.com
###############################################################################

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from virtualBg import virtualBackground

# MACROS
width, height = 800, 600    # Initialisation of webcam size
cap = cv2.VideoCapture(0)   # Type of Capture
appState = 0                # App state

# States
# 0:choose virtual bg picture
# 1: take the real bg photo
# 2: replace bg in webcam image


class Application:
    def __init__(self, master=None):
        self.widget = tk.Frame(master)
        self.widget.pack()
        self.choosePicBtn()

    def changeState(self):
        global appState
        appState += 1
        if appState == 1:
            self.selectBtn.destroy()
            self.takePicBtn()
            self.takePicHandler()
        if appState == 2:
            self.webcam.destroy()
            self.takePicBtn.destroy()
            self.vbg = virtualBackground(bg=self.bg, virtualbg=self.virtualbg)
            self.virtualBgView()
            self.replaceBg()

    def choosePicBtn(self):
        self.selectBtn = tk.Button(
            self.widget,
            highlightbackground='#4197B2',
            text="Select a virtual background image",
            command=self.choosePicBtnHandler,
        )
        self.selectBtn.pack()

    def choosePicBtnHandler(self):
        path = filedialog.askopenfilename()
        self.virtualbg = cv2.imread(path)
        self.changeState()

    def takePicBtn(self):
        self.takePicBtn = tk.Button(
            self.widget,
            text='Take the real background photo',
            highlightbackground='#4197B2',
            command=self.changeState)
        self.takePicBtn.pack()
        self.webcam = tk.Label(self.widget)
        self.webcam.pack()

    def takePicHandler(self):
        _, frame = cap.read()
        self.bg = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(self.bg, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.webcam.imgtk = imgtk
        self.webcam.configure(image=imgtk)
        self.webcam.after(10, self.takePicHandler)

    def insertText(self, text):
        txt = tk.Text(self.widget, width=10, height=0)
        txt.insert(tk.INSERT, text)
        txt.configure(state='disabled')
        txt.pack(side=tk.LEFT)

    def virtualBgView(self):
        self.plot = tk.Label(self.widget)
        self.plot.pack()
        self.insertText('Threshold')
        self.threshold_slider = tk.Scale(self.widget, from_=0, to=255, orient='horizontal')
        self.threshold_slider.pack(side=tk.LEFT)
        self.insertText('Opening')
        self.opening_slider = tk.Scale(self.widget, from_=4, to=100, orient='horizontal')
        self.opening_slider.pack(side=tk.LEFT)
        self.insertText('Closing')
        self.closing_slider = tk.Scale(self.widget, from_=4, to=100, orient='horizontal')
        self.closing_slider.pack(side=tk.LEFT)

    def replaceBg(self):
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        new_pic = self.vbg.replaceBg(frame, self.threshold_slider.get(), self.opening_slider.get(), self.closing_slider.get())
        new_pic = cv2.cvtColor(new_pic, cv2.COLOR_BGR2RGBA)
        new_pic = Image.fromarray(new_pic)
        imgtk = ImageTk.PhotoImage(image=new_pic)
        self.plot.imgtk = imgtk
        self.plot.configure(image=imgtk)
        self.plot.after(10, self.replaceBg)


root = tk.Tk()
root.geometry('1000x1000')
Application(root)
root.mainloop()
