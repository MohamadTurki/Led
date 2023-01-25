import datetime 
import os
import sys
import time
import string
import random
import math
import sqlite3
import re
from pytube import YouTube
#Shbeshbe
class User:
    def __init__(self):
        self.username = None
        self.password = None

    def get_credentials(self):
        self.username = input("What's your name: ")
        while not re.match(r"[A-Za-z]+", self.username):
            print("Invalid name, please enter a valid name.")
            self.username = input("What's your name: ")
        self.password = input("Enter your password: ")

def login_or_register():
    print("Hello my name is led")
    print("1. Login, 2. Register")
    user_selection = input("Select one: ")
    if user_selection in ["1", "2"]:
        return user_selection
    else:
        print("Invalid Choice")
        sys.exit()

name = ""

DB_NAME = "users.db"
guide_str = "Type one of the following (calc, quit, cls, cmd, date, myPc, weather, ytDownloader, guessingGame, searchEngine, fitness, help)"
def database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create users table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (username text, password text, height real, weight real, path text, gender text, activity integer)''')
    conn.commit()

    user = User()
    user_selection = login_or_register()
    if user_selection == "2":
        user.get_credentials()
        # Check if user already exists
        c.execute("SELECT * FROM users WHERE username = ?", (user.username,))
        if c.fetchone() is not None:
            print("User is already registered!")
            sys.exit()
        else:
            # Insert the user's information into the database
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
            conn.commit()
            print("Registration successful!")

    elif user_selection == "1":
        user.get_credentials()
        # Check if user exists and password is correct
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user.username, user.password))
        if c.fetchone() is not None:
            print("Login successful!")
        else:
            print("The Login was unsuccessful!")
            sys.exit()

    def welcome(user):
        if user and user.username:
            print("Ok " +  user.username + ", " + guide_str)
        else:
            print("User is not defined or logged in.")
    #EDITING / ADDING TABLES AND DELETING RECORDS
    # c.execute("ALTER TABLE users ADD COLUMN path TEXT")
    # c.execute("ALTER TABLE users ADD COLUMN gender TEXT")
    # c.execute("ALTER TABLE users ADD COLUMN activity INTEGER")
    # c.execute("DELETE FROM users WHERE username = ?", ('led'))
    # conn.commit()

    if user:
        welcome(user)
        
    conn.close()
    return (user.username,user.password)

    # #PRINT USERNAMES
    # c.execute("SELECT username FROM users")
    # users = c.fetchall()
    # if users:
    #     print("List of registered users:")
    #     for user in users:
    #         print(user[0])
    # else:
    #     print("No users found in the database.")
        
name, password = database()


def exec_cmd(cmd):

    # Create a dictionary that maps strings to functions
    cmds = {
        "calc": calc,
        "quit": byebye,
        "cls": clear_screen,
        "date": date,
        "weather": weather,
        "help": help,
        "ytdownloader": ytdownloader,
        "mypc": mypc,
        "cmd": cmd_func,
        "guessing_game": guessing_game,
        "search_engine": search_engine,
        "fitness": fitness
    }

    aliases = {
        "calc": ["calculator", "calc","cl"],
        "quit": ["quit", "exit", "byebye"],
        "cls": ["cls", "clear_screen"],
        "date": ["date", "d"],
        "weather": ["weather", "wt"],
        "help": ["help"],
        "ytdownloader": ["ytDownloader", "ytdn", "yd"],
        "myPc": ["mypc", "pc"],
        "cmd": ["cmd", "command", "c"],
        "guessing_game": ["guessinggame", "guessingGame", "gg"],
        "fitness": ["fitness", "gym", "ft"],
        "search_engine": ["SearchEngine","se"]
    }


    for key, val in aliases.items():
        if cmd in val:
            cmds[key]()
            break


def main():
    while True:
        cmd = input("Led: ")
        exec_cmd(cmd)

def cmd_func():
    print("Write \"led\" to go back")
    while True:
        usr_cmd = str(input("Enter cmd commands: "))
        if(usr_cmd == "led"):
            main()
        os.system(usr_cmd)

def guessing_game():
    random_num = random.randint(1, 10)
    curr_attempt_num = 0
    print("(You have 3 attempts)")

    invalid_guess_msgs = (
        "No characters, No symbols, No spaces",
        "I said no characters, no symbols, no spaces",
        "Can't you read ?",
        "Oh come on..",
        "Just go away",
    )
    not_out_of_range = False

    for i in range(len(invalid_guess_msgs)):
        try:
            guessed_num = int(input("Guess a number between 1 and 10: "))
            if guessed_num > 10 or guessed_num < 1:
                not_out_of_range = True
                print("Invalid Number")
                main()
            while True:
                if (guessed_num == random_num and not_out_of_range == True):
                    print("Congrats, You won!")
                    main()
                elif guessed_num != random_num and not_out_of_range == True:
                    if guessed_num < random_num:
                        guessed_num = int(input("Go higher!: "))
                        curr_attempt_num += 1
                    elif guessed_num > random_num:
                        guessed_num = int(input("Go lower!: "))
                        curr_attempt_num += 1
                if (curr_attempt_num == 2):
                    print("Unfortunetly, You lost.")
                    print("The number was " + str(random_num))
                    main()
                else:
                    not_out_of_range = True
        except:
            print(invalid_guess_msgs[i])
            if(i >= len(invalid_guess_msgs)):
                print(invalid_guess_msgs[i-1])

def date():
    print(datetime.datetime.now().date())

def weather():
    os.system("curl wttr.in")

def clear_screen():
    os.system("cls")
    print(guide_str)

def byebye():
    print("Bye Bye!")
    sys.exit()

def search_engine():
    os.system("cls")
    print("Write \"led\" to go back")
    while True:
        src = input("Search anything: ")
        search = src.replace(" ", "%20")
        if(src == ""):
            search_engine()
        elif(src == "led"):
            os.system("cls")
            print(guide_str)
            main()
        else:
            search_cmd = "start https://duckduckgo.com/?q={}".format(search)
            os.system(search_cmd)    

def fitness():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    def get_weight_height():
        c.execute("SELECT weight, height FROM users WHERE username = ? AND password = ? AND weight IS NULL AND height IS NULL", (name, password))
        results = c.fetchall()
        if len(results) > 0:
            weight = float(input("Enter your Weight in kg: "))
            height = float(input("Enter your Height in cm: "))/100
            c.execute("UPDATE users SET weight = ?, height = ? WHERE username = ? AND password = ?", (weight, height, name, password))
        else:
            c.execute("SELECT weight, height FROM users WHERE username = ? AND password = ?", (name, password))
            results = c.fetchall()
            for row in results:
                weight, height = row
        conn.commit()
        return (weight, height)
    def get_activity():
        c.execute("SELECT activity FROM users WHERE username = ? AND password = ? AND activity IS NULL", (name, password))
        results = c.fetchall()
        if len(results) > 0:
            print("1.sedentary, 2.moderately active, 3.very active")
            print("Select a number please.")
            activity_level = int(input("What is your activity level: "))
            c.execute("UPDATE users SET activity = ? WHERE username = ? AND password = ?", (activity_level, name, password))
            # c.execute("INSERT INTO users (activity) VALUES (?)", (activity_level))
            if activity_level == 1 or activity_level == 2 or activity_level == 3:
                pass
            else:
                os.system("cls")
                print("Invalid choice!")
                fitness()
        else:
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (name, password))
            results = c.fetchall()
            for row in results:
                activity_level = row[6]
        conn.commit()
        return activity_level
    def get_gender(): 
        c.execute("SELECT gender FROM users WHERE username = ? AND password = ? AND gender IS NULL", (name, password))
        results = c.fetchall()
        if len(results) > 0:
            print("male, female")
            gender = str(input("What is your Gender: "))
            # c.execute("INSERT INTO users (gender) VALUES (?)", (gender))
            if gender == "male" or gender == "female":
                pass
            else:
                os.system("cls")
                print("Invalid choice!")
                fitness()
            c.execute("UPDATE users SET gender = ? WHERE username = ? AND password = ?", (gender, name, password))
        else:
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (name, password))
            results = c.fetchall()
            for row in results:
                gender = row[5]
        conn.commit()
        return gender
    def get_path(): 
        c.execute("SELECT path FROM users WHERE username = ? AND password = ? AND path IS NULL", (name, password))
        results = c.fetchall()
        if len(results) > 0:
            # IF EMPTY
            path = str(input("What is your xlsx file path: "))
            # c.execute("INSERT INTO users (gender) VALUES (?)", (gender))
            if os.path.isfile(path):
                pass
            else:
                os.system("cls")
                print("Invalid choice!")
                fitness()
            c.execute("UPDATE users SET path = ? WHERE username = ? AND password = ?", (path, name, password))
        # IF NOT EMPTY
        else:
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (name, password))
            results = c.fetchall()
            for row in results:
                path = row[4]
        conn.commit()
        return path
    
    def myPlan():
        import win32com.client as win32
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        path = get_path()
        wop = r"{}".format(path)
        excel.Workbooks.Open(f'{wop}')
        excel.Visible = True
    def bmi_calc():    
        try:
            weight, height = get_weight_height()
            bmi = weight/height**2
            print(bmi)
        except:
            print("Invalid Value")
            fitness()
    def protein_calc():
        # try:
        activity_level = get_activity()
        weight_kg, height = get_weight_height()
        gender = get_gender()
        
        # except:
            # print("Invalid Syntax!")
            # fitness()
        # Determine protein intake based on gender, activity level, and BMI
        if gender == "male":
            if activity_level == 1:
                protein_intake = weight_kg * 0.8
            elif activity_level == 2:
                protein_intake = weight_kg * 1
            elif activity_level == 3:
                protein_intake = weight_kg * 1.2
            else:
                protein_intake = "Invalid activity level"
        elif gender == "female":
            if activity_level == 1:
                protein_intake = weight_kg * 0.6
            elif activity_level == 2:
                protein_intake = weight_kg * 0.8
            elif activity_level == 3:
                protein_intake = weight_kg * 1
            else:
                protein_intake = "Invalid activity level"
        else:
            os.system("cls")
            print("Invalid Gender")
            print(gender)
            fitness()
        print("The number of grams of protein you should get is " + str(protein_intake))
        fitness()

    print("bmi_calc, protein_calc, myPlan")
    print("Write \"led\" to go back")
    while True:
        usr_cmd = input("Select one of the above: ")
        if usr_cmd == "led":
            main()
        elif(usr_cmd == "bmi_calc" or usr_cmd == "bc"):
            bmi_calc()
        elif(usr_cmd == "protein_calc" or usr_cmd == "pc"):
            protein_calc()
        elif(usr_cmd == "myPlan" or usr_cmd == "mp" or usr_cmd == "myplan"):
            myPlan()

def ytdownloader():

    url = str(input("Enter th URL: "))
    my_video = YouTube(url)

    print("*********************VIDEO TITLE************************")
    print(my_video.title)

    print("********************THUMBNAIL IMAGE***********************")
    print(my_video.thumbnail_url)

    #set stream resolution
    my_video = my_video.streams.get_highest_resolution()

    #or
    #my_video = my_video.streams.first()

    #Download video
    my_video.download()

def mypc():
    print("Type one of the following commands: restart, hibernate, shutdown.")
    print("Write \"led\" to go back")
    while True:
        pcc = input("Computer: ")

        if(pcc == "restart"):
            yesNo = str(input("Are you sure ?, Write \"yes\" or \"no\": "))
            if (yesNo == "yes"):
                print("Your pc will restart in: ")
                countdown(3)
                os.system("shutdown /r /t 0")
            elif (yesNo == "no"):
                print("Ok :)")
            else:
                print("Invalid Selection")
        elif(pcc == "shutdown"):
            yesNo = str(input("Are you sure ?, Write \"yes\" or \"no\": "))
            if (yesNo == "yes"):
                print("Your pc will shutdown in: ")
                countdown(3)
                os.system("shutdown /s /t 0")
        elif(pcc == "sleep"):
            yesNo = str(input("Are you sure ?, Write \"yes\" or \"no\": "))
            if (yesNo == "yes"):
                print("Your pc will hibernate in: ")
                countdown(3)
                os.system("shutdown /h /t 0")
            elif (yesNo == "no"):
                print("Ok :)")
            else:
                print("Invalid Selection")
        elif(pcc == "led"):
            main()

def calc():
    # while True:
    #     x = input("Enter expression: ")
    #     print(eval(x))
    #     if x == "exit":
    #         main()
    try:
        op = str(input("Enter one of the following operators: +, -, /, *, %, sin, cos: "))


        # if (op == "sin"):
        #     sin_number = float(input("Enter a number: "))
        #     print(math.sin(sin_number))
        #     main()
        # if (op == "cos"):
        #     cos_number = float(input("Enter a number: "))
        #     print(math.sin(cos_number))
        #     main()
        fn = float(input("Enter the first number: "))
        sn = float(input("Enter the second number: "))
        if (op == "+"):
            print(fn + sn)
        elif (op == "-"):
            print(fn - sn)
        elif (op == "/"):
            print(fn / sn)
        elif (op == "*"):
            print(fn * sn)
        elif (op == "%"):
            print(fn % sn)
        else:
            print("Invalid Operator")
            main()
    except:
        print("An error occurred")
        main()
    
def countdown(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1

def help():
    print("")
    print("calc --> simple calculator")
    print("quit --> exits the program")
    print("cls  --> clears the screen")
    print("cmd  --> lets you run cmd commands")
    print("date --> displays the current date")
    print("my pc--> shows pc options")
    print("passGen --> simple password generator")
    print("weather --> displays the current weather")
    print("ytdownloader --> downloads youtube videos")
    print("fitness --> Opens fitness panel")
    print("help --> for help\n")

main()