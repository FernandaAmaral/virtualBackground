"""Virtual Background Interface

This script uses the tkinter module to create a GUI for
1: Selecting a desired virtual background image
2: Taking a picture of the real background using webcam
3. Controlling the background replacement algorith paramenters
(binary image threshold and opening/closing kernel size)

This script requires that `opencv and matplotlib` be installed within
the Python environment you are running this script in.
"""

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
        self._choose_pic_btn()

    def _change_state(self):
        """Manages the application state"""
        global appState
        appState += 1
        if appState == 1:  # Take the real bg picture
            self.selectBtn.destroy()
            self._take_pic_btn()
            self._take_pic_handler()
        if appState == 2:  # Replaces the webcam image bg by the virtual one
            self.webcam.destroy()
            self.takePicBtn.destroy()
            self.vbg = virtualBackground(bg=self.bg, virtualbg=self.virtualbg)
            self._virtual_bg_view()
            self._replace_bg()

    def _choose_pic_btn(self):
        """Displays the GUI button for choosing the virtual background file"""
        self.selectBtn = tk.Button(
            self.widget,
            highlightbackground='#4197B2',
            text="Select a virtual background image",
            command=self._choose_pic_handler,
        )
        self.selectBtn.pack()

    def _choose_pic_handler(self):
        """Button handler for the virtual background choosen file"""
        path = filedialog.askopenfilename()
        self.virtualbg = cv2.imread(path)
        self._change_state()

    def _take_pic_btn(self):
        """Displays the GUI button for taking the real background photo"""
        self.takePicBtn = tk.Button(
            self.widget,
            text='Take the real background photo',
            highlightbackground='#4197B2',
            command=self._change_state)
        self.takePicBtn.pack()
        self.webcam = tk.Label(self.widget)
        self.webcam.pack()

    def _take_pic_handler(self):
        """Button handler for the real background taken photo"""
        _, frame = cap.read()
        self.bg = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(self.bg, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.webcam.imgtk = imgtk
        self.webcam.configure(image=imgtk)
        self.webcam.after(10, self._take_pic_handler)

    def _insert_text(self, text):
        """Creates a text widget on the GUI

        Parameters
        ----------
        text : string
            The text to be displayed
        """
        txt = tk.Text(self.widget, width=10, height=0)
        txt.insert(tk.INSERT, text)
        txt.configure(state='disabled')
        txt.pack(side=tk.LEFT)

    def _create_slider(self, min, max):
        """Creates a slider widget on the GUI

        Parameters
        ----------
        min : int
            The slider minimum value
        max : int
            The slider maximum value
        """
        return tk.Scale(self.widget, from_=min, to=max, orient='horizontal')

    def _virtual_bg_view(self):
        """Frame containing the webcam image with the virtual background
        replacement and 3 sliders for controlling binary image threshold
        and opening/closing kernel size
        """
        self.plot = tk.Label(self.widget)
        self.plot.pack()
        self._insert_text('Threshold')
        self.threshold_slider = self._create_slider(0, 255)
        self.threshold_slider.pack(side=tk.LEFT)
        self._insert_text('Opening')
        self.opening_slider = self._create_slider(4, 100)
        self.opening_slider.pack(side=tk.LEFT)
        self._insert_text('Closing')
        self.closing_slider = self._create_slider(4, 100)
        self.closing_slider.pack(side=tk.LEFT)

    def _replace_bg(self):
        """Frame containing the webcam image with the virtual background
        replacement and 3 sliders for controlling binary image threshold
        and opening/closing kernel size
        """
        # Takes the cwebcam frame
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Replace background
        new_pic = self.vbg.replace_bg(
            frame,
            self.threshold_slider.get(),
            self.opening_slider.get(),
            self.closing_slider.get())

        # Converts the image to the tkinter required format
        new_pic = Image.fromarray(new_pic)
        imgtk = ImageTk.PhotoImage(image=new_pic)

        # Plot replaced bg image
        self.plot.imgtk = imgtk
        self.plot.configure(image=imgtk)

        # Update camera image
        self.plot.after(10, self._replace_bg)


root = tk.Tk()
root.geometry('1000x1000')
Application(root)
root.mainloop()
