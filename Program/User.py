from Queries import *

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

def LogIn(username, password):
    user = GetUserFromNameAndPassword(username.lower(), password)[0] 
    if user[0] is not None:
        print("accepted")
        return user[0]
    else:
        print("invalid username or password")
        return None

# SignUp("john_doe", "Password123", "john.doe@example.com", 1234567890)
# SignUp("a" * 50, "ValidPass123", "user.longname@example.com", 2345678901)
# SignUp("jane_doe", "ComplexPassword!123", "jane.doe@example.org", 3456789012)
# SignUp("alice_smith", "SecurePass456", "alice@mail.example.co.uk", 4567890123)
# SignUp("mike_doe_123", "StrongPass789", "mike123@example.com", 5678901234)
# SignUp("chris_2024", "ChrisPass2024", "chris.doe@example.net", 6789012345)
# SignUp("karen_lee", "P@ssword#789", "karen.lee@example.org", 7890123456)
# SignUp("AliceSmith", "UpperCase123", "alice.smith@example.edu", 8901234567)
# SignUp("robert_jones", "NumPass456", "robert.jones2024@example.com", 9012345678)
# SignUp("nancy_miller", "MixedCase789", "Nancy.Miller@Example.org", 1234567809)


