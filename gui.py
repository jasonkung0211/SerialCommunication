#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# import Tkinter as tk
from Tkinter import Tk, StringVar, Frame, Label, Entry, Button, Canvas, WORD, IntVar, RIGHT, LEFT
from ttk import Scrollbar, Radiobutton, Combobox

from PIL import ImageTk, Image

from SerialCommunication import *


class commGUI(object):
    def callback(self):
        sendComm(self.name + str(self.value.get()), self.conn)

    def __init__(self, parent, values, connt, name):
        # state = "disabled"
        self.style = MainWindowStyles()
        self.value = IntVar(0)
        self.value.set(values)
        self.name = name
        self.conn = connt
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
        parent.title("Z5212 Debug Client by 2017 ZEBEX, Inc. Version 1.3")
        resize_and_center(parent, 900, 480)

        self.conn_status = StringVar()
        self.conn_status.set('...')

        # Top Frame (name entry box, buttons, conn status)
        self.conn_frame = Frame(parent, **self.style.Frame)
        self.conn_frame.pack(side="top", fill="x")

        self.lower_frame = Frame(parent, **self.style.Frame)
        self.lower_frame.pack(side="top", fill="both", expand=1)

        # The message entry
        self.display_frame = Frame(self.lower_frame, **self.style.Frame)
        self.display_frame.pack(side="top", fill="both", expand=1, padx=5, pady=5)

        self.right_frame = Frame(self.lower_frame, **self.style.Frame)
        self.right_frame.pack(side="right", fill="y")

        ###
        # Top Frame Widgets
        ###
        self.name_label = Label(self.conn_frame,
                                textvariable=self.conn_status,
                                **self.style.Label
                               ).pack(side="left", padx=5, pady=5)

        Button(self.conn_frame, text='連線', command=self.conn, **self.style.SettingButton)\
            .pack(side="left", padx=5, pady=5)

        Button(self.conn_frame, text="重新開始", command=self.reopen, **self.style.SettingButton)\
            .pack(side="left", padx=5, pady=5)

        self.ports_Combobox = Combobox(self.conn_frame, values=c.port, width=8)
        # assign function to combobox
        self.ports_Combobox.bind('<<ComboboxSelected>>', self.port_on_select)
        self.ports_Combobox.current(portindex)

        self.baud_rate_Combo = Combobox(self.conn_frame, values=c.baud, width=8)
        self.baud_rate_Combo.bind('<<ComboboxSelected>>', self.baud_rate_on_select)
        self.baud_rate_Combo.current(baudindex)

        self.enter_exit_button = Button(self.conn_frame,
                                        text="回復預設值",
                                        command=self.quit,
                                        **self.style.Button
                                        )

        self.ports_Combobox.pack(side="left", padx=5, pady=5)
        self.baud_rate_Combo.pack(side="left", padx=5, pady=5)
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

        Button(self.conn_frame, text='拍照', command=self.getimg, **self.style.SettingButton).pack(side="left",
                                                                                                        padx=5, pady=5)

        ###
        # Display Frame Widgets
        ###
        self.display_frame.configure(background='#666666')
        # Create a canvas
        self.canvas = Canvas(self.display_frame, width=640, height=360, bg="#666666")
        self.loadImage('Capture.jpg')

    def conn(self):
        self.conn_status.set("...")
        c = Config('')
        c.baud = self.baud_rate_Combo.get()
        c.port = self.ports_Combobox.get()
        c.isRs232 = int(c.baud) - 115200 <= 0
        c.dump()
        self.serConnector = connect(c)
        serConnector = self.serConnector
        Has_response = handshake(self.serConnector)
        if Has_response:
            setDefault(c, self.serConnector)
            self.conn_status.set('已連線')
            commGUI(self.right_frame, c.Gain, self.serConnector, "Gain")
            commGUI(self.right_frame, c.Shutter, self.serConnector, "Shutter")
            commGUI(self.right_frame, c.light, self.serConnector, "light")



    def baud_rate_on_select(self, event=None):
        print("event.widget:", event.widget.get())

    def port_on_select(self, event=None):
        print("event.widget:", event.widget.get())

    def quit(self):
        self.serConnector.write("quit".encode('ascii') + '\r\n')

    def reopen(self):
        portindex = self.ports_Combobox.getint
        baudindex = self.baud_rate_Combo.getint
        try:
            self.serConnector.close()
        except AttributeError:
            pass
        self.mw.destroy()
        app = CoreGUI()

    def getimg(self):
        self.canvas.delete("all")
        getImage("image" + str(self.quality.get()), self.serConnector, c.isRs232)
        self.loadImage('Capture.jpg')

    def loadImage(self, filename):
        # Load the image file
        try:
            im = Image.open(filename)
        except IOError:
            print 'IOError'
            return
        # Put the image into a canvas compatible class, and stick in an
        # arbitrary variable to the garbage collector doesn't destroy it
        self.canvas.image = ImageTk.PhotoImage(im)
        # Add the image to the canvas, and set the anchor to the top left / north west corner
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        self.canvas.pack()

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
    c = Config('')
    portindex = 0
    baudindex = 0
    # c.isRs232 = int(c.baud) - 115200 <= 0
    # c.dump()
    serConnector = None

    # Has_response = handshake(serConnector)

    # if Has_response:
    #     setDefault(c, serConnector)
    app = CoreGUI()
    app.start()



