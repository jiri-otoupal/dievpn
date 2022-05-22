from pathlib import Path
from tkinter import filedialog, StringVar


def select_file(var: StringVar, initial_dir="/"):
    filetypes = (
        ('All files', '*.*'),
    )

    filename = filedialog.askopenfilename(
        title='Select vpn cli file',
        initialdir=initial_dir,
        filetypes=filetypes)
    if filename:
        var.set(filename)
