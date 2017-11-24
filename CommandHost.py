#!/usr/bin/env python

"""My test script for Python/Tk experimentation."""

import Tkinter as tk
from Tkinter import Tk, StringVar, Frame, Label, Text, Entry, Button, Listbox, END
from ttk import Scrollbar
from SerialCommunication import *
from PIL import ImageTk, Image

class CMDHost(object):
    def __init__(self):
        # Styles
        self.style = MainWindowStyles()
        self.mw = Tk()
        self.setup()

    def setup(self):
        self.mw.title("Python Z-5212 Command Host " + c.port + ", " + c.baud)
        resize_and_center(self.mw, 800, 600)

        # Variables
        self.cmd_message = StringVar(self.mw, "--empty--")

        # Top Frame (name entry box, buttons, conn status)
        self.login_frame = Frame(self.mw, **self.style.Frame)
        self.lower_frame = Frame(self.mw, **self.style.Frame)
        self.login_frame.pack(side="top", fill="x")
        self.lower_frame.pack(side="top", fill="both", expand=1)

        # The lower left (message entry, chat history) and lower right
        self.left_frame = Frame(self.lower_frame, **self.style.Frame)
        self.right_frame = Frame(self.lower_frame, **self.style.Frame)
        self.right_frame.pack(side="right", fill="y")
        self.left_frame.pack(side="right", fill="both", expand=1)

        # The cmd entry & history frames
        self.message_frame = Frame(self.login_frame, **self.style.Frame)
        self.dialogue_frame = Frame(self.left_frame, **self.style.Frame)
        self.message_frame.pack(side="top", fill="x")
        self.dialogue_frame.pack(side="top", fill="both", expand=1)


        ###
        # Top Frame Widgets
        ###
        self.enter_Connecte_button = Button(self.login_frame,
                                            text="Connect",
                                            command=self.conn,
                                            **self.style.Button
                                            )
        self.enter_Connecte_button.pack(side="left", padx=5, pady=5)

        self.enter_Connecte_button = Button(self.login_frame,
                                            text="Send CMD",
                                            command=self.send,
                                            **self.style.Button
                                            )
        self.enter_Connecte_button.pack(side="right", padx=5, pady=5)

        ###
        # Message Frame Widgets
        ###

        self.message_entry = Entry(self.message_frame,
                                   textvariable=self.cmd_message,
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
        # commandlist Frame Widgets
        ###

        self.commandlist_label = Label(self.right_frame,
                                       text="SSI Command List",
                                       anchor="w",
                                       **self.style.Label
                                       )
        self.commandlist_label.pack(side="top", fill="x")

        self.commandlist = Scrolled(self.right_frame, Listbox,
                                    attributes=self.style.Listbox,
                                    scrollbar=self.style.Scrollbar,
                                    )
        self.commandlist.pack(side="top", fill="both", expand=1)

        # Add command
        self.commandlist.widget.insert(END, "0x10 FLUSH_MACRO_PDF")
        self.commandlist.widget.insert(END, "0x11 ABORT_MACRO_PDF")
        self.commandlist.widget.insert(END, "0x12 CUSTOM_DEFAULTS")
        self.commandlist.widget.insert(END, "0x80 SSI_MGMT_COMMAND")
        self.commandlist.widget.insert(END, "0xA3 REQUEST_REVISION")
        self.commandlist.widget.insert(END, "0xA4 REPLY_REVISION")
        self.commandlist.widget.insert(END, "0xB0 Reserved")
        self.commandlist.widget.insert(END, "0xB1 IMAGE_DATA")
        self.commandlist.widget.insert(END, "0xB4 VIDEO_DATA")
        self.commandlist.widget.insert(END, "0xC0 ILLUMINATION_OFF")
        self.commandlist.widget.insert(END, "0xC1 ILLUMINATION_ON")
        self.commandlist.widget.insert(END, "0xC4 AIM_OFF")
        self.commandlist.widget.insert(END, "0xC5 AIM_ON")
        self.commandlist.widget.insert(END, "0xC6 PARAM_SEND")
        self.commandlist.widget.insert(END, "0xC7 PARAM_REQUEST")
        self.commandlist.widget.insert(END, "0xC8 PARAM_DEFAULTS")
        self.commandlist.widget.insert(END, "0xC9 CHANGE_ALL_CODE_TYPES")
        self.commandlist.widget.insert(END, "0xCA PAGER_MOTOR_ACTIVATION")
        self.commandlist.widget.insert(END, "0xD0 CMD_ACK")
        self.commandlist.widget.insert(END, "0xD1 CMD_NAK")
        self.commandlist.widget.insert(END, "0xD2 FLUSH_QUEUE")
        self.commandlist.widget.insert(END, "0xD3 CAPABILITIES_REQUEST")
        self.commandlist.widget.insert(END, "0xD4 CAPABILITIES_REPLY")
        self.commandlist.widget.insert(END, "0xD5 BATCH_REQUEST")
        self.commandlist.widget.insert(END, "0xD6 BATCH_DATA")
        self.commandlist.widget.insert(END, "0xD8 CMD_ACK_ACTION")
        self.commandlist.widget.insert(END, "0xE4 START_SESSION")
        self.commandlist.widget.insert(END, "0xE5 STOP_SESSION")
        self.commandlist.widget.insert(END, "0xE6 BEEP")
        self.commandlist.widget.insert(END, "0xE7 LED_ON")
        self.commandlist.widget.insert(END, "0xE8 LED_OFF")
        self.commandlist.widget.insert(END, "0xE9 SCAN_ENABLE")
        self.commandlist.widget.insert(END, "0xEA SCAN_DISABLE")
        self.commandlist.widget.insert(END, "0xEB SLEEP")
        self.commandlist.widget.insert(END, "0xF3 DECODE_DATA")
        self.commandlist.widget.insert(END, "0xF6 EVENT")
        self.commandlist.widget.insert(END, "0xF7 IMAGER_MODE")
        self.commandlist.widget.insert(END, "N/A WAKEUP")

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
            [["[JK] ", "Host"], ["Welcome to the JK SSI tool."]],
            [["[JK] ", "Host"], ["There are only a few rules:"]],
            [["[JK] ", "Host"], ["   Be respectful and sensitive to me"]],
            [["[JK] ", "Host"], ["   And HAVE FUN!"]],
            [["[JK] ", "Host"], [""]],
            [["[JK] ", "Host"], ["Termination of use can happen without warning!"]],
            [["[JK] ", "Host"], [""]],
            [["[JK] ", "Host"], ["JK SSI Tool version v0.01"]],
        ]

        for line in messages:
            self.insert_readonly(self.dialogue_text, 0.0, "\n")
            line.reverse()
            for part in line:
                self.insert_readonly(self.dialogue_text, 0.0, *part)
                #self.insert_readonly(self.dialogue_text, END, "[Admin]", "admin")

    @staticmethod
    def chat_styles(widget):
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

    def conn(self):
        self.serConnector = connect(c)
        if self.serConnector.is_open:
            pass

    def send(self):
        pass


class MainWindowStyles(object):
    """Simple Python class to hold style-related configurations for widgets."""
    Frame = dict(bg="#3C3F41",)

    BaseLabel = dict(font="Helvetica 12 bold", )

    Label = dict(
        bg="#45494A",
        fg="#CCDDDD",
        **BaseLabel
    )

    BaseFormCtrl = dict(
        highlightthickness=0,  # Removes stupid border around the widget
    )

    ListFormCtrl = dict(
        width=30,
        highlightthickness=0,  # Removes stupid border around the widget
    )

    BaseEntry = dict(
        insertwidth=1,
        selectborderwidth=0,
        selectbackground="#0099FF",
        font="Helvetica 12",
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
        bg="#2B2B2B",
        fg="#CCCCCC",
        insertbackground="#FFFFFF",  # Text insertion blinking cursor
        **BaseEntry
    )

    Listbox = dict(
        bg="#2B2B2B",
        fg="#CCCCCC",
        **ListFormCtrl
    )

    Dialogue = dict(
        bg="#2B2B2B",
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
    c = Config('')
    app = CMDHost()
    app.start()
