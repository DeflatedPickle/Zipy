#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The main window for Zipy."""

import tkinter as tk
import _tkinter
from tkinter import ttk
import zipfile
import os

import pkinter as pk

__title__ = "Zipy"
__author__ = "DeflatedPickle"
__version__ = "1.0.0"


# http://www.rarlab.com
# http://www.7-zip.org
# http://www.winzip.com/index.html


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Zipy")
        self.geometry("550x500")
        self.minsize(width=350, height=200)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.widget_toolbar = Toolbar(self)
        self.widget_toolbar.grid(row=0, column=0, sticky="we")

        self.widget_statusbar = Statusbar(self)
        self.widget_statusbar.grid(row=2, column=0, sticky="we")

        self.frame_treeview = ttk.Frame(self)
        self.frame_treeview.rowconfigure(0, weight=1)
        self.frame_treeview.columnconfigure(0, weight=1)
        self.frame_treeview.grid(row=1, column=0, sticky="nesw")

        self.widget_treeview = Treeview(self.frame_treeview)
        self.widget_treeview.grid(row=0, column=0, sticky="nesw")
        self.widget_treeview["displaycolumns"] = ("File Extension",
                                                  "Date Modified",
                                                  "File Type",
                                                  "Compress Size",
                                                  "File Size",
                                                  "Filler")
        # print(self.widget_treeview["displaycolumns"])

        self.widget_scrollbar_horizontal = ttk.Scrollbar(self.frame_treeview, orient="horizontal",
                                                         command=self.widget_treeview.xview)
        self.widget_scrollbar_horizontal.grid(row=1, column=0, sticky="we")

        self.widget_scrollbar_vertical = ttk.Scrollbar(self.frame_treeview, orient="vertical",
                                                       command=self.widget_treeview.yview)
        self.widget_scrollbar_vertical.grid(row=0, column=1, sticky="ns")

        self.widget_treeview.configure(xscrollcommand=self.widget_scrollbar_horizontal.set,
                                       yscrollcommand=self.widget_scrollbar_vertical.set)

        self.widget_menu = Menu(self)

    def clear(self):
        for item in self.widget_treeview.get_children():
            self.widget_treeview.delete(item)

    def open_file(self, file):
        self.clear()
        try:
            with zipfile.ZipFile(file, "r") as z:
                previous_folder = ""
                text = ""
                for item in z.infolist():
                    # print(item)
                    if "/" in item.filename:
                        try:
                            self.widget_treeview.insert(parent=previous_folder,
                                                        index="end",
                                                        iid=os.path.splitext(item.filename.split("/")[-2])[0],
                                                        text=os.path.splitext(item.filename.split("/")[-2])[0])
                            previous_folder = os.path.splitext(item.filename.split("/")[-2])[0]
                        except _tkinter.TclError:
                            pass
                        text = os.path.splitext(item.filename.split("/")[-1])[0]
                        self.add_item(item, previous_folder, text)
                    if "/" not in item.filename:
                        previous_folder = ""
                        text = os.path.splitext(item.filename)[0]
                        self.add_item(item, previous_folder, text)
        except FileNotFoundError:
            print("'{}' does not exist.".format(file))

    def add_item(self, item, parent, text):
        self.widget_treeview.insert(parent=parent,
                                    index="end",
                                    iid=os.path.splitext(item.filename)[0],
                                    text=text,
                                    values=[os.path.splitext(item.filename)[1],
                                            "{0[2]}/{0[1]}/{0[0]} {0[5]}:{0[4]}:{0[3]}".format(item.date_time),
                                            "",
                                            item.compress_type,
                                            item.comment,
                                            item.extra,
                                            item.create_system,
                                            item.create_version,
                                            item.extract_version,
                                            item.reserved,
                                            item.flag_bits,
                                            item.volume,
                                            item.internal_attr,
                                            item.external_attr,
                                            item.header_offset,
                                            item.CRC,
                                            item.compress_size,
                                            item.file_size])

    def exit_program(self):
        raise SystemExit


class Menu(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent, type="menubar", *args, **kwargs)
        self.option_add('*tearOff', False)
        self.parent = parent

        self.init_menu_application()
        self.init_menu_view()
        self.init_menu_columns()
        self.init_menu_window()
        self.init_menu_help()
        self.init_menu_system()

        self.parent.configure(menu=self)

    def init_menu_application(self):
        self.menu_application = tk.Menu(self, name="apple")

        self.menu_application.add_command(label="About Zipy", state="disabled")
        self.menu_application.add_command(label="Exit", command=self.parent.exit_program)

        self.add_cascade(label="Application", menu=self.menu_application)

    def init_menu_view(self):
        self.menu_view = tk.Menu(self)

        self.menu_view.add_command(label="Collapse the TreeView", state="disabled")
        self.menu_view.add_command(label="Expand the TreeView", state="disabled")
        self.menu_view.add_command(label="Refresh the TreeView", state="disabled")

        self.add_cascade(label="View", menu=self.menu_view)

    def init_menu_columns(self):
        self.menu_columns = tk.Menu(self.menu_view)
        self.columns_default = ["File Extension", "Date Modified", "File Type", "Compress Size", "File Size", "Filler"]

        # for item in self.parent.widget_treeview["columns"]:
        #     self.menu_columns.add_checkbutton(label=item, variable=tk.BooleanVar())

        # TO DO: Replace menu items below with a for loop to save lines.
        self.boolean_variable_file_extension = tk.BooleanVar()
        self.boolean_variable_file_extension.set(True)
        self.menu_columns.add_checkbutton(label="File Extension", variable=self.boolean_variable_file_extension, command=lambda: self.toggle_column(self.boolean_variable_file_extension, 0, "File Extension"))

        self.boolean_variable_date_modified = tk.BooleanVar()
        self.boolean_variable_date_modified.set(True)
        self.menu_columns.add_checkbutton(label="Date Modified", variable=self.boolean_variable_date_modified, command=lambda: self.toggle_column(self.boolean_variable_date_modified, 1, "Date Modified"))

        self.boolean_variable_file_type = tk.BooleanVar()
        self.boolean_variable_file_type.set(True)
        self.menu_columns.add_checkbutton(label="File Type", variable=self.boolean_variable_file_type, command=lambda: self.toggle_column(self.boolean_variable_file_type, 2, "File Type"))

        self.boolean_variable_compress_type = tk.BooleanVar()
        self.boolean_variable_compress_type.set(False)
        self.menu_columns.add_checkbutton(label="Compress Type", variable=self.boolean_variable_compress_type, command=lambda: self.toggle_column(self.boolean_variable_compress_type, 3, "Compress Type"))

        self.boolean_variable_comment = tk.BooleanVar()
        self.boolean_variable_comment.set(False)
        self.menu_columns.add_checkbutton(label="Comment", variable=self.boolean_variable_comment, command=lambda: self.toggle_column(self.boolean_variable_comment, 4, "Comment"))

        self.boolean_variable_extra = tk.BooleanVar()
        self.boolean_variable_extra.set(False)
        self.menu_columns.add_checkbutton(label="Comment", variable=self.boolean_variable_extra, command=lambda: self.toggle_column(self.boolean_variable_extra, 5, "Extra"))

        self.boolean_variable_create_system = tk.BooleanVar()
        self.boolean_variable_create_system.set(False)
        self.menu_columns.add_checkbutton(label="Create System", variable=self.boolean_variable_create_system, command=lambda: self.toggle_column(self.boolean_variable_create_system, 6, "Create System"))

        self.boolean_variable_create_version = tk.BooleanVar()
        self.boolean_variable_create_version.set(False)
        self.menu_columns.add_checkbutton(label="Create Version", variable=self.boolean_variable_create_version, command=lambda: self.toggle_column(self.boolean_variable_create_version, 7, "Create Version"))

        self.boolean_variable_extract_version = tk.BooleanVar()
        self.boolean_variable_extract_version.set(False)
        self.menu_columns.add_checkbutton(label="Extract Version", variable=self.boolean_variable_extract_version, command=lambda: self.toggle_column(self.boolean_variable_extract_version, 8, "Extract Version"))

        self.boolean_variable_reserved = tk.BooleanVar()
        self.boolean_variable_reserved.set(False)
        self.menu_columns.add_checkbutton(label="Reserved", variable=self.boolean_variable_reserved, command=lambda: self.toggle_column(self.boolean_variable_reserved, 9, "Reserved"))

        self.boolean_variable_flag_bits = tk.BooleanVar()
        self.boolean_variable_flag_bits.set(False)
        self.menu_columns.add_checkbutton(label="Flag Bits", variable=self.boolean_variable_flag_bits, command=lambda: self.toggle_column(self.boolean_variable_flag_bits, 10, "Flag Bits"))

        self.boolean_variable_volume = tk.BooleanVar()
        self.boolean_variable_volume.set(False)
        self.menu_columns.add_checkbutton(label="Volume", variable=self.boolean_variable_volume, command=lambda: self.toggle_column(self.boolean_variable_volume, 11, "Volume"))

        self.boolean_variable_internal_attr = tk.BooleanVar()
        self.boolean_variable_internal_attr.set(False)
        self.menu_columns.add_checkbutton(label="Internal Attr", variable=self.boolean_variable_internal_attr, command=lambda: self.toggle_column(self.boolean_variable_internal_attr, 12, "Internal Attr"))

        self.boolean_variable_external_attr = tk.BooleanVar()
        self.boolean_variable_external_attr.set(False)
        self.menu_columns.add_checkbutton(label="External Attr", variable=self.boolean_variable_external_attr, command=lambda: self.toggle_column(self.boolean_variable_external_attr, 13, "External Attr"))

        self.boolean_variable_header_offset = tk.BooleanVar()
        self.boolean_variable_header_offset.set(False)
        self.menu_columns.add_checkbutton(label="Header Offset", variable=self.boolean_variable_header_offset, command=lambda: self.toggle_column(self.boolean_variable_header_offset, 14, "Header Offset"))

        self.boolean_variable_crc = tk.BooleanVar()
        self.boolean_variable_crc.set(False)
        self.menu_columns.add_checkbutton(label="CRC", variable=self.boolean_variable_crc, command=lambda: self.toggle_column(self.boolean_variable_crc, 15, "CRC"))

        self.boolean_variable_compress_size = tk.BooleanVar()
        self.boolean_variable_compress_size.set(True)
        self.menu_columns.add_checkbutton(label="Compress Size", variable=self.boolean_variable_compress_size, command=lambda: self.toggle_column(self.boolean_variable_compress_size, 16, "Compress Size"))

        self.boolean_variable_file_size = tk.BooleanVar()
        self.boolean_variable_file_size.set(True)
        self.menu_columns.add_checkbutton(label="File Size", variable=self.boolean_variable_file_size, command=lambda: self.toggle_column(self.boolean_variable_file_size, 17, "File Size"))

        self.boolean_variable_filler = tk.BooleanVar()
        self.boolean_variable_filler.set(True)
        self.menu_columns.add_checkbutton(label="Filler", variable=self.boolean_variable_filler, command=lambda: self.toggle_column(self.boolean_variable_filler, 18, "Filler"))

        self.menu_view.add_cascade(label="Columns", menu=self.menu_columns)

    def init_menu_window(self):
        self.menu_window = tk.Menu(self, name="window")
        self.add_cascade(label="Window", menu=self.menu_window)

    def init_menu_help(self):
        self.menu_help = tk.Menu(self, name="help")

        self.add_cascade(label="Help", menu=self.menu_help)

    def init_menu_system(self):
        self.menu_system = tk.Menu(self, name="system")
        self.add_cascade(label="System", menu=self.menu_system)

    def toggle_column(self, variable: tk.BooleanVar, index: int, column: str):
        columns = list(self.parent.widget_treeview["displaycolumns"])
        if variable.get():
            columns.insert(index, column)
            # print("Added '{}' to the shown columns.".format(column))
        else:
            columns.pop(columns.index(column))
            # print("Removed '{}' from the shown columns.".format(column))
        self.parent.widget_treeview["displaycolumns"] = columns = tuple(columns)
        # print(columns)


class Toolbar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


class Statusbar(pk.Statusbar):
    def __init__(self, parent, *args, **kwargs):
        pk.Statusbar.__init__(self, parent, *args, **kwargs)

        self.status_variable = tk.StringVar()
        self.add_variable(textvariable=self.status_variable)

        self.add_sizegrip()


class Treeview(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        ttk.Treeview.__init__(self, parent, selectmode="browse", columns=["File Extension",
                                                                          "Date Modified",
                                                                          "File Type",
                                                                          "Compress Type",
                                                                          "Comment",
                                                                          "Extra",
                                                                          "Create System",
                                                                          "Create Version",
                                                                          "Extract Version",
                                                                          "Reserved",
                                                                          "Flag Bits",
                                                                          "Volume",
                                                                          "Internal Attr",
                                                                          "External Attr",
                                                                          "Header Offset",
                                                                          "CRC",
                                                                          "Compress Size",
                                                                          "File Size",
                                                                          "Filler"], *args, **kwargs)

        self.heading("#0", text="File Name")
        self.column("#0", width=200, stretch=False)
        self.heading("#1", text="File Extension")
        self.column("#1", width=80, stretch=False)
        self.heading("#2", text="Date Modified")
        self.column("#2", width=100, stretch=False)
        self.heading("#3", text="File Type")
        self.column("#3", width=80, stretch=False)
        self.heading("#4", text="Compress Type")
        self.column("#4", width=100, stretch=False)
        self.heading("#5", text="Comment")
        self.column("#5", width=80, stretch=False)
        self.heading("#6", text="Extra")
        self.column("#6", width=60, stretch=False)
        self.heading("#7", text="Create System")
        self.column("#7", width=100, stretch=False)
        self.heading("#8", text="Create Version")
        self.column("#8", width=100, stretch=False)
        self.heading("#9", text="Extract Version")
        self.column("#9", width=100, stretch=False)
        self.heading("#10", text="Reserved")
        self.column("#10", width=100, stretch=False)
        self.heading("#11", text="Flag Bits")
        self.column("#11", width=100, stretch=False)
        self.heading("#12", text="Volume")
        self.column("#12", width=100, stretch=False)
        self.heading("#13", text="Internal Attr")
        self.column("#13", width=100, stretch=False)
        self.heading("#14", text="External Attr")
        self.column("#14", width=100, stretch=False)
        self.heading("#15", text="Header Offset")
        self.column("#15", width=100, stretch=False)
        self.heading("#16", text="CRC")
        self.column("#16", width=100, stretch=False)
        self.heading("#17", text="Compress Size")
        self.column("#17", width=90, stretch=False)
        self.heading("#18", text="File Size")
        self.column("#18", width=70, stretch=False)
        self.column("#19", width=1)


def main():
    app = Window()
    app.open_file(r"C:\Users\PabloPatato\Documents\GitHub\Zipy\test.zip")
    app.mainloop()


if __name__ == "__main__":
    main()
