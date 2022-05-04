"""
Script Version: v0.1
Author: leifadev

This script applies too all versions of Scout v1.5.1 and under,
to automatically install FFmpeg for Scout AND the system!

This script installs FFmpeg and directs the path to: ... <<---------- FILL IN HERE
This script will be compiled and shipped out directly as such.


NOTE: Make an options available local path and system-wide path

"""

from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from ttkthemes import ThemedTk # dark mode theme and stuff
import webbrowser, getpass, requests, os, time, darkdetect, sys, ssl, logging
from zipfile import ZipFile
import zipfile, threading, queue
from functools import partial


class Window:
    def __init__(self, parent):

        self.localPath = ""
        self.systemPath = ""
        self.permDir = "C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\" # add \\FFmpeg folder later!
        self.tempDir = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Temp\\" # ADD TEMP DIR FROM WINDOWS
        self.icon = ""
        self.version = "v0.1"

        ssl._create_default_https_context = ssl._create_unverified_context

        parent.title("Scout Windows FFmpeg Installer")



        width=450
        height=350
        screenwidth = parent.winfo_screenwidth()
        screenheight = parent.winfo_screenheight()

        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr)
        parent.resizable(width=True, height=True)


        # Download logo icon!
        print("Attemping logo downloading...")
        url = "https://raw.githubusercontent.com/leifadev/scout/main/images/scout_logo_windows_installer.png"

        # Fetch latest ffmpeg build API https://ffbinaries.com/api
        ffmpeg_url = "https://ffbinaries.com/api/v1/version/latest"
        data = requests.get(ffmpeg_url).json()
        self.release_url = data["bin"]["windows-64"]["ffmpeg"]

        self.logfield = tk.Text(parent)

        # Download icon for use if not present
        if not os.path.isfile(self.tempDir + "scout_windows_installer.png"):
            wget.download(url, self.tempDir + "scout_windows_installer.png")
            self.logfield.insert(END, "INFO: Downloaded the app icon!")
        else:
            print("DEBUG: Icon detected!")

        try:
            self.icon = PhotoImage(file=self.tempDir + "scout_windows_installer.png")
            parent.tk.call('wm', 'iconphoto', parent._w, self.icon)
        except Exception as e:
            print(f"DEBUG: WARNING: Tkinter could not apply these app with PhotoImage class!\nIt's found directory should be {self.tempDir}, a temporary directory in Windows 10")
            self.logfield.insert(END, f"WARNING: Icon could not be found or applied to the app!")

        parent.update()   # Updates window at startup to be interactive and lifted


        # Define UI elements
        ft = tkFont.Font(family="Courier", size=7)
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(END, f"Launched successfully!\nVersion: {self.version}\n")
        self.logfield["state"] = "disabled"

        self.progress = ttk.Progressbar(parent, orient = HORIZONTAL,
                      length = 400, mode = 'determinate')

        self.installB=tk.Button(parent)
        self.installB["text"] = "Install"
        self.installB["command"] = self.install


        self.cancelB=tk.Button(parent)
        self.cancelB["text"] = "Cancel"
        self.cancelB["command"] = self.cancel

        # Apply darktheme!
        if darkdetect.isDark():
            parent.set_theme("equilux")
            self.logfield["bg"] = "#e5e5e5"
            self.cancelB["bg"] = "#444444"
            self.installB["bg"] = "#444444"
            self.cancelB["fg"] = "#ffffff"
            self.installB["fg"] = "#ffffff"

        elif darkdetect.isLight():
            print("DEBUG: Light mode detected!")
        else:
            self.logfield.insert(END, "Detected no system theme! Defaulting to light mode")


        ## Gridding ##

        self.installB.pack(side=TOP)
        self.cancelB.pack(side=TOP)
        self.progress.pack(side=BOTTOM, pady=15)
        self.logfield.pack(side=BOTTOM, padx=40, pady=10)


    def bar(self, amount):
        """
        Call to fill progress bar
        """
        laundry_list = [] # lists all things being loaded

        for i in range(0, amount):
            self.progress['value'] = i
            parent.update_idletasks()
            time.sleep(0.000001)



    ## Functions! ##

    def install(self):
        print("Installing function running!!")

        # Bar process first
        os.chdir("C:\\Users\\leif\\Desktop\\")
        print(f"Current working directory isss..... {os.getcwd()}!")

        self.logfield["state"] = "normal"
        self.logfield.insert(END, f"INFO: Downloading FFmpeg!\nSOURCE URL: {self.release_url}\n\n")
        self.logfield["state"] = "disabled"

        def download(root, q):

            response = requests.get(self.release_url, stream=True)
            dl_size = int(response.headers['Content-length'])

            with open("lol", 'wb') as fp:
                for chunk in response.iter_content(chunk_size=1024):
                    fp.write(chunk)
                    q.put(len(chunk) / dl_size * 100)
                    parent.event_generate('<<Progress>>')
                    # logging.debug("Chunk loaded")

            parent.event_generate('<<Done>>')


        def updater(pb, q, event):
            self.progress['value'] += q.get()
            # print("Updating UI bar...")


        q = queue.Queue()
        update_handler = partial(updater, self.progress, q)
        parent.bind('<<Progress>>', update_handler)

        thread = threading.Thread(target=download, args=(parent, q), daemon=True)
        thread.start()


        self.logfield["state"] = "normal"
        self.logfield.insert(END, "\nDownloading latest stable version of ffmpeg, may take at least several seconds!\n")
        print("Downloading latest binary from link! Wait pls")

        # MAKE IT CUSTOM DIR OPTION SOON
        try:
            os.mkdir("C:\\Users\\Leif\\AppData\\Roaming\\FFmpeg\\")
            self.logfield.insert(END, "\nINFO: Making FFmpeg directory, probably your first time installing with Winpeg!\n")
        except:
            print("FFmpeg folder is already there, by this script?")
            self.logfield.insert(END, "\nINFO: FFmpeg folder inside default user AppData folder detected!\n")
        self.logfield["state"] = "disabled"

        print("Made FFmpeg directory for unzipping...")

        try:
            with ZipFile("ffmpeg.zip", 'r') as zip: # extracts downloaded zip from ffmpegs download API for latest release
                zip.extractall(self.permDir) # permanent spot for ffmpeg binary as said in line 27
        except zipfile.BadZipFile as e:
            self.logfield["state"] = "normal"
            self.logfield.insert(END, "\nERROR: File downloaded is not a zip file!\n")
            print(f"File downloaded is not a zip file, something wrong in the backend?:\n{e}")
        except FileNotFoundError as e:
            self.logfield["state"] = "normal"
            self.logfield.insert(END, "\nERROR: File downloaded is not a zip file!\n")
            print(f"No file was found with FileNotFoundError:\n{e}")


        self.logfield["state"] = "normal"

        self.logfield.insert(END, f"\nINFO: File extracted to final directory: {self.permDir}!")
        print("\nFile extracted...\n")

        self.logfield["state"] = "disabled"



    # cancels program and "saves"
    def cancel(self):
        self.logfield["state"] = "normal"
        self.bar(25)
        self.logfield.insert(END, f"\nWARNING: Installer program is closing!\n")
        time.sleep(0.1)
        self.logfield.insert(END, f"\nINFO: Programming quiting!")
        self.logfield["state"] = "disabled"


        print("DEBUG: Quitting function is after this line being executed")
        sys.exit(0)



# loop it lol XD

if __name__ == "__main__":
    parent = ThemedTk(themebg=True)
    app = Window(parent)
    parent.mainloop()
