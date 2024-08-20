import sqlite3
import datetime

connection = sqlite3.connect("C:\\Users\\smoah\\Documents\\Task 6 CS\\Task6-Database-Project-Assessment\\Program\\music_data.db")
cursor = connection.cursor()

#---------------------INITIALIZING DATABASE---------------------#
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
                BankDetailsID INTEGER,
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

#---------------------INSERTING RECORDS---------------------#

#add songs to to Songs Table while either plaintext or identifier key for the Foreign keys
def AddSong(title, releaseDate, description, cost, artist, album, genre, musicfile):
    artist = GetOrAddRecord("Artist", artist, "Name")
    album = GetOrAddRecord("Album", album, "Title")
    genre = GetOrAddRecord("Genre", genre, "Title")
    cursor.execute(f"""INSERT INTO Songs
                   VALUES(NULL,"{title}", "{releaseDate}", "{description}", {cost}, {artist}, {album}, {genre}, {musicfile})""")
    #connection.commit()

#add music file
def AddMusicFile(fileName, duration, fileSize, sampleRate):
    cursor.execute(f"""INSERT INTO MusicFile("FileName", "Duration", "FileSize", "SampleRate") VALUES("{fileName}",{duration},{fileSize},{sampleRate})""")
    #connection.commit()
    return cursor.execute(f"""SELECT * FROM MusicFile 
                          WHERE FileName = "{fileName}"
                        AND Duration = {duration}
                        AND FileSize = {fileSize}
                        AND SampleRate = {sampleRate}""").fetchone()

#checks if the inputted value is the unique idenitifier or the attribute argument
# If the record does not exist, insert it
def GetOrAddRecord(table, record, attribute):
    if type(record) != int or cursor.execute(f"""SELECT * FROM {table} 
                      WHERE {attribute} = {record} """).fetchone() is None:      
        if cursor.execute(f"""SELECT * FROM {table} 
                      WHERE {attribute} = "{record}" """).fetchone() is None:
            cursor.execute(f"""INSERT INTO {table}("{attribute}") VALUES("{record}")""")
            
            return cursor.execute(f"""SELECT * FROM {table}
                      WHERE {attribute} = "{record}" """).fetchone()[0]
        else:
            return cursor.execute(f"""SELECT * FROM {table} 
                      WHERE {attribute} = "{record}" """).fetchone()[0]
    return record

def AddUser(username, password, email, bankDetails):
    if bankDetails.upper() != "NULL":
        bankDetails = GetOrAddRecord("BankDetails", bankDetails, "BankNumber")
    cursor.execute(f"""INSERT INTO User("Username", "Password", "Email", "BankDetailsID") 
                   VALUES("{username}","{password}", "{email}", {bankDetails})""")

def CreateOwnedMusic(userID, songID):
    cursor.execute(f"""INSERT INTO OwnedMusic("UserID", "SongID") VALUES({userID}, {songID})""")
    #connection.commit()
    return cursor.execute(f"""SELECT OwnedMusicID FROM OWnedMusic 
                   WHERE UserID = {userID}
                    AND SongID = {songID}""").fetchone()[0]

def CreateReciept(ownedMusicID, discount):
    ownedMusic = cursor.execute(f"""SELECT * FROM OwnedMusic 
                                WHERE OwnedMusicID = {ownedMusicID}""").fetchone()
    cost = cursor.execute(f"""SELECT Cost FROM Songs
                          WHERE SongID = {ownedMusicID[2]}""")
    totalCost = cost - cost * discount
    purchaseDate = datetime.today().strftime('%Y-%m-%d')
    cursor.execute(f"""INSERT INTO Receipt("OwnedMusicID", "PurchaseDate", "Discount", "TotalCost") 
                   VALUES({ownedMusicID}, "{purchaseDate}", "{discount}", "{totalCost}")""")
    #connection.commit()

#---------------------ACCESSING RECORDS---------------------#
   
def GetUserFromNameAndPassword(name, password):
    check = cursor.execute(f"""SELECT UserID FROM User
                      WHERE Username = {name}
                        AND Password = {password}""").fetchone()
    if check is not None:
        return [check, 0]
    
    check2 = cursor.execute(f"""SELECT UserID FROM User
                      WHERE Username = {name}""").fetchone()

    if check2 is not None:
        return [None, 1]
    else:
        print("account does not exist or has wrong details")
        return [None, 0]

def GetAllSongs():
    return cursor.execute(f"""SELECT * FROM Songs""").fetchall()

def GetAllSongsInGroup(attribute, value):
    return cursor.execute(f"""SELECT * FROM Songs
                        WHERE {attribute} = "{value}" """).fetchall()

def GetAllSongsSorted(attribute, desc):
    if desc:
        return cursor.execute(f"""SELECT * FROM Songs
                            SORT BY {attribute} DESC """).fetchall()
    else:
        return cursor.execute(f"""SELECT * FROM Songs
                            SORT BY {attribute} ASC """).fetchall()
    
#musicFile = AddMusicFile("woah", "100", "1000000", "4410000")
#AddSong("go with the flow","2009-10-23","funny funny", 100,"Queens Of The Stone Age","Songs For The Deaf","Rock", musicFile[0])

cursor.close()