#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import Tkinter as tk
from Tkinter import Tk, StringVar, Frame, Label, Text, Entry, Button, Listbox, END
from ttk import Scrollbar

import sys
from contextlib import *


class CoreGUI(object):
    def __init__(self):
        # Styles
        self.mw = Tk()
        self.style = MainWindowStyles()
        self.setup(self.mw)

    def setup(self, parent):
        parent.title("Debug Client @ 2017 ZEBEX, Inc.")
        resize_and_center(parent, 1024, 580)

        # Variables
        self.modelname = StringVar(parent, "Z5212")
        self.message = StringVar(parent, "--disconnect--")

        # Top Frame (name entry box, buttons, conn status)
        self.login_frame = Frame(parent, **self.style.Frame)
        self.lower_frame = Frame(parent, **self.style.Frame)
        self.login_frame.pack(side="top", fill="x")
        self.lower_frame.pack(side="top", fill="both", expand=1)

        # The lower left (message entry, chat history) and lower right
        # (who lists)
        self.left_frame = Frame(self.lower_frame, **self.style.Frame)
        self.right_frame = Frame(self.lower_frame, **self.style.Frame)
        self.right_frame.pack(side="right", fill="y")
        self.left_frame.pack(side="right", fill="both", expand=1)

        # The message entry & chat history frames
        self.message_frame = Frame(self.left_frame, **self.style.Frame)
        self.dialogue_frame = Frame(self.left_frame, **self.style.Frame)
        self.message_frame.pack(side="top", fill="x")
        self.dialogue_frame.pack(side="top", fill="both", expand=1)

        ###
        # Top Frame Widgets
        ###

        self.name_label = Label(self.login_frame,
                                text="Project :",
                                **self.style.Label
                                )
        self.name_entry = Entry(self.login_frame,
                                textvariable=self.modelname,
                                width=20,
                                **self.style.DarkEntry
                                )
        self.enter_exit_button = Button(self.login_frame,
                                        text="Enter chat",
                                        **self.style.Button
                                        )
        self.status_label = Label(self.login_frame,
                                  text="Connected to CyanChat",
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

        self.right_label = Label(self.right_frame,
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
        # Dialogue Frame Widgets
        ###

        self.dialogue_text = Scrolled(self.dialogue_frame, Text,
                                      attributes=self.style.Dialogue,
                                      scrollbar=self.style.Scrollbar,
                                      )
        self.chat_styles(self.dialogue_text.widget)
        self.dialogue_text.pack(side="top", fill="both", padx=10, pady=0, expand=1)

        # Dummy junk
        messages = [
            [["[Kirsle]", "user"], [" Hello room!"]],
            [["\\\\\\\\\\", "server"], ["[Kirsle]", "user"], [" <links in from comcast.net Age>"], ["/////", "server"]],
            [["[ChatServer] ", "server"], ["Welcome to the Cyan Chat room."]],
            [["[ChatServer] ", "server"], ["There are only a few rules:"]],
            [["[ChatServer] ", "server"], ["   Be respectful and sensitive to others"]],
            [["[ChatServer] ", "server"], ["   And HAVE FUN!"]],
            [["[ChatServer] ", "server"], [""]],
            [["[ChatServer] ", "server"], ["Termination of use can happen without warning!"]],
            [["[ChatServer] ", "server"], [""]],
            [["[ChatServer] ", "server"], ["Server commands now available, type !\\? at the beginning of a line."]],
            [["[ChatServer] ", "server"], ["CyanChat Server version 2.12d"]],
        ]
        for i in range(80):
            messages.append([["[ChatClient]", "client"], [" Connecting..."]])
        messages.reverse()
        for line in messages:
            self.insert_readonly(self.dialogue_text, 0.0, "\n")
            line.reverse()
            for part in line:
                self.insert_readonly(self.dialogue_text, 0.0, *part)
                # self.insert_readonly(self.dialogue_text, END, "[Admin]", "admin")

    def chat_styles(self, widget):
        """Configure chat text styles."""
        # User colors
        widget.tag_configure("user", foreground="#FFFFFF")
        widget.tag_configure("guest", foreground="#FF9900")
        widget.tag_configure("admin", foreground="#00FFFF")
        widget.tag_configure("server", foreground="#00FF00")
        widget.tag_configure("client", foreground="#FF0000")

    def insert_readonly(self, widget, *args):
        """Insert text into a readonly (disabled) widget."""
        widget.widget.configure(state="normal")
        widget.widget.insert(*args)
        widget.widget.configure(state="disabled")

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
