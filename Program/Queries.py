import sqlite3

connection = sqlite3.connect("music_data.db")
cursor = connection.cursor()

#creating all the tables for the database
def InitDatabase():
    cursor.execute("""CREATE TABLE Artist (
                ArtistID INTEGER NOT NULL UNIQUE,
                Name varchar(50) NOT NULL,
                PRIMARY KEY("ArtistID" AUTOINCREMENT)
                );""")

    cursor.execute("""CREATE TABLE Album (
                AlbumID INTEGER NOT NULL UNIQUE,
                Title varchar(50) NOT NULL,
                PRIMARY KEY("AlbumID" AUTOINCREMENT)
                );""")

    cursor.execute("""CREATE TABLE Genre (
                GenreID INTEGER NOT NULL UNIQUE,
                Title varchar(50) NOT NULL,
                PRIMARY KEY("GenreID" AUTOINCREMENT)
                );""")

    cursor.execute("""CREATE TABLE MusicFile (
                MusicFileID INTEGER NOT NULL UNIQUE,
                FileName varchar(55) NOT NULL UNIQUE,
                Duration INTEGER NOT NULL,
                FileSize INTEGER NOT NULL,
                SampleRate INTEGER NOT NULL,
                PRIMARY KEY("MusicFileID" AUTOINCREMENT)
                );""")

    cursor.execute("""CREATE TABLE Songs (
                SongID INTEGER NOT NULL UNIQUE,
                Title varchar(50) NOT NULL,
                ReleaseDate DATE NOT NULL,
                Description varchar(200),
                Cost FLOAT NOT NULL,
                ArtistID INTEGER NOT NULL,
                AlbumID INTEGER NOT NULL,
                GenreID INTEGER NOT NULL,
                MusicFileID INTEGER NOT NULL,
                PRIMARY KEY("SongID" AUTOINCREMENT)
                FOREIGN KEY("ArtistID") REFERENCES Artist("ArtistID")
                FOREIGN KEY("AlbumID") REFERENCES Album("AlbumID")
                FOREIGN KEY("GenreID") REFERENCES Genre("GenreID")
                FOREIGN KEY("MusicFileID") REFERENCES MusicFile("MusicFileID")
                );""")

    cursor.execute("""CREATE TABLE BankDetails (
                BankDetailsID INTEGER NOT NULL UNIQUE,
                BankNumber INTEGER NOT NULL UNIQUE,
                PRIMARY KEY("BankDetailsID" AUTOINCREMENT)
                );""")

    cursor.execute("""CREATE TABLE User (
                UserID INTEGER NOT NULL UNIQUE,
                Username varchar(50) NOT NULL UNIQUE,
                Password TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                BankDetailsID INTEGER NOT NULL,
                PRIMARY KEY("UserID" AUTOINCREMENT)
                FOREIGN KEY("BankDetailsID") REFERENCES BankDetails("BankDetailsID")
                );""")
    cursor.execute("""CREATE TABLE OwnedMusic (
                OwnedMusicID INTEGER NOT NULL UNIQUE,
                UserID INTEGER NOT NULL,
                SongID INTEGER NOT NULL,
                PRIMARY KEY("OwnedMusicID" AUTOINCREMENT)
                FOREIGN KEY("UserID") REFERENCES UserID("UserID")
                FOREIGN KEY("SongID") REFERENCES SongID("SongID")
                );""")
    cursor.execute("""CREATE TABLE Receipt (
                ReceiptID INTEGER NOT NULL UNIQUE,
                OwnedMusicID INTEGER NOT NULL UNIQUE,
                PurchaseDate DATE NOT NULL,
                Discount INTEGER,
                TotalCost INTEGER NOT NULL,
                PRIMARY KEY("ReceiptID" AUTOINCREMENT)
                FOREIGN KEY("OwnedMusicID") REFERENCES OwnedMusicID("OwnedMusicID")
                );""")

def AddSong(title, releaseDate, description, cost, artist, album, genre, musicfile):
    artist = GetOrAddRecord("Artist", artist, "Name")
    album = GetOrAddRecord("Album", album, "Title")
    genre = GetOrAddRecord("Genre", genre, "Title")

    cursor.execute(f"""INSERT INTO Songs 
                   VALUES(NULL,"{title}", "{releaseDate}", "{description}", "{cost}", "{artist}", "{album}", "{genre}", "{musicfile}")""")
    

def GetOrAddRecord(table, record, attribute):
    if type(record) != int or cursor.execute(f"""SELECT * FROM {table} 
                      WHERE ArtistID = {record} """).fetchall() == []:
        if cursor.execute(f"""SELECT * FROM {table} 
                      WHERE {attribute} = "{record}" """).fetchall() == []:
            print("cool")
            cursor.execute(f"""INSERT INTO {table}("{attribute}") VALUES("{record}")""")
            return cursor.execute(f"""SELECT ArtistID FROM {table}
                      WHERE {attribute} = "{record}" """).fetchall()[0][0]
        else:
            return cursor.execute(f"""SELECT ArtistID FROM {table} 
                      WHERE {attribute} = "{record}" """).fetchall()[0][0]
    return record
AddSong("lol","lol","lol","lol","test","lol", "lol")