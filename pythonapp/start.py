import os
from openai import OpenAI
from tkinter import *
from googlesearch import search
import requests
import webbrowser
import pywinctl as pwc
import wmi
import psutil
import subprocess
import time
from pywinauto import Application
from dotenv import load_dotenv
from customtkinter import *

import importlib

import pathlib

#os.system("cmd /k")

pluginpath = os.path.dirname(__file__)
pluginpath = pluginpath + "/plugins/"
homepath = os.path.dirname(__file__)

f = open(r"D:\pythonapp\pluginpath.txt", "w")
f.write(pluginpath)
f.close()

plugins = []
pluginlist = []

for f in pathlib.Path(pluginpath).iterdir():
    read = str(f)
    if read[-3:] == ".py":
        plugin = str(f)
        plugin = plugin[:-3]
        apd = importlib.import_module("plugins." + plugin[21:])
        pluginlist.append(apd)
        print("added plugin: " + plugin[21:])
        plugins.append(plugin[21:])





w = wmi.WMI()

mode = 1

app=CTk()

app.title("__________________---------SINGULARITY---------____________________")

app.geometry('400x500')

webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(r"C:\Users\Addy\AppData\Local\Google\Chrome\Application\chrome.exe"))

#frame.Frame(bg="blue")

#frame = LabelFrame(frame, text="frame", padx=5,pady=5)
#frame.pack(padx=10,pady=10)


client = OpenAI(
    # This is the default and can be omitted
    api_key=""
)


def clicked():
    a=""
    Sorter(a)


def Sorter(self):
    print("sorting...")
    askbot=messagebotwindow.get(1.0,"end-1c")
    askbot = askbot + " "
    if askbot != " ":
        print(repr(askbot))
        askbot = askbot.rstrip()
        askbot = askbot + " "
        print(repr(askbot))
    #askbot = askbot.rstrip()
    indexofmsg = askbot.index(" ")
    print(indexofmsg)
    print(askbot[:indexofmsg])
    messagebotwindow.delete(1.0,END)

    if str(askbot[:6]) == "error ":                     #search stack overflow for error answers


        searchq = list(search(askbot + " stack overflow", tld="co.in", num=10, stop=10, pause=2))
        URL = searchq[0] 
        webbrowser.open(URL, new= 2)
    elif str(askbot[:6]) == "erroru":                   #search youtube for answers


        URL = "https://www.youtube.com/results?search_query=" + askbot[6:] + " programming"
        webbrowser.open(URL, new= 2)
    elif str(askbot[:3]) == "cmd":                      #start cmd


        os.system("start cmd")
    elif str(askbot[:4]) == "save":                     #save current apps to restore using mode(1-9)


        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Path'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        f = open(r"D:\pythonapp\mode"+str(mode)+".txt", "w")
        f.write("")
        f.close()

        for line in proc.stdout:
            if not line.decode()[0].isspace():
                x = line.decode().rstrip()
                if("chrome.exe" in x):
                    app = Application(backend='uia')
                    app.connect(title_re=".*Chrome.*")
                    element_name="Address and search bar"
                    dlg = app.top_window()
                    savebrowseurl = dlg.child_window(title=element_name, control_type="Edit").get_value()
                    f = open(r"D:\pythonapp\mode"+str(mode)+".txt", "a")
                    f.write("url: " + savebrowseurl + "\n")
                    f.close()
                else:
                    f = open(r"D:\pythonapp\mode"+str(mode)+".txt", "a")
                    f.write('"" "'+ x + '"\n')
        f.close()
        f = open(r"D:\pythonapp\mode"+str(mode)+".txt", "r")
        print(f.read())
    elif str(askbot[:4]) == "clsx":                         #kill all tasks
        os.system(r'TASKKILL /FI "USERNAME ne NT AUTHORITY\SYSTEM" /FI "IMAGENAME ne sublime_text.exe"  /FI "IMAGENAME ne python.exe" /FI "IMAGENAME ne conhost.exe" /FI "IMAGENAME ne py.exe" /FI "IMAGENAME ne powershell.exe" /IM *' )
    elif str(askbot[:5]) == "mode1":                        #mode 1


        os.system(r'TASKKILL /FI "USERNAME ne NT AUTHORITY\SYSTEM"  /FI "IMAGENAME ne python.exe" /FI "IMAGENAME ne conhost.exe" /FI "IMAGENAME ne py.exe" /IM *' )
        time.sleep(2)
        f = open(r"D:\pythonapp\mode1.txt", "r")

        f.readline()
        f.readline()

        for line in f:
            if "url" in str(line):
                URL = str(line)
                webbrowser.get('chrome').open(URL[4:], new= 2)
            else:
                os.system("start "  + str(line))
    elif str(askbot[:5]) == "mode2":                        #mode 2



        os.system(r'TASKKILL /IM chrome.exe' )
        time.sleep(2)
        f = open(r"D:\pythonapp\mode2.txt", "r")

        f.readline()
        f.readline()

        for line in f:
            if "chrome.exe" in str(line):
                URL = "https://www.reddit.com/"
                webbrowser.open(URL, new= 2)
                webbrowser.open("https://www.youtube.com/", new= 2)
                webbrowser.open("https://www.google.com/", new= 2)
            else:
                os.system("start "  + str(line))
    elif str(askbot[:3]) == "gts":                          #go to shutdown

        os.system("shutdown /s /t 1")

    elif str(askbot[:indexofmsg]) in plugins:
        pluginindex = plugins.index(str(askbot[:indexofmsg]))                               # use plugins
        pluginlist[pluginindex].default(chatbotwindow, askbot[indexofmsg:])
    elif str(askbot[:indexofmsg]) == "?":
        print(askbot[:indexofmsg])
        chatbotwindow.insert("end-1c", "commands: ----------------------------------------------"+'\n','warning2')
        chatbotwindow.insert("end-1c", "erroru          open up the error after it in stackoverflow"+'\n','warning2')
        chatbotwindow.insert("end-1c", "erroru          open the error after it in youtube"+'\n','warning2')
        chatbotwindow.insert("end-1c", "cmd             open cmd shell"+'\n','warning2')
        chatbotwindow.insert("end-1c", "save            save current applications (to open with mode1 or mode2)"+'\n','warning2')
        chatbotwindow.insert("end-1c", "clsx            kill all tasks"+'\n','warning2')
        chatbotwindow.insert("end-1c", "mode1-2         enter:mode1 or mode2"+'\n','warning2')
        chatbotwindow.insert("end-1c", "gts             it shutsdown in 1 second"+'\n','warning2')
        chatbotwindow.insert("end-1c", "plugins ------------------------------------------------"+'\n','warning2')
        for i in range(len(plugins)):
            chatbotwindow.insert("end-1c", plugins[i]+'\n','warning2')

    else:                                                                               #chat bot
        botToReply(askbot)

        

def botToReply(askbot):                                                                 #bot reply mode
    chatbotwindow.tag_config('warning2', foreground="red", justify='left')
    chatbotwindow.tag_config('warning', foreground="blue", justify='left')
    chatbotwindow.tag_config('warning1', foreground="black", justify='right')
    messages = {"role": "user","content": askbot}
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": askbot,
        }
    ],
    model="gpt-3.5-turbo",
)
    reply = chat_completion.choices[0].message.content
    print("ChatGPT: {reply}")
    chatbotwindow.insert("end-1c", askbot+'\n','warning1')
    chatbotwindow.insert("end-1c", reply+'\n','warning')



frame1 = CTkFrame(master=app, fg_color="grey", border_color="grey",height = 800 , border_width=2, corner_radius=16)
frame1.pack(expand = True, padx = 20, pady = 10,ipadx = 20, ipady = 80, anchor="s", fill="both")

frame2 = CTkFrame(master=app, fg_color="black", border_color="black",height = 800 , border_width=2, corner_radius=16)
frame2.pack(expand = True, padx = 20, pady = 10, anchor="s", fill="both")

#chat window

chatbotwindow=CTkTextbox(master=frame1,fg_color="white",text_color = "black",wrap="word",corner_radius=16)
chatbotwindow.pack(expand=True, padx = 0, pady = 0, anchor="n", fill="both")

#message window

#button

botbutton=CTkButton(master=frame2,text='askbot',fg_color='grey',corner_radius=32,bg_color="black",hover_color="white",command=clicked)
botbutton.pack(padx = 15, pady = 0, anchor="sw", side="left", fill ="y")

messagebotwindow=CTkTextbox(master=frame2,fg_color="white",bg_color="black", text_color = "black",corner_radius=16)
messagebotwindow.pack(expand=True, ipadx = 10, ipady = 0, anchor="s", side="left", fill = "both")

chatbotwindow.insert("end-1c", "Press '?'' for a list of commands else type for ChatGPT"+'\n','warning1')

app.bind('<Return>', Sorter)


app.mainloop()

'''chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)
print(chat_completion.choices[0].message.content)
print(dict(chat_completion).get('usage'))'''

