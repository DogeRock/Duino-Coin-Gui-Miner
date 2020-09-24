#!/usr/bin/python3

from tkinter import * # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from tkinter import messagebox
top = Tk()
top.configure(background="#7d796e")
top.geometry("500x500")
top.title("DogeRock Duino-Coin Miner")
L1 = Label(top, text = "User Name")
L1.place(x = 1,y = 200)
L2 = Label(top, text = "Password")
L2.place(x = 1,y = 250)
E1 = Entry(top, bd = 5)
E1.place(x = 200,y = 200)
E2 = Entry(top, bd = 5)
E2.config(show="•");
E2.place(x = 200,y = 250)

def helloCallBack():
   import socket, hashlib, os, urllib.request # Only python3 included libraries
   soc = socket.socket()
   username = E1.get()
   password = E2.get()
   # This sections grabs pool adress and port from Duino-Coin GitHub file
   serverip = "https://raw.githubusercontent.com/revoxhere/duino-coin/gh-pages/serverip.txt" 
   with urllib.request.urlopen(serverip) as content:
       content = content.read().decode().splitlines() #Read content and split into lines
   pool_address = content[0] #Line 1 = pool address
   pool_port = content[1] #Line 2 = pool port

   # This section connects and logs user to the server
   soc.connect((str(pool_address), int(pool_port))) # Connect to the server
   server_version = soc.recv(3).decode() # Get server version
   print("Server is on version", server_version)

   soc.send(bytes("LOGI," + username + "," + password, encoding="utf8")) # Send login data
   response = soc.recv(2).decode() # Get server feedback about logging in                
   if response == "OK":
       print("Logged in")
   else:
       print("Error loging in - check account credentials!")
       soc.close()
       os._exit(1)

   # Mining section
   while True:
       soc.send(bytes("JOB", encoding="utf8")) # Send job request
       job = soc.recv(1024).decode() # Get work from pool
       job = job.split(",") # Split received data to job (job and difficulty)
       difficulty = job[2]

       for result in range(100 * int(difficulty) + 1): # Calculate hash with difficulty
           ducos1 = hashlib.sha1(str(job[0] + str(result)).encode("utf-8")).hexdigest() # Generate hash
           if job[1] == ducos1: # If result is even with job
               soc.send(bytes(str(result), encoding="utf8")) # Send result of hashing algorithm to pool
               feedback = soc.recv(1024).decode() # Get feedback about the result
               if feedback == "GOOD": # If result was good
                   print("Accepted share", result, "Difficulty", difficulty)
                   break
               elif feedback == "BAD": # If result was bad
                   print("Rejected share", result, "Difficulty", difficulty)
                   break

B = Button(top, text = "Mine", command = helloCallBack)
B.place(x = 200,y = 350)
top.mainloop()
