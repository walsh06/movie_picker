import sys
import os
import math

from tkinter import *
from tkinter import filedialog
from random import randint


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
        Ra = movieOne.elo
        Rb = movieTwo.elo
        Pb = self.Probability(Ra, Rb) 
        Pa = self.Probability(Rb, Ra) 

        if winner == 1: 
            winner = "one"
            Ra = Ra + K * (1 - Pa) 
            Rb = Rb + K * (0 - Pb) 
        else: 
            winner = "two"
            Ra = Ra + K * (0 - Pa) 
            Rb = Rb + K * (1 - Pb) 
        
        movieOne.elo = Ra
        movieTwo.elo = Rb
        print("Updated Ratings for winner {}:-".format(winner)) 
        print("{} =".format(movieOne.name), round(Ra, 6)," {} =".format(movieTwo.name), round(Rb, 6)) 

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
            for movie in self.movies:
                f.write("{},{}\n".format(movie.name, movie.elo))


class MoviePicker(Frame):

    def __init__(self, parent, movies):
        Frame.__init__(self, parent)
        self.movies = movies

        self.label = Label(self, text="Pick a Movie")
        self.label.grid(column=1, row=2)

        self.movieOneButton = Button(self, text="temp", command=self.movieOneClicked)
        self.movieTwoButton = Button(self, text="temp", command=self.movieTwoClicked)
        self.movieOneButton.grid(column=0, row=3)
        Label(self, text="V").grid(column=1, row=3)
        self.movieTwoButton.grid(column=2, row=3)
        self.getNewMovies()

    def movieOneClicked(self):
        self.calcResult(1)

    def movieTwoClicked(self):
        self.calcResult(2)

    def calcResult(self, winner):
        self.movies.EloRating(self.movieOneIndex, self.movieTwoIndex, winner)
        self.getNewMovies()
        self.movies.save()
        print(sorted(self.movies))

    def getNewMovies(self):
        self.movieOneIndex = randint(0, len(self.movies) - 1)
        self.movieTwoIndex = self.movieOneIndex
        while self.movieTwoIndex == self.movieOneIndex:
            self.movieTwoIndex = randint(0, len(self.movies) - 1)

        self.movieOneButton.configure(text=self.movies[self.movieOneIndex].name)
        self.movieTwoButton.configure(text=self.movies[self.movieTwoIndex].name)

class Leaderboard(Frame):

    def __init__(self, parent, movies):
        Frame.__init__(self, parent)
        self.movies = movies
        self.listbox = Listbox(self, width=200)
        self.listbox.grid(column=0, row=0)
        self.load()
    
    def load(self):
        self.listbox.delete(0, END)
        for movie in sorted(self.movies, reverse=True):
            self.listbox.insert(END, "{:.3f} | {}".format(movie.elo, movie.name))

def main():
    window = Tk()
    window.title("Testing TKINTER")
    window.geometry('500x500')
    
    filepath = filedialog.askopenfilename()

    movies = MovieList(filepath)
    print(movies)

    def clicked(frame):
        frame.tkraise()
    
    def leaderboardClicked():
        lb.load()
        clicked(lb)

    lb = Leaderboard(window, movies)
    lb.grid(column=0, row=2, sticky='news')
    
    mp = MoviePicker(window, movies)
    mp.grid(column=0, row=2, sticky='news')
    
    menu = Menu(window)

    new_item = Menu(menu)
    new_item.add_command(label='Movie Picker', command=lambda: clicked(mp))
    new_item.add_command(label='Leaderboard', command=lambda: leaderboardClicked())

    menu.add_cascade(label='File', menu=new_item)
    window.config(menu=menu)
    
    window.mainloop()

main()