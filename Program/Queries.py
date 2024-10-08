import sqlite3
import datetime
import atexit

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
                PRIMARY KEY("AlbumID")
                );""")

    cursor.execute("""CREATE TABLE Genre (
                GenreID INTEGER NOT NULL UNIQUE,
                Title varchar(50) NOT NULL,
                PRIMARY KEY("GenreID")
                );""")

    cursor.execute("""CREATE TABLE MusicFile (
                MusicFileID INTEGER NOT NULL UNIQUE,
                FileName varchar(55) NOT NULL UNIQUE,
                Duration INTEGER NOT NULL,
                FileSize INTEGER NOT NULL,
                SampleRate INTEGER NOT NULL,
                PRIMARY KEY("MusicFileID")
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
                PRIMARY KEY("SongID")
                FOREIGN KEY("ArtistID") REFERENCES Artist("ArtistID")
                FOREIGN KEY("AlbumID") REFERENCES Album("AlbumID")
                FOREIGN KEY("GenreID") REFERENCES Genre("GenreID")
                FOREIGN KEY("MusicFileID") REFERENCES MusicFile("MusicFileID")
                );""")

    cursor.execute("""CREATE TABLE BankDetails (
                BankDetailsID INTEGER NOT NULL UNIQUE,
                BankNumber INTEGER NOT NULL UNIQUE,
                PRIMARY KEY("BankDetailsID")
                );""")

    cursor.execute("""CREATE TABLE User (
                UserID INTEGER NOT NULL UNIQUE,
                Username varchar(50) NOT NULL UNIQUE,
                Password TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                BankDetailsID INTEGER,
                PRIMARY KEY("UserID")
                FOREIGN KEY("BankDetailsID") REFERENCES BankDetails("BankDetailsID")
                );""")
    cursor.execute("""CREATE TABLE OwnedMusic (
                OwnedMusicID INTEGER NOT NULL UNIQUE,
                UserID INTEGER NOT NULL,
                SongID INTEGER NOT NULL,
                PRIMARY KEY("OwnedMusicID")
                FOREIGN KEY("UserID") REFERENCES UserID("UserID")
                FOREIGN KEY("SongID") REFERENCES SongID("SongID")
                );""")
    cursor.execute("""CREATE TABLE Receipt (
                ReceiptID INTEGER NOT NULL UNIQUE,
                OwnedMusicID INTEGER NOT NULL UNIQUE,
                PurchaseDate DATE NOT NULL,
                Discount INTEGER,
                TotalCost INTEGER NOT NULL,
                PRIMARY KEY("ReceiptID")
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

#add an user to the user table
def AddUser(username, password, email, bankDetails):
    if bankDetails is not str:
        bankDetails = GetOrAddRecord("BankDetails", bankDetails, "BankNumber")
    elif bankDetails.upper() != "NULL":
        bankDetails = GetOrAddRecord("BankDetails", bankDetails, "BankNumber")
    cursor.execute(f"""INSERT INTO User("Username", "Password", "Email", "BankDetailsID") 
                   VALUES("{username}","{password}", "{email}", {bankDetails})""")

#create a record for owned music with user and song id
def CreateOwnedMusic(userID, songID):
    cursor.execute(f"""INSERT INTO OwnedMusic("UserID", "SongID") VALUES({userID}, {songID})""")
    return cursor.execute(f"""SELECT OwnedMusicID FROM OWnedMusic 
                   WHERE UserID = {userID}
                    AND SongID = {songID}""").fetchone()[0]

#create a receipt based on ownedmusic and discount
def CreateReceipt(ownedMusicID, discount, songID):
    ownedMusic = cursor.execute(f"""SELECT * FROM OwnedMusic 
                                WHERE OwnedMusicID = {ownedMusicID}""").fetchone()
    cost = cursor.execute(f"""SELECT Cost FROM Songs
                          WHERE SongID = {songID}""").fetchone()[0]
    totalCost = float(cost) - float(cost) * float(discount)/100
    purchaseDate = datetime.datetime.today().strftime('%Y-%m-%d')
    cursor.execute(f"""INSERT INTO Receipt("OwnedMusicID", "PurchaseDate", "Discount", "TotalCost") 
                   VALUES({ownedMusicID}, "{purchaseDate}", "{discount}", "{totalCost}")""")

#---------------------ACCESSING RECORDS---------------------#
   
#get record from value
def GetRecordFromAttribute(table, attribute, value):
    return cursor.execute(f"""SELECT * FROM {table}
                            WHERE {attribute} = {value} """).fetchone()

#check if the username or password is correct 
def GetUserFromNameAndPassword(name, password):

    # [UserID if valid username and password, user exists]

    check = cursor.execute(f"""SELECT UserID FROM User
                      WHERE Username = "{name}" 
                      AND Password = "{password}" """).fetchone()
    if check is not None:
        print("Epic")
        return [check, 1]
    
    check2 = cursor.execute(f"""SELECT UserID FROM User
                      WHERE Username = "{name}" """).fetchone()

    if check2 is not None:
        return [None, 1]
    else:
        return [None, 0]

#get all song records
def GetAllSongs():
    return cursor.execute(f"""SELECT * FROM Songs""").fetchall()

#filter song records
def GetAllSongsInGroup(attribute, value):
    return cursor.execute(f"""SELECT * FROM Songs
                        WHERE {attribute} = "{value}" """).fetchall()

#sort song records
def GetAllSongsSorted(attribute, desc):
    if desc:
        return cursor.execute(f"""SELECT * FROM Songs
                            SORT BY {attribute} DESC """).fetchall()
    else:
        return cursor.execute(f"""SELECT * FROM Songs
                            ORDER BY {attribute} ASC """).fetchall()

#get all owned music based on username
def GetMusicOwnedByUser(username):
    return cursor.execute(f"""SELECT * FROM OwnedMusic
                          INNER JOIN Songs ON Song.SongID = OwnedMusic.SongID
                          INNER JOIN User ON User.UserID = OwnedMusic.UserID
                          WHERE Username = "{username}" """).fetchall()

#---------------------PROFITS---------------------#
#get all profit
def GetAllProfits():
    return cursor.execute(f"""SELECT SUM(TotalCost) FROM Receipt""").fetchone()[0]

#get all profit on a specific day
def GetAllProfitsOnDay(date):
    return cursor.execute(f"""SELECT SUM(TotalCost) AS Profit FROM Receipt
                          WHERE PurchaseDate = "{date}" """).fetchone()[0]
#get all profit on a specific month
def GetAllProfitsOnMonth(date):
    return cursor.execute(f"""SELECT SUM(TotalCost) AS Profit FROM Receipt
                          WHERE PurchaseDate LIKE "{date}%" """).fetchone()[0]
#get all profit on a specific year
def GetAllProfitsOnYear(year):
    return cursor.execute(f"""SELECT SUM(TotalCost) AS Profit FROM Receipt
                          WHERE PurchaseDate LIKE "{year}%" """).fetchone()[0]

#number of sales each day
def NumOfSalesEachDay():
    data = cursor.execute(f"""SELECT COUNT(ReceiptID) AS NumberOfSales, PurchaseDate FROM Receipt
                          GROUP BY PurchaseDate""").fetchall()
    return [data, cursor.description]

#---------------------MODIFY RECORDS---------------------#

#modify record with value
def ModifyRecordWithAttribute(table, attribute, value, newAttribute, newValue):
    cursor.execute(f"""UPDATE {table}
                    SET {newAttribute} = {newValue}
                    WHERE {attribute} = {value}""")
    connection.commit()

#---------------------REMOVE RECORDS---------------------#

#remove record with value
def RemoveRecordWithAttribute(table, attribute, value):
    cursor.execute(f"""DELETE FROM {table}
                    WHERE {attribute} = {value};""")
    connection.commit()

#Delete every record
def Purge():
    cursor.execute("""DELETE FROM Receipt""")
    cursor.execute("""DELETE FROM OwnedMusic""")
    cursor.execute("""DELETE FROM Songs""")
    cursor.execute("""DELETE FROM Artist""")
    cursor.execute("""DELETE FROM Genre""")
    cursor.execute("""DELETE FROM Album""")
    cursor.execute("""DELETE FROM MusicFile""")
    cursor.execute("""DELETE FROM User""")
    cursor.execute("""DELETE FROM BankDetails""")
    connection.commit()

#Purge()

#making sure the cursor is closed when the user stops running the python file
@atexit.register
def quit():
    print("\n bye bye")
    cursor.close()