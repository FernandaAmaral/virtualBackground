import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from virtualBg import virtualBackground

# MACROS
width, height = 800, 600    # Initialisation of webcam size
cap = cv2.VideoCapture(0)   # Type of Capture
appState = 0


class Application:
    def __init__(self, master=None):
        self.widget1 = tk.Frame(master)
        self.widget1.pack()
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
            self.widget1,
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
            self.widget1,
            text='Take the real background photo',
            highlightbackground='#4197B2',
            command=self.changeState)
        self.takePicBtn.pack()
        self.webcam = tk.Label(self.widget1)
        self.webcam.pack()

    def takePicHandler(self):
        _, frame = cap.read()
        self.bg = cv2.flip(frame, 1)
        self.new_pic = self.bg
        cv2image = cv2.cvtColor(self.bg, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.webcam.imgtk = imgtk
        self.webcam.configure(image=imgtk)
        self.webcam.after(10, self.takePicHandler)

    def virtualBgView(self):
        self.plot = tk.Label(self.widget1)
        self.plot.pack()

    def replaceBg(self):
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        new_pic = self.vbg.replaceBg(frame)
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
