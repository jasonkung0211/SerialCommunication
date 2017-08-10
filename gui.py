#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# import Tkinter as tk
from Tkinter import  Tk, StringVar, Frame, Label, Entry, Button, Canvas, WORD, IntVar, RIGHT, LEFT
from ttk import Scrollbar, Radiobutton
from PIL import ImageTk, Image
from tkinter import messagebox

from SerialCommunication import *


class commGUI(object):
    def callback(self):
        sendComm(self.name + str(self.value.get()), serConnector)

    def __init__(self, parent, values, name):
        # state = "disabled"
        self.style = MainWindowStyles()
        self.value = IntVar(0)
        self.value.set(values)
        self.name = name
        _frame = Frame(parent, **self.style.Frame)
        Button(_frame, text=name, anchor="w", command=self.callback, **self.style.SettingButton).pack(side=LEFT, fill="x")
        Entry(_frame, width=5, textvariable=str(self.value), **self.style.Entry).pack(side=RIGHT, fill="x")
        _frame.pack(side="left", padx=5, pady=5)


class CoreGUI(object):
    def __init__(self):
        self.mw = Tk()
        self.style = MainWindowStyles()
        self.quality = IntVar()
        self.setup(self.mw)

    def setup(self, parent):
        parent.title("JDebug Client by 2017 ZEBEX, Inc.")
        resize_and_center(parent, 1280, 720)

        # Variables
        self.modelname = StringVar(parent, "Z5212")

        # Top Frame (name entry box, buttons, conn status)
        self.conn_frame = Frame(parent, **self.style.Frame)
        self.conn_frame.pack(side="top", fill="x")

        self.lower_frame = Frame(parent, **self.style.Frame)
        self.lower_frame.pack(side="top", fill="both", expand=1)

        # The message entry
        self.display_frame = Frame(self.lower_frame, **self.style.Frame)
        self.display_frame.pack(side="top", fill="both", expand=1, padx=5, pady=5)

        ###
        # Top Frame Widgets
        ###

        self.name_label = Label(self.conn_frame,
                                text="Project :",
                                **self.style.Label
                                )
        self.name_entry = Entry(self.conn_frame,
                                textvariable=self.modelname,
                                width=8,
                                **self.style.DarkEntry
                                )
        self.enter_exit_button = Button(self.conn_frame,
                                        text="Quit",
                                        command=self.quit,
                                        **self.style.Button
                                        )
        self.name_label.pack(side="left", padx=5, pady=5)
        self.name_entry.pack(side="left", pady=5)
        self.enter_exit_button.pack(side="left", padx=5, pady=5)

        ###
        # Image Frame Widgets get image, set quality
        ###

        self.img_frame = Frame(self.conn_frame, **self.style.Frame)
        image_q_label = Label(self.img_frame, text='Quality', anchor="w", **self.style.Label)
        image_q_label.pack(side=LEFT, fill="x")
        self.quality.set(85)
        Radiobutton(self.img_frame, text='L', variable=self.quality, value=35, command=self.selected_quality).pack(side=RIGHT, anchor="w")
        Radiobutton(self.img_frame, text='M', variable=self.quality, value=85, command=self.selected_quality).pack(side=RIGHT, anchor="w")
        Radiobutton(self.img_frame, text='H', variable=self.quality, value=93, command=self.selected_quality).pack(side=RIGHT, anchor="w")

        self.img_frame.pack(side="left", padx=5, pady=5)

        commGUI(self.conn_frame, c.Gain, "Gain")
        commGUI(self.conn_frame, c.Shutter, "Shutter")
        commGUI(self.conn_frame, c.light, "light")

        Button(self.conn_frame, text='GET Image', command=self.getimg, **self.style.SettingButton).pack(side="left",
                                                                                                        padx=5, pady=5)

        ###
        # Display Frame Widgets
        ###
        self.display_frame.configure(background='#666666')
        # Create a canvas
        self.canvas = Canvas(self.display_frame, width=1280, height=720, bg="#666666")
        self.loadImage('Capture.jpg')

    def quit(self):
        sendComm("quit", serConnector)
        app.quit()
        app.destroy()

    def getimg(self):
        self.canvas.delete("all")
        getImage("image" + str(self.quality.get()), serConnector, c.isRs232)
        self.loadImage('Capture.jpg')

    def loadImage(self, filename):
        self.canvas.pack()
        # Load the image file
        try:
            im = Image.open(filename)
        except IOError:
            return
        # Put the image into a canvas compatible class, and stick in an
        # arbitrary variable to the garbage collector doesn't destroy it
        self.canvas.image = ImageTk.PhotoImage(im)
        # Add the image to the canvas, and set the anchor to the top left / north west corner
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def start(self):
        self.mw.mainloop()

    def selected_quality(self):
        pass
        # if '' != self.quality.get():
        #    messagebox.showinfo('Change Image Quality', self.quality.get())


class MainWindowStyles(object):
    """Simple Python class to hold style-related configurations for widgets."""
    Frame = dict(
        bg="#666666",
    )

    BaseLabel = dict(
        font=("Helvetica", 14, "bold italic"),
    )
    Label = dict(
        bg="#666666",
        fg="#EEFFCC",
        **BaseLabel
    )
    ConnectedLabel = dict(
        bg="#666666",
        fg="#00FF00",
        **BaseLabel
    )

    BaseFormCtrl = dict(
        highlightthickness=0,  # Removes stupid border around the widget
    )

    BaseEntry = dict(
        insertwidth=1,
        selectborderwidth=0,
        selectbackground="#0099FF",
        font=("Helvetica", 14, "bold"),
        **BaseFormCtrl
    )
    Entry = dict(
        bg="#FFFFFF",
        fg="#000000",
        disabledbackground="#000000",
        disabledforeground="#666666",
        insertbackground="#000000",
        **BaseEntry
    )
    DarkEntry = dict(
        bg="#000000",
        fg="#CCCCCC",
        insertbackground="#FCFCFC",  # Text insertion blinking cursor
        **BaseEntry
    )

    Listbox = dict(
        bg="#666666",
        fg="#CCCCCC",
        **BaseFormCtrl
    )

    Dialogue = dict(
        bg="#000000",
        fg="#CCCCCC",
        # disabledbackground="#000000",
        # disabledforeground="#CCCCCC",
        wrap=WORD,
        state="disabled",
        **BaseEntry
    )

    Button = dict(
        bg="#000000",
        fg="#CCCCCC",
        activebackground="#000000",
        activeforeground="#0099FF",
        **BaseFormCtrl
    )

    SettingButton = dict(
        bg="#666666",
        fg="#EEFFCC",
        font=("Helvetica", 11, "bold italic"),
        **BaseFormCtrl
    )

    # If using the Tkinter scrollbar, uncommon these. If using the ttk
    # scrollbar, use ttk's theming system instead.
    Scrollbar = dict(
        # relief="flat",
        # troughcolor="#000000",
        # bg="#606060",
        # activebackground="#999999",
        # borderwidth=1,
        # width=12,
        # highlightthickness=0,
    )


class Scrolled(object):
    """My own implementation for adding a scrollbar to a widget. Similar in
    principal to Python's ScrolledText module, but it works on other widgets too
    (this script uses it on Listbox too). So it's more like the Perl/Tk module
    Tk::Scrolled in that it can wrap any widget, in theory."""

    def __init__(self, master, widget_class, attributes=None, scrollbar=None):
        """
        master is the parent widget
        widget_class is the class, like Text or Listbox
        attributes are attributes for the widget
        scrollbar are attributes for the scrollbar
        """
        if attributes is None:
            attributes = []
        if scrollbar is None:
            scrollbar = []

        self.master = master

        # Parent frame to hold the widget + scrollbar
        self.frame = Frame(master)

        # The scrollbar
        self.scrollbar = Scrollbar(self.frame, **scrollbar)

        # The widget itself
        self.widget = widget_class(self.frame,
                                   yscrollcommand=self.scrollbar.set,
                                   **attributes
                                   )
        self.scrollbar.configure(command=self.widget.yview)

        self.scrollbar.pack(side="right", fill="y")
        self.widget.pack(side="right", fill="both", expand=1)

    def widget(self):
        """Get at the inner widget."""
        return self.widget

    def scrollbar(self):
        """Get at the scrollbar widget."""
        return self.scrollbar

    def pack(self, **kwargs):
        """Wrapper so that pack() works as you'd expect."""
        self.frame.pack(**kwargs)


def resize_and_center(win, width, height):
    """Resize a window and center it on the screen."""
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    geometry = "{}x{}+{}+{}".format(
        width,
        height,
        screen_w / 2 - width / 2,
        screen_h / 2 - height / 2,
    )
    win.geometry(geometry)


if __name__ == "__main__":
    ports = serial_ports()
    s_port = serial_devices_name(ports)
    s_baud = serial_baud(s_port)

    if s_baud == -1:
        print s_port
        exit(0)

    c = Config('')
    c.baud = s_baud
    c.port = s_port
    c.isRs232 = int(c.baud) - 115200 <= 0
    c.dump()
    serConnector = connect(c)

    Has_response = handshake(serConnector)

    if Has_response:
        setDefault(c, serConnector)
    else:
        exit(1)

    app = CoreGUI()
    app.start()
