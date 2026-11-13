#import tools
import sys #reading arguments
import os #hiding password
from dotenv import load_dotenv
load_dotenv()  
import sqlite3 #database module
import smtplib #email module_simple mail transfer protocol 
from email.message import EmailMessage #define email
from datetime import datetime #date & time module
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
app_pass = os.getenv("GMAIL_APP_PASSWORD")
server.login(email, app_pass)

#checking birthday function
def check_birthdays():
        saved_friends = get_all_friends()
        local_now = datetime.now(ZoneInfo("Asia/Dhaka"))
        today = local_now.date()
        current_time = local_now.strftime("%H:%M")

        for friend in saved_friends: #to check date & time
                  birthday_date = datetime.strptime(friend["birthday"],"%d %B") #convert to dd/mm format
                  if today.day == birthday_date.day and today.month == birthday_date.month and current_time >= friend["send_time"]  and friend["last_sent_year"] != today.year:
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

                           #stopping repetition
                           cursor.execute("UPDATE birthdays SET last_sent_year = ? WHERE name = ?",
                           (today.year, friend["name"]))
                           connection.commit()
                                    
        server.quit()

if __name__ == "__main__":
        check_birthdays()
        