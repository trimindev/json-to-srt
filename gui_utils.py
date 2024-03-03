import tkinter as tk
from tkinter import filedialog


def create_entry(self, label_text, row, isFolder=False, isBrowse=False):
    frame = tk.Frame(self.root)
    frame.grid(row=row, column=0, padx=10, pady=5, sticky="w")

    label = tk.Label(frame, text=label_text)
    label.grid(row=0, column=0, padx=5, pady=5)

    entry = tk.Entry(frame, width=30)
    entry.grid(row=0, column=1, padx=5, pady=5)

    if isBrowse:

        def browse():
            if isFolder:
                folder = filedialog.askdirectory()
                if folder:
                    entry.delete(0, tk.END)
                    entry.insert(0, folder)
            else:
                file = filedialog.askopenfilename()
                if file:
                    entry.delete(0, tk.END)
                    entry.insert(0, file)

        button = tk.Button(frame, text="Browse", command=browse)
        button.grid(row=0, column=2, padx=5, pady=5)

    return entry


def create_button(self, text, command, row):
    button = tk.Button(self.root, text=text, command=command)
    button.grid(row=row, column=0, padx=10, pady=5)
    return button


def create_status_label(self, text, row):
    label = tk.Label(self.root, text=text)
    label.grid(row=row, column=0, padx=10, pady=5)
    return label
