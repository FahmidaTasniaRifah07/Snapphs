import smtplib #email module_simple mail transfer protocol 
from email.message import EmailMessage #define email
from datetime import date,datetime #date & time module
from zoneinfo import ZoneInfo #zone module

server = smtplib.SMTP("smtp.gmail.com", 587) #initial connection
server.ehlo() #client to gmail introduction
server.starttls() #activate encryption
server.ehlo() #introduce again
email = "snapphs026@gmail.com"
app_pass = "mwgq rjgu iemj fdsp"
server.login(email, app_pass)


friends = [] #friend list
number = int(input("How many friends?\n= ")); #no of friends


for i in range(number): #for running n times
    name = input("Enter your friend's name : ")
    birthday = input("Enter your friend's birthday (eg. 1 January) : ")
    send_time = input("Enter your sending time[use 24hr format(eg. HH:MM)] : ")
    email_ID1 = input("Enter your friend's email ID : ")
    email_ID2 = input("Enter your email ID : ")
    custom_text = input("Write your own customized text : ")
    friend = {"name" : name, "birthday" : birthday, "send_time" : send_time, "email_ID1" : email_ID1, "email_ID2" :email_ID2, "custom_text" : custom_text} #dictionary to store friends' info
    friends.append(friend) #to add in the friends' list
for friend in friends: #for display
    print("Name : " + friend["name"])
    print("Birthday : " + friend["birthday"])
    print("Send_Time : " + friend["send_time"])
    print("Email_Receiver : " + friend["email_ID1"])
    print("Email_Sender : " + friend["email_ID2"])
    print("Message : " + friend["custom_text"])
today = date.today() #today's date
for friend in friends: #to check date & time
     birthday_date = datetime.strptime(friend["birthday"],"%d %B") #convert to dd/mm format
     sending_time = datetime.strptime(friend["send_time"],"%H:%M").time() #convert to HH/MM format
     today1 = datetime.now(ZoneInfo("Asia/Dhaka")) #specifies timezone
     if today.day == birthday_date.day and today.month == birthday_date.month and today1.time() >= sending_time:
         print("It's " +friend["name"] + "'s birthday." )
         print("Message Sent : " + friend["custom_text"])
         msg = EmailMessage()
         msg["From"] = email
         receiver = friend["email_ID1"]
         msg["To"] = receiver
         msg["Reply-To"] = friend["email_ID2"]
         msg.set_content(friend["custom_text"]) #body
         server.send_message(msg)
         server.quit