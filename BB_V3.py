#import tools
import os #hiding password
from dotenv import load_dotenv
load_dotenv()  
import sqlite3 #database module
import smtplib #email module_simple mail transfer protocol 
from email.message import EmailMessage #define email
from datetime import date,datetime #date & time module
from zoneinfo import ZoneInfo #zone module

#connect to database
connection = sqlite3.connect("snapphs.db") #creating connection
connection.row_factory = sqlite3.Row #giving dictionary-like access
cursor = connection.cursor() #giving command to SQL_Structured Query Language
cursor.execute(""" CREATE TABLE IF NOT EXISTS birthdays  
               (name TEXT,
               birthday TEXT, 
               send_time TEXT, 
               email_ID1 TEXT,
               email_ID2 TEXT,
               subject TEXT,
               custom_text TEXT,
               last_sent_year INTEGER DEFAULT 0)""")
#error prevention for table already existinng 
#for multiple string """
connection.commit() #saving changes

#delete function
def delete_friend(name): #deleting the row
    cursor.execute("DELETE FROM birthdays WHERE name = ?", (name,))
    connection.commit()
#call eg. delete_friend("Toji")

#update function
def update_email(name, new_email1, new_email2):
    cursor.execute("""UPDATE birthdays SET email_ID1 = ?, email_ID2 = ? WHERE name = ?""",
                   (name, new_email1, new_email2))
    connection.commit()
#call eg. update_email("Toji","new_email1@gmai.com","new_email2@gmail.com")

#select function
def get_all_friends(): #retrieving info
    cursor.execute("SELECT * FROM birthdays")
    friends = cursor.fetchall()
    return friends

#connect to email
server = smtplib.SMTP("smtp.gmail.com", 587) #initial connection
server.ehlo() #client to gmail introduction
server.starttls() #activate encryption
server.ehlo() #introduce again
email = os.getenv("GMAIL_ADDRESS") #retrieving info from env file
app_pass = os.getenv("GMAIL_APP_PASSWROD")
server.login(email, app_pass)


friends = [] #friend list
number = int(input("How many friends?\n= ")); #no of friends


for i in range(number): #for running n times
    name = input("Enter your friend's name : ")
    birthday = input("Enter your friend's birthday (eg. 1 January) : ")
    send_time = input("Enter the sending time[use 24hr format(eg. HH:MM)] : ")
    email_ID1 = input("Enter your friend's email ID : ")
    email_ID2 = input("Enter your email ID : ")
    subject = input("Enter the subject of email: ")
    custom_text = input("Write your own customized text : ")
    friend = {"name" : name, "birthday" : birthday, "send_time" : send_time, "email_ID1" : email_ID1, "email_ID2" : email_ID2, "subject" : subject, "custom_text" : custom_text, "last_sent_year" : 0} #dictionary to store friends' info
    friends.append(friend) #to add in the friends' list

#transfer info to table from dictionary
for friend in friends:
    cursor.execute("""INSERT INTO birthdays
                   (name, birthday, send_time, email_ID1, email_ID2, subject, custom_text, last_sent_year)
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                   (friend["name"],
                    friend["birthday"],
                    friend["send_time"],
                    friend["email_ID1"],
                    friend["email_ID2"],
                    friend["subject"],
                    friend["custom_text"],
                    friend["last_sent_year"]))
    connection.commit()

saved_friends = get_all_friends() #storing info

#for display   
for friend in saved_friends: 
    print("Name : " + friend["name"])
    print("Birthday : " + friend["birthday"])
    print("Send_Time : " + friend["send_time"])
    print("Email_Receiver : " + friend["email_ID1"])
    print("Email_Sender : " + friend["email_ID2"])
    print("Subject : " + friend["subject"])
    print("Message : " + friend["custom_text"])
today = date.today() #today's date

for friend in saved_friends: #to check date & time
     birthday_date = datetime.strptime(friend["birthday"],"%d %B") #convert to dd/mm format
     sending_time = datetime.strptime(friend["send_time"],"%H:%M").time() #convert to HH/MM format
     today1 = datetime.now(ZoneInfo("Asia/Dhaka")) #specifies timezone
     if today.day == birthday_date.day and today.month == birthday_date.month and today1.time() >= sending_time and friend["last_sent_year"] != today.year:
         print("It's " +friend["name"] + "'s birthday." )
         print("Message Sent : " + friend["custom_text"])
         msg = EmailMessage()
         msg["From"] = email
         receiver = friend["email_ID1"]
         msg["To"] = receiver
         msg["Reply-To"] = friend["email_ID2"]
         msg["Subject"] = friend["subject"]
         msg.set_content(friend["custom_text"]) #body
         server.send_message(msg)

         #stopping repetition of msg sent
         cursor.execute("UPDATE birthdays SET last_sent_year = ? WHERE name = ?",
                        (today.year, friend["name"]))
         connection.commit()

         server.quit
