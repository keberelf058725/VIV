from tkinter import *
from tkinter import filedialog
import pandas
import numpy
from tkinter.filedialog import askopenfilename
import datetime


# Function for opening the
# file explorer window

def import_csv_data():
    global v
    try:
        csv_file_path = askopenfilename()
        Viv = pandas.read_csv(csv_file_path)
        Viv[['Evaluation Date', 'Evaluation Date_2']] = Viv['Evaluation Date'].str.split(' ', n=1, expand=True)
        Viv.loc[:, ('Evaluation Date')] = pandas.to_datetime(Viv.loc[:, ('Evaluation Date')]).dt.date
        Date_Min = Viv['Evaluation Date'].min()
        Date_Max = Viv['Evaluation Date'].max()
        Date_Min = Date_Min.strftime('%b %d %Y')
        Date_Max = Date_Max.strftime('%b %d %Y')
        Viv['Count'] = 1
        VivT = numpy.sum(Viv['Count'])
    except FileNotFoundError:
        label_file_explorer.configure(text= "You did not \n select a file?")
    except KeyError:
        label_file_explorer.configure(text="You selected \n a unsupported file")
    except Exception:
        label_file_explorer.configure(text="I have know fucking \n idea what happened")
    else:
        label_file_explorer.configure(text='The total number of Vivitrol Injections \n from {} to {} is: {}'.format(Date_Min, Date_Max, VivT))
# Create the root window
window = Tk()

# Set window title
window.title('Vivitrol Monthly Administrations')

# Set window size
window.geometry("450x270")

# Set window background color
window.config(background="white")


# Create a File Explorer label
label_file_explorer = Label(window,
                            text="Vivitrol Administrations",
                            width=40, height=6,
                            fg="blue")

label_file_explorer.config(font=(20))

button_analyze = Button(window,
                        text="Analyze File",
                        command=import_csv_data, width=30,height=2)

button_analyze.config(font=(15))

button_exit = Button(window,
                     text="Exit",
                     command=exit,width=30,height=2)

button_exit.config(font=(15))

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=0, row=1)

button_analyze.grid(column=0, row=3)

button_exit.grid(column=0, row=4)

# Let the window wait for any events
window.mainloop()
