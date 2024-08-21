import datetime

def InsertNewSong(title, releaseDate, description, cost, artist, album, genre, fileName, duration, fileSize, sampleRate):
    condsTitle = [
        lambda s: len(s) <= 50
    ]
    condsReleaseDate = [
        lambda s: datetime.date.fromisoformat(s),
    ]
    condsDescription = [
        lambda s: len(s) <= 200
    ]
    condsCost = [
        lambda s: s is float
    ]