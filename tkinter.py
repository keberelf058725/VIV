from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
from tkinter.filedialog import askopenfilename


# Function for opening the
# file explorer window

def import_csv_data():
    global v
    csv_file_path = askopenfilename()
    Viv = pd.read_csv(csv_file_path)
    Viv['Count'] = 1
    VivT = np.sum(Viv['Count'])

    label_file_explorer.configure(text='The total number of Vivitrol Injections this month was: {}'.format(VivT))

# Create the root window
window = Tk()

# Set window title
window.title('Vivitrol Monthly Administrations')

# Set window size
window.geometry("700x500")

# Set window background color
window.config(background="white")

# Create a File Explorer label
label_file_explorer = Label(window,
                            text="Vivitrol Administrations",
                            width=100, height=4,
                            fg="blue")

button_analyze = Button(window,
                        text="Analyze File",
                        command=import_csv_data)


button_exit = Button(window,
                     text="Exit",
                     command=exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=0, row=1)

button_analyze.grid(column=0, row=3)

button_exit.grid(column=0, row=4)

# Let the window wait for any events
window.mainloop()
