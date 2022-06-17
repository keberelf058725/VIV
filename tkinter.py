from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np


# Function for opening the
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("CSV files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)

def analyze_file():
    Viv = pd.read_csv(filename)
    Viv['Count'] = 1
    VivT = np.sum(Viv['Count'])
    Vitrol_Monthly_Count = 'The total number of Vivitrol Injections this month was: {}'.format(VivT)
    print(Vitrol_Monthly_Count)

# Create the root window
window = Tk()

# Set window title
window.title('Vivitrol Monthly Administrations')

# Set window size
window.geometry("500x500")

# Set window background color
window.config(background="white")

# Create a File Explorer label
label_file_explorer = Label(window,
                            text="Vivitrol Administrations",
                            width=100, height=4,
                            fg="blue")

button_explore = Button(window,
                        text="Browse Files",
                        command=browseFiles)

button_analyze = Button(window,
                        text="Analyze File",
                        command=analyze_file)


button_exit = Button(window,
                     text="Exit",
                     command=exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=0, row=1)

button_explore.grid(column=0, row=2)

button_analyze.grid(column=0, row=3)

button_exit.grid(column=0, row=4)

# Let the window wait for any events
window.mainloop()
