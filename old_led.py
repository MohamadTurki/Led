import datetime
import os
import sys
import time
import random
import sqlite3
import re
# from pytube import YouTube

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
user_is_logged_in = False
guide_str = "Type one of the following (calc, quit, cls, cmd, date, edit_data, myPc, weather, ytDownloader, guessingGame, searchEngine, fitness, help)"
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
def database():

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
            user_is_logged_in = True
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
        
    #Get User id
    c.execute("SELECT rowid FROM users WHERE username = ? AND password = ?", (user.username, user.password))
    id = c.fetchone()
    id = id[0]

    conn.close()
    return (id, user.username, user.password)
        
id, name, password = database()

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
        "fitness": fitness,
        "speak": speak,
        "update_data": update_data,

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
        "search_engine": ["searchEngine","SearchEngine","se"],
        "speak": ["speak", "HeyLed"],
        "update_data": ["update_data", "updatedata", "updateData", "edit_data", "editdata", "editData", "up", "ed"],
    }


    for key, val in aliases.items():
        if cmd in val:
            cmds[key]()
            break

def get_name(in_txt):
    username = input(in_txt)
    while not re.match(r"[A-Za-z]+", username):
        print("Invalid name, please enter a valid name.")
        username = input(in_txt)
    return str(username)

def main():
    try:
        while True:
            cmd = input("Led: ")
            exec_cmd(cmd)
    except KeyboardInterrupt:
        print("\nExiting program...")

def update_data():
    try:
        edited_data_txt = "1. Name, 2. Password, 2. Weight, 3. Height, 4. Path, 5. Gender, 6. Activity level, 7. delete_account"
        print(edited_data_txt)
        print("Write \"led\" to go back.")
        while user_is_logged_in:
            user_selection = str(input("Edit: "))
            if(user_selection == "led"):
                main()
            elif(user_selection == "cls"):
                clear_screen()
                print(edited_data_txt)
            elif(user_selection == "1"):
                new_username = get_name("Enter your new name: ")
                c.execute("UPDATE users SET username = ? WHERE rowid = ?", (new_username, id))
                print("Username has just changed succesfully!")
            elif(user_selection == "2"):
                new_password = input("Enter your new password: ")
                c.execute("UPDATE users SET password = ? WHERE rowid = ?", (new_password, id))
                print("Password has just changed succesfully!")
            elif(user_selection == "3"):
                new_weight = input("Enter your new weight (kg): ")
                c.execute("UPDATE users SET weight = ? WHERE rowid = ?", (new_weight, id))
                print("Weight has just changed succesfully!")
            elif(user_selection == "4"):
                new_height = input("Enter your new height (cm): ")
                c.execute("UPDATE users SET height = ? WHERE rowid = ?", (new_height, id))
                print("Height has just changed succesfully!")  
            elif(user_selection == "5"):
                new_path = input("Enter your new xlsx path: ")
                c.execute("UPDATE users SET path = ? WHERE rowid = ?", (new_path, id))
                print("Workout plan path has just changed succesfully!")  
            elif(user_selection == "6"):
                print("1.sedentary, 2.moderately active, 3.very active")
                print("Select a number please.")
                new_activity_lvl = int(input("Enter your new activity level: "))
                c.execute("UPDATE users SET activity = ? WHERE rowid = ?", (new_activity_lvl, id))
                print("Activity level has just changed succesfully!")
            elif(user_selection == "7"):
                print("Are you sure you want to delete this account?")
                answer = input("Yes/No: ")
                if answer == "Yes":
                    c.execute("DELETE FROM users WHERE rowid = ?", (id,))
                    conn.commit()
                    print("User deleted succefully!")
                    user_is_logged_in = False
                elif answer == "No":
                    clear_screen()
                    print("Ok then!")
                    pass
                else:
                    clear_screen()
                    print("Invalid Choice")
                    print(guide_str)
                    main()
            conn.commit()
    except:
        print("Invalid Error!")

def cmd_func():
    try:
        print("Write \"led\" to go back")
        while True:
            usr_cmd = str(input("Enter cmd commands: "))
            if(usr_cmd == "led"):
                main()
            os.system(usr_cmd)
    except KeyboardInterrupt:
        print("Exiting program...")

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

def speak():
    import speech_recognition as sr
    import pyttsx3
    
    # Initialize the recognizer
    r = sr.Recognizer()

    # Function to convert text to
    # speech
    def SpeakText(command):
        
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()
    while(1):
        
        # Exception handling to handle
        # exceptions at the runtime
        try:
            
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                #listens for the user's input
                audio2 = r.listen(source2)
                
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print("Did you say: ",MyText)
                if MyText == "show me the weather":
                    speak_text = "Ok! {}".format(name)
                    SpeakText(speak_text)
                    weather()
                elif MyText == "show me the date":
                    SpeakText(datetime.datetime.now().date())
                elif MyText == "hello led":
                    speak_text = "hello {}".format(name)
                    SpeakText(speak_text)
                    
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred")

def date():
    print(datetime.datetime.now().date())

def weather():
    os.system("curl wttr.in")

def clear_screen():
    os.system("cls")

def byebye():
    clear_screen()
    print("Bye Bye!")
    sys.exit()

def search_engine():
    clear_screen()
    print("Write \"led\" to go back")
    while True:
        src = input("Search anything: ")
        search = src.replace(" ", "%20")
        if(src == ""):
            search_engine()
        elif(src == "led"):
            clear_screen()
            print(guide_str)
            main()
        else:
            search_cmd = "start https://duckduckgo.com/?q={}".format(search)
            os.system(search_cmd)    

def fitness():
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
                clear_screen()
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
                clear_screen()
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
            if os.path.isfile(path):
                pass
            else:
                clear_screen()
                print("Invalid choice!")
                fitness()
            c.execute("UPDATE users SET path = ? WHERE username = ? AND password = ?", (path, name, password))
        # IF NOT EMPTY
        else:
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (name, password))
            results = c.fetchall()
            for row in results:
                path = row[3]
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
            clear_screen()
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
    print("calc         --> Simple calculator")
    print("quit         --> Exits the program")
    print("cls          --> Clears the screen")
    print("cmd          --> Lets you run cmd commands")
    print("date         --> Displays the current date")
    print("my pc        --> Shows pc options")
    print("passGen      --> Simple password generator")
    print("weather      --> Displays the current weather")
    print("ytdownloader --> Downloads youtube videos")
    print("fitness      --> Opens fitness panel")
    print("edit_data    --> Edit/Updates user's personal data")
    print("help         --> For help\n")

main()