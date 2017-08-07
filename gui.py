#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import Tkinter as tk
from Tkinter import Tk, StringVar, Frame, Label, Text, Entry, Button, Listbox, END
from ttk import Scrollbar
from PIL import ImageTk, Image

import sys
from contextlib import *


class CoreGUI(object):
    def __init__(self):
        self.mw = Tk()
        self.style = MainWindowStyles()
        self.setup(self.mw)

    def setup(self, parent):
        parent.title("Debug Client by 2017 ZEBEX, Inc.")
        resize_and_center(parent, 1280, 600)

        # Variables
        self.modelname = StringVar(parent, "Z5212")
        self.message = StringVar(parent, "--disconnect--")

        # Top Frame (name entry box, buttons, conn status)
        self.conn_frame = Frame(parent, **self.style.Frame)
        self.lower_frame = Frame(parent, **self.style.Frame)
        self.conn_frame.pack(side="top", fill="x")
        self.lower_frame.pack(side="top", fill="both", expand=1)

        self.image_frame = Frame(self.lower_frame, **self.style.Frame)
        self.command_frame = Frame(self.lower_frame, **self.style.Frame)
        self.command_frame.pack(side="right", fill="y")
        self.image_frame.pack(side="right", fill="both", expand=1)

        # The message entry
        self.message_frame = Frame(self.image_frame, **self.style.Frame)
        self.display_frame = Frame(self.image_frame, **self.style.Frame)
        self.message_frame.pack(side="top", fill="x")
        self.display_frame.pack(side="top", fill="both", expand=1)

        ###
        # Top Frame Widgets
        ###

        self.name_label = Label(self.conn_frame,
                                text="Project :",
                                **self.style.Label
                                )
        self.name_entry = Entry(self.conn_frame,
                                textvariable=self.modelname,
                                width=20,
                                **self.style.DarkEntry
                                )
        self.enter_exit_button = Button(self.conn_frame,
                                        text="Quit",
                                        **self.style.Button
                                        )
        self.status_label = Label(self.conn_frame,
                                  # text="Connected",
                                  **self.style.ConnectedLabel
                                  )
        self.name_label.pack(side="left", padx=5, pady=5)
        self.name_entry.pack(side="left", pady=5)
        self.enter_exit_button.pack(side="left", padx=5, pady=5)
        self.status_label.pack(side="left")

        ###
        # Message Frame Widgets
        ###

        self.message_entry = Entry(self.message_frame,
                                   textvariable=self.message,
                                   state="disabled",
                                   **self.style.Entry
                                   )
        self.message_entry.pack(
            side="top",
            fill="x",
            padx=10,
            pady=10,
            expand=1,
        )

        ###
        # Who Frame Widgets
        ###

        self.right_label = Label(self.command_frame,
                                 text="Command:",
                                 anchor="w",
                                 **self.style.Label
                                 )
        self.right_label.pack(side="top", fill="x")

        """self.who_list = Scrolled(self.right_frame, Listbox,
            attributes=self.style.Listbox,
            scrollbar=self.style.Scrollbar,
        )
        self.who_list.pack(side="top", fill="both", expand=1)

        for i in range(200):
            self.who_list.widget.insert(END, "Anonymous{}".format(i))
        """
        ###
        # Display Frame Widgets
        ###

        self.display_frame.configure(background='#666666')

        # Create a canvas
        canvas = tk.Canvas(self.display_frame, width=1280, height=720)
        canvas.pack()
        # Load the image file
        im = Image.open('Capture.jpg')
        # Put the image into a canvas compatible class, and stick in an
        # arbitrary variable to the garbage collector doesn't destroy it
        canvas.image = ImageTk.PhotoImage(im)
        # Add the image to the canvas, and set the anchor to the top left / north west corner
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')

    def start(self):
        self.mw.mainloop()


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
        bg="#FFFF00",
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
        wrap=tk.WORD,
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
    app = CoreGUI()
    app.start()
