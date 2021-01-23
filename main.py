# @author : Hugo Simony
# github : https://github.com/hugosimony
# creation date : 20/01/2021

# -------------------------------------------------------------------------------------------------------------
# imports

from tkinter import *
import threading
import time
import random
import os.path
from os import path


# -------------------------------------------------------------------------------------------------------------
# variables (n, p and speed can be set by the user)

class Var:
    def __init__(self, n=50, p=0.58, speed=0.01):
        self.n = n          # the size of the squared matrix is n*n
        self.p = p          # the probability of erosion for each part of the concrete
        self.speed = speed  # the speed of the animation (in seconds)

        self.concrete = []  # the matrix representing the concrete
        self.to_treat = []  # the list of the spots of the concrete where some water has to be put


var = Var()


# -------------------------------------------------------------------------------------------------------------
# classes

class Simulation (threading.Thread):
    def __init__(self, sec):
        threading.Thread.__init__(self)
        self.sec = sec

    def run(self):
        while len(var.to_treat) != 0:
            x, y = var.to_treat[0]
            var.to_treat.pop(0)
            if y == var.n-1:
                # the water has reach the bottom of the concrete
                canvas.create_rectangle(x * (600 / var.n), y * (600 / var.n), (x + 1) * (600 / var.n),
                                        (y + 1) * (600 / var.n), fill='red', outline='red')
            else:
                # the water is still inside the concrete
                canvas.create_rectangle(x * (600 / var.n), y * (600 / var.n), (x + 1) * (600 / var.n),
                                        (y + 1) * (600 / var.n), fill='blue', outline='blue')
            for i_ in range(-1, 2):
                for j_ in range(-1, 2):
                    # only check up, down, on the left and on the right of the actual coordinates
                    # verify if the checked coordinates are not out of bounds
                    # check if the checked coordinates represent an eroded concrete hole
                    if i_ != j_ and i_ != -j_ and 0 <= x + i_ < var.n and 0 <= y + j_ < var.n \
                            and var.concrete[x + i_][y + j_] == 1:
                        # put water in the eroded concrete hole
                        var.concrete[x + i_][y + j_] = 2
                        var.to_treat.append((x + i_, y + j_))
            # speed of the animation
            time.sleep(self.sec)
        else:
            # no water can be placed anymore, the animation is over
            print("Done")


# -------------------------------------------------------------------------------------------------------------
# functions

def reset_values():
    # set all values to default
    var.n = 50
    var.p = 0.58
    var.speed = 0.01
    var.concrete = []
    var.to_treat = []

    # create the default random concrete and draw it
    create_concrete(var.p)
    draw_concrete()


def create_concrete(probability):
    # initialize the matrix representing the concrete
    # 0 represents non-eroded concrete
    # 1 represents eroded concrete
    # 2 represents water
    for i1 in range(var.n):
        var.concrete.append([])
        for i2 in range(var.n):
            r = random.random()
            if r > probability:
                # this concrete part will not erode with time
                var.concrete[i1].append(0)
            else:
                # this concrete part will erode with time
                var.concrete[i1].append(1)
        # the first layer of eroded concrete is filled with water
        if var.concrete[i1][0] == 1:
            var.to_treat.append((i1, 0))
            var.concrete[i1][0] = 2


def simulation():
    # start the animation
    s = Simulation(var.speed)
    s.start()


def draw_concrete():
    # draw the concrete matrix on the window
    for i in range(var.n):
        for j in range(var.n):
            if var.concrete[i][j] == 0:
                # this is a non-eroded concrete part
                canvas.create_rectangle(i * (600 / var.n), j * (600 / var.n), (i + 1) * (600 / var.n),
                                        (j + 1) * (600 / var.n), fill='black', outline='black')
            else:
                # this is an eroded concrete part
                canvas.create_rectangle(i * (600 / var.n), j * (600 / var.n), (i + 1) * (600 / var.n),
                                        (j + 1) * (600 / var.n), fill='white', outline='white')


# -------------------------------------------------------------------------------------------------------------
# window

window = Tk()

window.title("Water Visualization")

# set the window not resizable
window.geometry("620x750")
window.minsize(620, 750)
window.maxsize(620, 750)

# change the icon of the frame if the icon is found
if path.exists("water_icon.ico"):
    window.iconbitmap("water_icon.ico")

window.config(background='black')

label_water = Label(window, text="Simulation of water flowing in concrete", font=("Arial", 20), bg='black', fg='white')
label_water.pack(side=TOP)

# the grid representing the concrete
panel = Frame(window, bg='black', bd=1, relief=SUNKEN)
canvas = Canvas(panel, width=600, height=600)

# start the animation (calling the simulation() function)
start_button = Button(window, text='Start', font=("Arial", 20), bg='green', fg='white', command=simulation)
start_button.pack(fill=X, side=BOTTOM)

# -------------------------------------------------------------------------------------------------------------
# initialization

# create the concrete matrix with the probability set by the user and draw it
create_concrete(var.p)
draw_concrete()

# -------------------------------------------------------------------------------------------------------------
# finishing window

canvas.pack()
panel.pack(expand=YES)
window.mainloop()
