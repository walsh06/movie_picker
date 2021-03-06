from tkinter import Frame, Button, Listbox, Label, Entry, Scrollbar
from tkinter import END, RIGHT, VERTICAL, Y, EXTENDED
from random import randint


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


class MovieUtils(Frame):

    def __init__(self, parent, movies):
        Frame.__init__(self, parent)
        self.movies = movies
        self.addLabel = Label(self, text="Enter New Movie Name:")
        self.addLabel.grid(column=1, row=1)
        self.addTextbox = Entry(self, width=35)
        self.addTextbox.grid(column=1, row=2, padx=5)
        self.addButton = Button(self, text="Add Movie", command=self.addMovie)
        self.addButton.grid(column=3, row=2, padx=5)
        self.addTextbox.focus_force()

        self.resetLabel = Label(self, text="Enter Movie Name to Reset Rating:")
        self.resetLabel.grid(column=1, row=3)
        self.resetTextbox = Entry(self, width=35)
        self.resetTextbox.grid(column=1, row=4, padx=5)
        self.resetButton = Button(self, text="Reset Movie", command=self.resetMovie)
        self.resetButton.grid(column=3, row=4, padx=5)

    def addMovie(self):
        self.movies.addByName(self.addTextbox.get())
        self.addTextbox.delete(0, END)

    def resetMovie(self):
        self.movies.resetMovie(self.resetTextbox.get())       
        self.resetTextbox.delete(0, END)
