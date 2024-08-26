from User import *
from Songs import *
from Queries import *

while True:
    option1 = input("Options: \n1) Account Options \n2) Song Options \n3) Receipt Options\n...")

    match int(option1):
        case 1:
            option2 = input("Account Options: \n1) Signup \n2) Login \n3) Delete Account \n4) Modify Account\n...")
            match int(option2):
                case 1:
                    name = input("What is your username? ")
                    password = input("what is your password? ")
                    email = input("What is youyr email? ")
                    bankDetails = input("what is your bank number (type 'NULL' if you want to leave blank)? ")
                    SignUp(name, password, email, bankDetails)
                case 2:
                    name = input("What is your username? ")
                    password = input("what is your password? ")
                    LogIn(name, password)
                case 3:
                    name = input("What is your username? ")
                    password = input("what is your password? ")
                    user = GetUserFromNameAndPassword(name.lower(), password)
                    if user[0] != None:
                        RemoveRecordWithAttribute("User", "UserID", user[0][0])
                case 4:
                    name = input("What is your username? ")
                    password = input("what is your password? ")
                    user = GetUserFromNameAndPassword(name.lower(), password)
                    if user[0] != None:
                        newAttribute = input("What do you want to change? ")
                        newValue = input("What do you want to change it to (make sure text is inside quotes \" \")? ")
                        ModifyRecordWithAttribute("User", "UserID", user[0][0], newAttribute, newValue)
                    else:
                        print("invalid credentials")
        case 2:
            option2 = input("Song Options: \n1) Add Song \n2) Remove Song \n3) Modify Song \n4) View Songs\n...")
            match int(option2):
                case 1:
                    title = input("What is the title? ")
                    releaseDate = input("What is the release date? ")
                    description = input("What is the description? ")
                    cost = input("What is the cost? ")
                    artist = input("What is the artist? ")
                    album = input("What is the album? ")
                    genre = input("What is the genre? ")
                    fileName = input("What is the file name? ")
                    duration = input("What is the duration? ")
                    fileSize = input("What is the file size? ")
                    sampleRate = input("What is the sample rate? ")
                    InsertNewSong(title, releaseDate, description, cost, artist, album, genre, fileName, int(duration), int(fileSize), int(sampleRate))
                case 2:
                    songID = input("What is the song id? ")
                    RemoveRecordWithAttribute("Songs", "SongID", songID)
                case 3:
                    songID = input("What is the song id? ")
                    newAttribute = input("What do you want to change? ")
                    newValue = input("What do you want to change it to (make sure text is inside quotes \" \")? ")
                    ModifyRecordWithAttribute("Songs", "SongID", songID, newAttribute, newValue)
                case 4:
                    option3 = input("ViewSongs: \n1) All Songs \n2) Songs In Category \n3) Sorted Songs\n...")
                    match int(option3):
                        case 1:
                            songs = GetAllSongs()
                            for song in songs:
                                print(song[0],song[1],song[2],"\n",song[3],"\n$",song[4])
                        case 2:
                            attribute = input("What category are you using? ")
                            value = input("What is the category value? ")
                            songs = GetAllSongsInGroup(attribute, value)
                            for song in songs:
                                print(song[0],song[1],song[2],"\n",song[3],"\n$",song[4])
                        case 3:
                            attribute = input("What attribute do you want to sort? ")
                            value = input("DESC or ASC? ")
                            if value == "DESC":
                                songs =GetAllSongsSorted(attribute, True)
                            elif value == "ASC":
                                songs =GetAllSongsSorted(attribute, False)
                            else:
                                print("Input 'DESC' or 'ASC'")
                            
                            for song in songs:
                                print(song[0],song[1],song[2],"\n",song[3],"\n$",song[4])

                    
        case 3:
            option2 = input("Receipt Options: \n1) Get All Profits \n2) Get Profits On Date \n3) Num Of Sales Each Day\n...")
            match int(option2):
                case 1:
                    print(GetAllProfits())
                case 2:
                    option3 = input("Get Profits On Date: \n1) On Day \n2) On Month \n3) On Year\n...")
                    match int(option3):
                        case 1:
                            date = input("What date? ")
                            print(GetAllProfitsOnDay(date))
                        case 2:
                            date = input("What year and month? ")
                            print(GetAllProfitsOnMonth(date))
                        case 3:
                            date = input("What year? ")
                            print(GetAllProfitsOnYear(date))
                case 3:
                    NumOfSalesEachDay()