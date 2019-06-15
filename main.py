from pypresence import Presence
import time
import pylast
import os
from tkinter import *
from tkinter import messagebox
import webbrowser
from shutil import copyfile
from tkinter import filedialog

argu = sys.argv
print(argu)

if "--debug" in argu:
    debug=1
else:
    debug=0

root = Tk()
root.title('Discord listening')

clnt1 = StringVar()
api1 = StringVar()
api2 = StringVar()
uname = StringVar()

def discordpai():
    webbrowser.open("https://discordapp.com/developers/applications/")
def lastfmapi():
    webbrowser.open("https://last.fm/api")
def importold():
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select settings file",filetypes = (("Discord Listening Settings File","*stg"),("Old version's settings file","*.*")))
    check = open(root.filename)
    text = check.read().strip().split()
    print(len(text))
    if len(text)!=4:
        messagebox.showerror("Error!", "Settings file has too less or too many options!")
    else:
        copyfile(root.filename, "settings.stg")
        messagebox.showinfo("Settings file imported and checked!", "Please restart this program for it to take effect!")

def getvalue():

    if clnt1.get() == "":
        messagebox.showerror("Error!", "Make sure to fill in the client ID! You can get it by going to the Menubar - Get APIs - Discord Client ID")
        if debug==1:
            print("DEBUG: clnt1 wasn't defined!")
    elif api2.get() == "":
        if debug==1:
            print("DEBUG: api2 wasn't defined!")
        messagebox.showerror("Error!", "Make sure to fill in the last.fm Secret API key! You can get it by going to the Menubar - Get APIs - last.fm API")
    elif api1.get() == "":
        if debug==1:
            print("DEBUG: api1 wasn't defined!")
        messagebox.showerror("Error!", "Make sure to fill in the last.fm API Key! You can get it by going to the Menubar - Get APIs - last.fm API")
    elif uname.get() == "":
        if debug==1:
            print("DEBUG: uname wasn't defined!")
        messagebox.showerror("Error!", "Make sure to fill in the last.fm Username! You can get it by going to the Menubar - Get APIs - last.fm API")
    else:
        if debug==1:
            print("DEBUG: ClientID is" + clnt1.get())
            print("DEBUG: API KEY is" + api1.get())
            print("DEBUG: SECRET API KEY is" + api2.get())
            print("DEBUG: USERNAME is" + uname.get())
            print("DEBUG: Opening settings file...")
        try:
            filewrite = open("settings.stg", "w+")
            if debug==1:
                print("DEBUG: Writing Client ID to line 1")
            filewrite.write(clnt1.get() + "\r\n")
            if debug==1:
                print("DEBUG: Writing API KEY to line 3")
            filewrite.write(api1.get() + "\r\n")
            if debug==1:
                print("DEBUG: Writing SECRET API KEY to line 5")
            filewrite.write(api2.get() + "\r\n")
            if debug==1:
                print("DEBUG: Writing Username to line 7")
            filewrite.write(uname.get() + "\r\n")
            if debug==1:
                print("DEBUG: DONE! Closing file.")
            filewrite.close()
            root.destroy()
        except Exception:
            print("ERROR: Saving failed! Please create a new issue with the output of the console!")


def getvaluetest():
    if clnt1.get() == "":
        messagebox.showerror("Error!", "Make sure to fill in the client ID! You can get it by going to the Menubar - Get APIs - Discord Client ID")
        if debug==1:
            print("DEBUG: clnt1 wasn't defined!")
    elif api2.get() == "":
        if debug==1:
            print("DEBUG: api2 wasn't defined!")
        messagebox.showerror("Error!", "Make sure to fill in the last.fm Secret API key! You can get it by going to the Menubar - Get APIs - last.fm API")
    elif api1.get() == "":
        if debug==1:
            print("DEBUG: api1 wasn't defined!")
        messagebox.showerror("Error!", "Make sure to fill in the last.fm API Key! You can get it by going to the Menubar - Get APIs - last.fm API")
    elif uname.get() == "":
        if debug==1:
            print("DEBUG: uname wasn't defined!")
        messagebox.showerror("Error!", "Make sure to fill in the last.fm Username! You can get it by going to the Menubar - Get APIs - last.fm API")
    else:
        network = pylast.LastFMNetwork(api1.get())
        user = network.get_user(uname.get())
        messagebox.showinfo("Discord - playing Music", "\n\nPlaying {}.".format(user.get_now_playing()))

def thestart(client_id, API_KEY, API_SECRET, user):
    network = pylast.LastFMNetwork(API_KEY)
    user = network.get_user(user)
    RPC = Presence(client_id)
    RPC.connect() # Start the handshake loop
    RPC.update(state="Playing some music.") # Initialize the message. Will get replaced very shortly.


    while True:  # The presence will stay on as long as the program is running
        nowplaying = user.get_now_playing()
        nowplaying = str(nowplaying)
        if debug==1:
            print("DEBUG: User is playing " + nowplaying + "!")
        RPC.update(state="Playing " + nowplaying + ".")
        if debug==1:
            print("DEBUG: Updated the status!\nDEBUG: Sleeping one sec...")
        time.sleep(1)


config = os.path.exists('./settings.stg')
if config:
    fobj = open("settings.stg")
    text = fobj.read().strip().split()
    # Conditions
    print("The ClientID is {}, the API key is {} and the secret API key is {}!".format(text[0], text[1], text[2]))
    client_id = text[0]
    API_KEY = text[1]
    API_SECRET = text[2]
    user=text[3]
    if debug==1:
            print("DEBUG: ClientID is" + client_id)
            print("DEBUG: API KEY is" + API_KEY)
            print("DEBUG: SECRET API KEY is" + API_SECRET)
            print("DEBUG: USERNAME is" + user)
    thestart(client_id, API_KEY, API_SECRET, user)

else:

    Label(root, text="ClientID").grid(row=0, sticky=W)  # label
    Entry(root, textvariable=clnt1).grid(row=0, column=1, sticky=E)  # entry textbox
    Label(root, text="last.fm API").grid(row=1, sticky=W)  # label
    Entry(root, textvariable=api1).grid(row=1, column=1, sticky=E)  # entry textbox
    Label(root, text="last.fm SECRET API").grid(row=2, sticky=W)  # label
    Entry(root, textvariable=api2).grid(row=2, column=1, sticky=E)  # entry textbox
    Label(root, text="last.fm Username").grid(row=3, sticky=W)  # label
    Entry(root, textvariable=uname).grid(row=3, column=1, sticky=E)  # entry textbox

    SaveButton = Button(root, text="Save settings", command=getvalue).grid(row=4, column=0, sticky=W)  # button
    PreviewButton = Button(root, text="Preview / Test", command=getvaluetest).grid(row=4, column=1, sticky=W)  # button

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Import old config file", command=importold)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    apimenu = Menu(menubar, tearoff=0)
    apimenu.add_command(label="Discord Client ID", command=discordpai)
    apimenu.add_command(label="last.fm API", command=lastfmapi)
    menubar.add_cascade(label="Get APIs", menu=apimenu)
    root.config(menu=menubar)
    root.resizable(0, 0)
    root.mainloop()

    client_id = clnt1.get()
    API_KEY = api1.get()
    API_SECRET = api2.get()
    user = uname.get()
    thestart(client_id, API_KEY, API_SECRET, user)

