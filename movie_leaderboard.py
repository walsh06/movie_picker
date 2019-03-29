import sys
import os
import math

from tkinter import Tk, Menu
from tkinter import filedialog
from random import randint

from gui import MoviePicker, Leaderboard, AddMovie

class Movie():

    def __init__(self, name, elo):
        self.name = name
        self.elo = elo

    def __repr__(self):
        return "{} - {}".format(self.name, self.elo)

    def __eq__(self, other):
        return self.elo == other.elo

    def __lt__(self, other):
        return self.elo < other.elo

    def updateElo(self, eloChange):
        self.elo += eloChange


class MovieList():

    def __init__(self, filepath):
        self.filepath = filepath
        self.movies = []
        self.load()

    def __getitem__(self, key):
        return self.movies[key]

    def __len__(self):
        return len(self.movies)

    def __repr__(self):
        string = ""
        for movie in self.movies:
            string += "{}, ".format(movie)
        return string

    def Probability(self, rating1, rating2): 
        return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)) 
    
    def EloRating(self, movieOneIndex, movieTwoIndex, winner): 
        K = 30
        movieOne = self.movies[movieOneIndex]
        movieTwo = self.movies[movieTwoIndex]
        Pb = self.Probability(movieOne.elo, movieTwo.elo) 
        Pa = self.Probability(movieTwo.elo, movieOne.elo) 

        if winner == 1: 
            movieOneChange = K * (1 - Pa) 
            movieTwoChange = K * (0 - Pb) 
        else: 
            movieOneChange = K * (0 - Pa) 
            movieTwoChange = K * (1 - Pb) 
        
        movieOne.updateElo(movieOneChange)
        movieTwo.updateElo(movieTwoChange)
        
        return "{}: {:.2f} ({:.2f}), {}: {:.2f} ({:.2f})".format(movieOne.name, movieOne.elo, movieOneChange, movieTwo.name, movieTwo.elo, movieTwoChange)

    def load(self):
        movies = []
        if os.path.exists(self.filepath):
            with open(self.filepath) as f:
                contents = f.read()
            
            for movie in contents.split("\n"):
                parts = movie.split(",")
                name = parts[0].strip()
                elo = float(parts[1].strip()) if len(parts) > 1 else 1000
                if name:
                    movies.append(Movie(name, elo))
        self.movies = movies

    def save(self):
        with open(self.filepath, "w") as f:
            for movie in sorted(self.movies, reverse=True):
                f.write("{},{}\n".format(movie.name, movie.elo))

    def add(self, movie):
        self.movies.append(movie)
        self.save()

    def addByName(self, movieName, elo=1000):
        if movieName:
            newMovie = Movie(movieName, elo)
            self.add(newMovie)

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
    
    am = AddMovie(window, movies)
    am.grid(column=0, row=2, sticky='news')
    
    menu = Menu(window)

    new_item = Menu(menu, tearoff=False)
    new_item.add_command(label='Movie Picker', command=lambda: clicked(mp))
    new_item.add_command(label='Leaderboard', command=lambda: leaderboardClicked())
    new_item.add_command(label='Add Movie', command=lambda: clicked(am))

    menu.add_cascade(label='File', menu=new_item)
    window.config(menu=menu)
    
    clicked(mp)
    
    window.mainloop()

main()