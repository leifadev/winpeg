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
import webbrowser, getpass, requests, os, time, darkdetect, sys, ssl, logging, wget
from zipfile import ZipFile
import threading, queue
from functools import partial
from tkinter import messagebox
import subprocess


class Window:
    """Main window for Winpeg """

    def __init__(self, parent):

        self.permDir = f"C:/Users/{getpass.getuser()}/AppData/Roaming/"
        self.tempDir = f"C:/Users/{getpass.getuser()}/AppData/Local/Temp/"
        self.icon = ""
        self.version = "v0.1"
        self.file_name = "ffmpeg.zip" # don't change this, just for extra purposes
        self.mode = "User" # Leave User env variable for now, add feature for User and System later

        ssl._create_default_https_context = ssl._create_unverified_context

        # Replacing / with \ for actual compatibility around previews f strings using them to avoid \\'s
        self.permDir = self.permDir.translate({ord('/'): '\\'})
        self.tempDir = self.tempDir.translate({ord('/'): '\\'})

        self.UIAttributes = { # pre-made attributes to be place holders for multiple tkinter parames later on
            "Font": "Courier",
            "charSize": 8,
            "restartTextPos": 302,
            "logFont": "Courier",
            "logSize": 8,
            "verSize": 8
        }

        # Create and configure logger
        logging.basicConfig(filename=f"{self.tempDir}winpeg_log.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)


        parent.title("Scout Windows FFmpeg Installer")

        width=450
        height=350
        screenwidth = parent.winfo_screenwidth()
        screenheight = parent.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr)
        parent.resizable(width=False, height=False)


        # Download logo icon!
        logging.info("Attemping logo downloading...")
        url = "https://raw.githubusercontent.com/leifadev/scout/main/images/scout_logo_windows_installer.png"

        # Fetch latest ffmpeg build API https://ffbinaries.com/api
        ffmpeg_url = "https://ffbinaries.com/api/v1/version/latest"

        try:
            data = requests.get(ffmpeg_url).json()
        except ConnectionError as e:
            self.logfield.insert(END, f"WARNING: Icon could not be found or applied to the app!")
            logging.info(e)

        self.release_url = data["bin"]["windows-64"]["ffmpeg"]

        self.logfield = tk.Text(parent)

        # Download icon for use if not present
        if not os.path.isfile(self.tempDir + "scout_windows_installer.png"):
            wget.download(url, self.tempDir + "scout_windows_installer.png")
            self.logfield.insert(END, "INFO: Downloaded the app icon!")
        else:
            logging.debug("DEBUG: Icon detected!")

        try:
            self.icon = PhotoImage(file=self.tempDir + "scout_windows_installer.png")
            parent.tk.call('wm', 'iconphoto', parent._w, self.icon)
        except Exception as e:
            logging.warning(f"WARNING: Tkinter could not apply these app with PhotoImage class!\nIt's found directory should be {self.tempDir}, a temporary directory in Windows 10")
            self.logfield.insert(END, f"WARNING: Icon could not be found or applied to the app!")

        parent.update()   # Updates window at startup to be interactive and lifted


        # Menu Bar #

        self.menubar = Menu(parent)
        self.filemenu = Menu(self.menubar, tearoff=0)

        try:
            pass
            # self.filemenu.add_command(label="Cut", accelerator="Command+X", command=lambda: parent.focus_get().event_generate('<<Cut>>'))
            #
            # self.filemenu.add_command(label="Copy", accelerator="Command+C", command=lambda: parent.focus_get().event_generate('<<Copy>>'))
            #
            # self.filemenu.add_command(label="Paste", accelerator="Command+V", command=lambda: parent.focus_get().event_generate('<<Paste>>'))
            # self.filemenu.add_command(label="Select All", accelerator="Command+A", command=lambda: parent.focus_get().select_range(0, 'END')) # Does not work as of now v1.5
        except KeyError as e:
            print(f"Paste and copying functions failed!\n{e}")

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", accelerator="Command+Q", command=lambda: parent.quit())
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)

        self.helpmenu.add_command(label="About", command=self.aboutWindow)
        self.helpmenu.add_command(label="Help", command=lambda: webbrowser.open("https://github.com/leifadev/winpeg"))

        self.helpmenu.add_separator()

        self.helpmenu.add_command(label="Reset Environment Path", command=self.removeEnv)

        self.menubar.add_cascade(label="About", menu=self.helpmenu)

        self.menubar.entryconfig("About", state="normal")

        parent.config(menu=self.menubar)
        parent.update()


        # Define UI elements
        ft = tkFont.Font(family="Courier", size=8)
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(END, f"Launched successfully!\nVersion: {self.version}\n")
        self.logfield["state"] = "disabled"

        self.progress = ttk.Progressbar(parent, orient = HORIZONTAL,
                      length = 400, mode = 'determinate')

        self.installB=tk.Button(parent)
        self.installB["text"] = "Install"
        self.installB["command"] = self.download


        self.cancelB=tk.Button(parent)
        self.cancelB["text"] = "Cancel"
        self.cancelB["command"] = self.cancel

        # Apply darktheme!
        if darkdetect.isDark():
            parent.set_theme("equilux")
            self.darkMode = True
            self.logfield["bg"] = "#e5e5e5"
            self.cancelB["bg"] = "#444444"
            self.installB["bg"] = "#444444"
            self.cancelB["fg"] = "#ffffff"
            self.installB["fg"] = "#ffffff"

        elif darkdetect.isLight():
            self.darkMode = False
            logging.info("Light mode detected!")
        else:
            self.logfield.insert(END, "Detected no system theme! Defaulting to light mode")


        ## Gridding ##

        self.installB.pack(side=TOP)
        self.cancelB.pack(side=TOP)
        self.progress.pack(side=BOTTOM, pady=15)
        self.logfield.pack(side=BOTTOM, padx=40, pady=10)


    def removeEnv(self):
        logging.info("Removing set ffmpeg enviorment variable from install function using `REG` command\n(if was set at all in self.install...)")

        # https://www.digitalcitizen.life/remove-edit-clear-environment-variables/
        popUp = messagebox.askokcancel("Reset FFmpeg Enviorment Variable", "Do you want to remove the FFmpeg enviorment variable?\nFor the command to work again you will have to reinstall it again.")

        if popUp == True:
            logging.info("User confirmed yes, removing env var!")
            subprocess.run(f'powershell REG delete "HKCU\Environment" /F /V "ffmpeg"', shell=True)
            print(popUp)
        elif popUp == False:
            logging.info("User answered no!")
            print(popUp)


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

    def download(self):
        logging.info("Installing function running!!")

        # Bar process first
        logging.info(f"Current working directory isss... {os.getcwd()}!")

        self.logfield["state"] = "normal"
        self.logfield.insert(END, f"\nINFO: Downloading latest version of FFmpeg!\n")
        self.logfield["state"] = "disabled"


        def download(root, q):

            response = requests.get(self.release_url, stream=True)
            dl_size = int(response.headers['Content-length'])

            with open(f"{self.tempDir}ffmpeg.zip", 'wb') as fp:
                for chunk in response.iter_content(chunk_size=100_000):
                    fp.write(chunk)
                    q.put(len(chunk) / dl_size * 100)
                    parent.event_generate('<<Progress>>')
                    logging.debug("Chunk loaded")

            parent.event_generate('<<Done>>')

        def updater(pb, q, event):
            self.progress['value'] += q.get()
            logging.debug("Updating UI bar...")


            # Triggers next install function after 100 done
            if self.progress['value'] > 100:
                time.sleep(2)
                self.install()

        q = queue.Queue()
        update_handler = partial(updater, self.progress, q)
        parent.bind('<<Progress>>', update_handler)

        thread = threading.Thread(target=download, args=(parent, q), daemon=True)
        thread.start()

        self.logfield["state"] = "normal"
        self.logfield.insert(END, "\nINFO: Downloading latest stable version of ffmpeg, may take at least several seconds!\n")
        logging.info(f"Downloading latest binary from link! Sourcing from: {self.release_url}")
        self.logfield["state"] = "disabled"
        thread.stop()


    def install(self):

        self.logfield["state"] = "normal"

        self.logfield.delete("1.0","end")
        self.logfield.insert(END, f"Launched successfully!\nVersion: {self.version}\n")

        logging.info("Starting installation process: Creating directories, decompressing, writing env variables...\n\n")

        try:
            os.mkdir("C:/Users/Leif/AppData/Roaming/FFmpeg/")
            self.logfield.insert(END, "\nINFO: Making FFmpeg directory, probably your first time installing with Winpeg!\n")
        except:
            logging.info("FFmpeg folder is already there, by this script?")

        self.logfield["state"] = "disabled"

        logging.info("Made FFmpeg directory for unzipping...")


        # Extract, move, sys path #
        print(self.tempDir, self.permDir)
        import zipfile
        try:
            print("OOOO")
            with ZipFile(f"{self.tempDir}ffmpeg.zip", 'r') as zip: # extracts downloaded zip from ffmpegs download API for latest release
                zip.extractall(self.permDir + "FFmpeg") # permanent spot for ffmpeg binary

                # Messages for successful extract
                # self.logfield["state"] = "normal"
                logging.info("\nFile extracted...\n")
                # self.logfield.insert(END, f"\nINFO: File extracted to final directory: {self.permDir}!\n")
                # self.logfield["state"] = "disabled"

        except zipfile.BadZipfile as e:
            self.logfield["state"] = "normal"
            self.logfield.insert(END, "\nERROR: File downloaded is not a zip file!\n")
            logging.error(f"File downloaded is not a zip file, something wrong in the backend?:\n{e}")
        except FileNotFoundError as e:
            self.logfield["state"] = "normal"
            self.logfield.insert(END, "\nERROR: File downloaded is not a zip file!\n")
            logging.error(f"No file was found with FileNotFoundError:\n{e}")

        # Delete FFmpeg.zip
        os.remove(f"{self.tempDir}ffmpeg.zip")
        logging.info(f"Deleted compressed ffmpeg binary in {self.tempDir}")
        self.logfield.insert(END, f"\nDeleted compressed ffmpeg binary in: {self.tempDir}\n")


        # Instaniate systen enviorment variable #

        # Check the output of User's current env path via powershell
        env = subprocess.check_output("powershell $Env:Path")

        logging.info(f'Path for FFmpeg folder to be in: {self.permDir}')

        # Detect if variable possibly by this script is already made, regardless still running powershell cmd
        if f"{self.permDir}FFmpeg" in str(env):
            self.logfield.insert(END, "\nAlready detected Winpegs ffmpeg folder! Running env var script anyways\n")
            logging.warning(f"Already have Winpegs ffmpeg path! ({self.permDir})")
            subprocess.run(f"powershell [Environment]::SetEnvironmentVariable('ffmpeg', '{self.permDir}FFmpeg', 'User')", shell=True)
        else:
            subprocess.run(f"powershell [Environment]::SetEnvironmentVariable('ffmpeg', '{self.permDir}FFmpeg', 'User')", shell=True)
            logging.info(f"Added path: {self.permDir}")
            self.logfield.insert(END, "\nSuccessfully added enviorment variable!\n")


    # Cancel function: bar animation with a exit code of 0, console output too
    def cancel(self):
        self.logfield["state"] = "normal"
        self.logfield.insert(END, f"\nWARNING: Installer program is closing!\n")
        self.bar(20)
        self.logfield.insert(END, f"\nINFO: Programming quiting!")
        self.logfield["state"] = "disabled"

        logging.debug("DEBUG: Quitting function is after this line being executed")
        sys.exit(0)


    def aboutWindow(self):

        abtWindow = ThemedTk(themebg=True)

        abtWindow.title("About")
        # abtWindow.iconphoto(False, self.icon)

        if self.darkMode:
            abtWindow.set_theme("equilux")
        else:
            pass

        width=300
        height=300
        screenwidth = abtWindow.winfo_screenwidth()
        screenheight = abtWindow.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        abtWindow.geometry(alignstr)
        abtWindow.resizable(width=False, height=False)

        self.abtWindowTitle = ttk.Label(abtWindow)
        self.abtWindowTitle = Label(abtWindow, text="About")
        self.abtWindowTitle.place(x=45,y=10,width=210)
        if self.darkMode:
            self.abtWindowTitle["bg"] = "#464646" # dark theme gray
            self.abtWindowTitle["fg"] = "#999999" # light theme gray
        else:
            self.abtWindowTitle['bg'] = "#ececec"
            self.abtWindowTitle["fg"] = "black"

        ## All below are just the elements to the about pane, you can figure these out I'm sure :)
        abtWindowMsg = f"Author: leifadev\nLicense: GPL/GNU v3\nVersion: {self.version}\n\nLanguage: Python 3.6+\nCompilier: Pyinstaller\nFramework: Tkinter"
        self.msg = ttk.Label(abtWindow)
        self.msg = Label(abtWindow, text=abtWindowMsg, anchor=CENTER, wraplength=160, justify=CENTER)
        self.msg.place(x=50,y=40,width=200)
        if self.darkMode:
            self.msg["bg"] = "#464646" # dark theme gray
            self.msg["fg"] = "#999999" # light theme gray
        else:
            self.msg['bg'] = "#ececec"
            self.msg["fg"] = "black" # If statement checking if darkMode is on and to switch bg accordingly


        self.abtWindowLink = "Contribute to the wiki!"
        self.abtWindowLink = ttk.Label(abtWindow)
        self.abtWindowLink = Label(abtWindow, font=(self.UIAttributes.get("Font"), self.UIAttributes.get("charSize"), "underline"), text="Read the wiki for more info!", anchor=CENTER, wraplength=160, justify=CENTER)
        self.abtWindowLink.place(x=50,y=170,width=200)
        self.abtWindowLink["fg"] = "#2f81ed"
        self.abtWindowLink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/leifadev/winpeg/wiki"))
        if self.darkMode: # If statement checking if darkMode is on and to switch bg accordingly
            self.abtWindowLink["bg"] = "#464646" # dark theme gray
        else:
            self.abtWindowLink['bg'] = "#ececec"



# loop it lol XD

if __name__ == "__main__":
    parent = ThemedTk(themebg=True)
    app = Window(parent)
    parent.mainloop()
