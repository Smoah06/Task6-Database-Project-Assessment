from Queries import *

def BuyMusic(username, songTitle, discount):

    user = GetRecordFromAttribute("User", "Username", f"\"{username}\"")
    song = GetRecordFromAttribute("Songs", "Title", f"\"{songTitle}\"")

    ownedMusic = CreateOwnedMusic(user[0], song[0])

    if type(discount) != int or discount < 0 or discount > 100:
        print("invalid discount")
        return

    CreateReciept(ownedMusic, discount)