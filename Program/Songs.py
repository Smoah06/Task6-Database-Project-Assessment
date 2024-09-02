import datetime
from Queries import *

#add new song into the database from user input
def InsertNewSong(title, releaseDate, description, cost, artist, album, genre, fileName, duration, fileSize, sampleRate):
    condsLength = [
        lambda s: len(s) <= 50
    ]
    condsFileName = [
        lambda s: len(s) <= 55
    ]
    condsReleaseDate = [
        lambda s: datetime.date.fromisoformat(s),
    ]
    condsDescription = [
        lambda s: len(s) <= 200
    ]
    condsCost = [
        lambda s: type(s) == float
    ]

    cost = float(cost)

    #i'm sorry for my crime against humanity
    if not all(cond(title) for cond in condsLength):
        print("invalid title")
        return
    elif not all(cond(releaseDate) for cond in condsReleaseDate):
        print("invalid date")
        return
    elif not all(cond(description) for cond in condsDescription):
        print("invalid description")
        return
    elif not all(cond(cost) for cond in condsCost):
        print("invalid cost")
        return
    elif not all(cond(artist) for cond in condsLength):
        print("invalid artist")
        return
    elif not all(cond(album) for cond in condsLength):
        print("invalid album")
        return
    elif not all(cond(genre) for cond in condsLength):
        print("invalid genre")
        return
    elif not all(cond(fileName) for cond in condsFileName):
        print("invalid file name")
        return
    elif type(duration) != int:
        print("invalid duration")
        return
    elif type(fileSize) != int:
        print("invalid file size")
        return
    elif type(sampleRate) != int:
        print("invalid sample rate")
        return

    musicfile = AddMusicFile(fileName, duration, fileSize, sampleRate)
    AddSong(title.lower(), releaseDate, description.lower(), cost, artist.lower(), album.lower(), genre.lower(), musicfile[0])
    connection.commit()