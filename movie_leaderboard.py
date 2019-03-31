import sys
import os
import math

from tkinter import Tk, Menu
from tkinter import filedialog
from random import randint

from gui import MoviePicker, Leaderboard, MovieUtils
from movie import Movie, MovieList

def main():
    window = Tk()
    window.title("Movie Leaderboard")
    window.geometry('550x200')
    
    filepath = filedialog.askopenfilename()

    movies = MovieList(filepath)

    def clicked(frame):
        frame.tkraise()
    
    def leaderboardClicked():
        lb.load()
        clicked(lb)

    lb = Leaderboard(window, movies)
    lb.grid(column=0, row=2, sticky='news')
    
    mp = MoviePicker(window, movies)
    mp.grid(column=0, row=2, sticky='news')
    
    mu = MovieUtils(window, movies)
    mu.grid(column=0, row=2, sticky='news')
    
    menu = Menu(window)

    new_item = Menu(menu, tearoff=False)
    new_item.add_command(label='Movie Picker', command=lambda: clicked(mp))
    new_item.add_command(label='Leaderboard', command=lambda: leaderboardClicked())
    new_item.add_command(label='Movie Options', command=lambda: clicked(mu))

    menu.add_cascade(label='File', menu=new_item)
    window.config(menu=menu)
    
    clicked(mp)    
    window.mainloop()

if __name__ == "__main__":
    main()