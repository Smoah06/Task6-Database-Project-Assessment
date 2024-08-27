from Queries import *

#function for the user to buy music based on their username, song title, and discount
#Creates a Ownedmusic and receipt table
def BuyMusic(username, songTitle, discount):

    user = GetRecordFromAttribute("User", "Username", f"\"{username}\"")
    song = GetRecordFromAttribute("Songs", "Title", f"\"{songTitle}\"")

    ownedMusic = CreateOwnedMusic(user[0], song[0])

    if type(discount) != int or (discount < 0 or discount > 100):
        print("invalid discount")
        return

    CreateReceipt(ownedMusic, discount, song[0])
    connection.commit()
