import sys
import os
import math

from Tkinter import *
import tkFileDialog
from random import randint


class Movie():

    def __init__(self, name, elo=1000):
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


class MoviePicker(Frame):

    def __init__(self, parent, movies):
        Frame.__init__(self, parent)
        self.movies = movies

        self.label = Label(self, text="Pick a Movie")
        self.label.grid(column=1, row=2)

        self.movieOneButton = Button(self, text="temp", command=self.movieOneClicked)
        self.movieTwoButton = Button(self, text="temp", command=self.movieTwoClicked)
        self.movieOneButton.grid(column=0, row=3, padx=10)
        Label(self, text="V").grid(column=1, row=3)
        self.movieTwoButton.grid(column=2, row=3, padx=10)
        self.movieOneIndex = -1
        self.movieTwoIndex = -1
        self.getNewMovies()
        self.output = Label(self, text="")
        self.output.grid(column=0, row=4, columnspan=3, pady=50, padx=20)

    def movieOneClicked(self):
        self.calcResult(1)

    def movieTwoClicked(self):
        self.calcResult(2)

    def calcResult(self, winner):
        result = self.movies.EloRating(self.movieOneIndex, self.movieTwoIndex, winner)
        self.output.config(text="Previous Matchup\n{}".format(result))
        self.getNewMovies()
        self.movies.save()

    def getNewMovies(self):
        oldIndex = self.movieOneIndex
        while oldIndex == self.movieOneIndex:
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
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.listbox = Listbox(self, width=80, yscrollcommand=scrollbar.set, selectmode=EXTENDED)
        self.listbox.pack(expand=True, fill=Y)
        scrollbar.config(command=self.listbox.yview)

        self.load()
    
    def load(self):
        self.listbox.delete(0, END)
        count = 1
        for movie in sorted(self.movies, reverse=True):
            self.listbox.insert(END, "{}. {} ({:.2f})".format(count, movie.name, movie.elo))
            count += 1

class AddMovie(Frame):

    def __init__(self, parent, movies):
        Frame.__init__(self, parent)
        self.movies = movies
        self.label = Label(self, text="Enter New Movie Name:")
        self.label.grid(column=1, row=1)
        self.textbox = Entry(self, width=35)
        self.textbox.grid(column=1, row=2, padx=5)
        self.button = Button(self, text="Add Movie", command=self.addMovie)
        self.button.grid(column=3, row=2, padx=5)

    def addMovie(self):
        self.movies.addByName(self.textbox.get())
        self.textbox.delete(0, END)

def main():
    window = Tk()
    window.title("Movie Leaderboard")
    window.geometry('550x200')
    
    filepath = tkFileDialog.askopenfilename()

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