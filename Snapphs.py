#import tools
import base64 #decoding 
import os 
import sqlite3 #database module
import requests
from dotenv import load_dotenv
#load environment variables
load_dotenv()

#github cconnection
token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("GITHUB_REPO")

#authorization
headers = {"Authorization" : f"Bearer {token}",
           "Accept" : "application/vnd.github+json"}

#database location
url = f"https://api.github.com/repos/{repo}/contents/snapphs.db"

#download database from github
def download_database():
      response = requests.get(url, headers = headers)
      if response.status_code == 200:
            content = response.json()["content"]
            decoded_content = base64.b64decode(content)

            with open("snapphs.db", "wb") as file:
               file.write(decoded_content)

            print("Latest database downloaded successfully.")
      else:
            print("Download failed:", response.status_code, response.text)
            raise SystemExit("Stopping to protect the local database.")

#download latest database before connecting
download_database()



#upload database to github
def upload_database():
      response = requests.get(url, headers = headers)
      if response.status_code == 200:
            file_sha = response.json()["sha"]
            print("Database found on GitHub.")
      else :
            print("Error:", response.status_code, response.text) 
            return

      with open("snapphs.db", "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")

      data = {"message" : "Update birthday database",
               "content" : content,
               "sha" : file_sha}
      upload_response = requests.put(url, headers = headers, json = data)

      if upload_response.status_code == 200:
            print("Database uploaded successfully.")
      else:
            print("Upload failed:", upload_response.text)

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
    upload_database()
#call eg. delete_friend("Toji")

#update function
def update_email(name, new_email1, new_email2):
    cursor.execute("""UPDATE birthdays SET email_ID1 = ?, email_ID2 = ? WHERE name = ?""",
                   (new_email1, new_email2,name))
    connection.commit()
    upload_database()
#call eg. update_email("Toji","new_email1@gmai.com","new_email2@gmail.com")

#select function
def get_all_friends(): #retrieving info
    cursor.execute("SELECT * FROM birthdays")
    friends = cursor.fetchall()
    return friends

#add function
def add_friends():
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
        upload_database()

#display function
def display_friends():
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

def main():
      while True:
          print("Welcome to Snapphs!")
          print("1. Add friends")
          print("2. Display friends")
          print("3. Update email")
          print("4. Delete friend")
          print("5. Exit")

          choice = input("Choose an option: ")
          if  choice == "1":
              add_friends()
          elif choice == "2":
              display_friends()
          elif choice == "3":
              name = input("Enter your friend's name: ")
              new_email1 = input("Enter new receiver email: ")
              new_email2 = input("Enter new sender email: ")
              update_email(name, new_email1, new_email2)
          elif choice == "4":
              name = input("Enter your friend's name: ")
              delete_friend(name)
          elif choice == "5":
              print("Goodbye!")
              break
      else:
              print("Invalid choice!")
           


if __name__ == "__main__":
        main()