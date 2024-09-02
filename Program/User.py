from Queries import *

#add new user to database from user inputs
def SignUp(name, password, email, bankDetails):
    if GetUserFromNameAndPassword(name, "NULL")[1] == 1:
        print("Hey this account already exist!")
        return
    
    #conditions for username, password, and email
    condsUserName = [
        lambda s: len(s) <= 50
    ]
    condsPassword = [
        lambda s: any(x.isupper() for x in s),
        lambda s: any(x.islower() for x in s),
        lambda s: any(x.isdigit() for x in s),
        lambda s: len(s) >= 8
    ]
    condsEmail = [
        lambda s: len(s) <= 50,
        lambda s: any(x == "@" for x in s),
        lambda s: any(x == "." for x in s)
    ]

    if not all(cond(name) for cond in condsUserName):
        print("Invalid username. Username must be less than 50 characters")
        return
    elif not all(cond(password) for cond in condsPassword):
        print("Invalid password. Password must have a capital letter, digit, and must be more than 8 characters")
        return
    elif not all(cond(email) for cond in condsEmail):
        print("Invalid Email")
        return
    
    AddUser(name.lower(), password, email.lower(), bankDetails)
    connection.commit()

#check username and password is valid (for when a user front end exists)
def LogIn(username, password):
    user = GetUserFromNameAndPassword(username.lower(), password)[0] 
    if user[0] is not None:
        print("accepted")
        return user[0]
    else:
        print("invalid username or password")
        return None


