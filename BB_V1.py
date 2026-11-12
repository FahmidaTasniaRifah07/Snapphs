from datetime import date,datetime #datetime module
friends = [] #friend list

number = int(input("How many friends?\n= ")); #no of friends

for i in range(number): #for running n times
    name = input("Enter your friend's name : ")
    birthday = input("Enter your friend's birthday : ")
    email_ID = input("Enter your friend's email ID : ")
    custom_text = input("Write your own customized text : ")
    friend = {"name" : name, "birthday" : birthday, "email_ID" : email_ID, "custom_text" : custom_text} #dictionary to store friends' info
    friends.append(friend) #to add in the friends' list
for friend in friends: #for display
    print("Name : " + friend["name"])
    print("Birthday : " + friend["birthday"])
    print("Email_ID : " + friend["email_ID"])
    print("Message : " + friend["custom_text"])
today = date.today() #today's date
for friend in friends: #to check date
     birthday_date = datetime.strptime(friend["birthday"],"%d %B") #convert to dd/mm format
     if today.day == birthday_date.day and today.month == birthday_date.month:
         print("It's " +friend["name"] + "'s birthday." )
         print("Message Sent : " + friend["custom_text"])