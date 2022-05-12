"""

This is the official compile/build script for Winpeg, made by leifadev.

If there are ANY errors, *Please* report them informally or formally. This can be through
the github (https://github.com/leifadev/winpeg/issues) as issues, or a DM even.

It also recommended that you could make a commit or pull request for any issues as well, if
you have a github account :)

Thank you for supporting by downloading Winpeg!

"""

import glob
import subprocess
import os
import urllib.error
import time


# Script makes PyInstaller command to compile the program yourself easily!

class setup:
    def __init__(self):
        # Main Vars
        self.which = ""
        self.version = ""
        self.debug = ""
        self.appVersion = ""
        self.pip = "pi3.3456789 "
        self.python = "python3.6789 "
        self.modFile = ""
        self.manReq = bool

        ## Supported image file types for icons ##
        self.extensions = [".png", ".icns", ".ico"]
        ##########################################

        # print(os.getcwd())
        print("\n** THIS SCRIPT REQURIES PYTHON 3.6+ **")
        print("\n** ELEVATED PRIVILAGES like sudo, may be NEEDED for the script compiling! **\n")

        time.sleep(1)

        print("Starting compile process...")

        self.moveOn = (input("What python path/version are you using? (python, python3.8): "))
        if "python" in self.moveOn:
            self.version = "python"
            print("You selected: " + self.version)
            for x in self.version:
                if x not in self.python:
                    print("Your pip version may be outdated or your entry is invalid.")
                    continue
            if "3" in self.moveOn:
                print("Ok, you seem to be using a python version of python to python3.9!")
            else:
                pass
        else:
            print("You have to use a supported version of python! (sorry if you customized your path to pysnake69, etc.)")
            return
        self.version = self.moveOn
        print(f"\nYour using: {self.version}")

        time.sleep(0.5)
        print("\nBeginning!\n")

        self.installmodules()

    def installmodules(self):
        self.which = (input("What pip version are you using? (pip, pip3): "))
        if "pip" in self.which:
            print("You selected: " + self.which)
            for x in self.which:
                if x not in self.pip:
                    print("\nYour pip version may be outdated or your entry is invalid.")
                    continue
            if "3" in self.which:
                print("\nOk, you seem to be using a pip version of pip3 or pip3.9!")
        else:
            print("\nYou have to use pip as your package manager!")
            return
        print(f"\nYour using: {self.which}")

        # Make and/or reset module requirements!
        subprocess.run(f'{self.which} install pip-upgrader', shell=True)
        try:
            import wget
            import pyperclip
        except ModuleNotFoundError as e:
            print(f"Require modules for the script were not found! {e}")
            subprocess.run(f'{self.which} install wget pyperclip', shell=True)
            import wget
            import pyperclip

        if self.which in ("pip", "pip3"):
            time.sleep(0.5)
            try:
                os.remove("requirements.txt")
            except FileNotFoundError:
                print(f'requirements.txt is not present as acting for freezing modules. Maybe you have a file for this under a different name?')

            self.manReq = str(input("\nEnter for default version modules: "))
            """
            DEV NOTE: As of Feb. 18 2022, the automatic requirements.txt pipdeptree option is deprecated and REMOVED
            The reason why you are seeing self.manReq still being used, and being True everytime is just for the sake of simplicity in removing
            the feature from the setup.py script. The above input() prompt essentially now is just a confirmation prompt, it's easier for me to
            just set too true regardless and keep some structure in case I need to use the option again at all, probably not thought ;)
            """

            if self.manReq == "":
                self.manReq = True
            else:
                self.manReq = True
            print(f"\nRemoving requirements.txt in current folder directory...\n")
            time.sleep(1)
            print(os.getcwd() + ", is the current executing path. \nIf this isn't, maybe look into the code, and/or submit an issue at the github")
            time.sleep(2)
            print("\n**Installing**")
            print(self.manReq)
            time.sleep(1)
            try:
                import tkinter
                if self.manReq:
                    print(f"Installing pre-made modules")
                    time.sleep(1)
                    if os.path.isfile("manReq.txt"):
                        print("No manReq.txt! Making fresh one")
                        os.remove("manReq.txt")

                    # Download custom name requirements.txt
                    try:
                        wget.download("https://raw.githubusercontent.com/leifadev/winpeg/main/manReq.txt", "manReq.txt")
                        print("manReq.txt not present! Generating new one")
                    except urllib.error.HTTPError as err:
                        print(f"ERROR: Request for new manReq.txt from github url not wasn't found/invalid!\n{err}")

                    subprocess.run(f"pip-upgrade --skip-package-installation manReq.txt", shell=True) # upgrade manreq.txt
                    subprocess.run(f"{self.which} install -r manReq.txt", shell=True)
                    print(f"Upgraded modules from repo!")

                elif self.manReq == False:
                    pass # Use this if needed a second option/method to auto upgrade all modules

            except ModuleNotFoundError:
                print(f'\n----------------------------------------------\nYou do not have tkinter installed with python!\nTkinter is required for the GUI to work.\n----------------------------------------------\n')
                pass
        else:
            print("Not a valid option! Use pip or pip3\nIf you use another version like pip3.9, try pip3, if that doesn't work contact the developer.")
            return

    # Call PyInstaller to compile baby
        self.compile(None, None, None, None) # settings for pyinstaller args


    def compile(self, debug, icon, name, bundleId):
        print("\nTarget File: Specify a .py file that is the main python file to compile with: ")

        # Asking for compile options

        self.targetFile = str(input("Press enter for default, otherwise please specify: "))

        if self.targetFile == "":
            self.targetFile = "main.py"
        else:
            if ".py" not in self.targetFile:
#                print("ERROR: You did not include .py in your file. Please use e.g. main.py.")
                return

        print(f'\nYou chose:\n >> {self.targetFile} << \n')


        print("\nDebug: When enabled will show a verbose logging console for realtime\ntraceback and exception errors.\n")

        self.debug = str(input("Press enter for windowed mode, type anything for debug mode: "))

        if self.debug == "":
            self.debug = "--windowed"
        else:
            self.debug = "--console"
        print(f'\nYou chose:\n >> {self.debug} << \n')


        # print("\nVersion: Adds a version file value with your compile arguments\n")
        #
        # self.appVersion = str(input("Press enter for no version value, type your desired custom version (e.g. v1.1.1, v.2.1-beta): "))
        #
        # print(f'\nYou chose:\n >> {self.appVersion} << \n')


        print(f'\nFound these image files in images direcotry\nDetected Possible Icons:')

        options = {}
        count = 0

        for ext in self.extensions:
            files = glob.glob(os.getcwd() + "/images" + '/**/*' + ext, recursive=True)
            if len(files) > 1:
                for x in files:
                    options.update({count:x})
                    count += 1
            else:
                for x in files:
                    options.update({count:x})
                    count += 1
            self.icount = count

        for key in options:
            print(f'[{key}]: {options.get(key)}')

        self.icon = str(input("\nPress enter to skip setting an icon, or specify file name: "))

        try:
            if self.icon != "":
                if int(self.icon) in range(0,self.icount):
                    for key, value in enumerate(options):
                        if str(self.icon) == str(key):
                            self.icon = (options.get(key))
                            print(f'\nYou chose:\n[{key}]: {self.icon}\n')
                        else:
                            pass
                            # print(key, self.icon)
                            # print("---")

                    else:
                        pass
                else:
                    print("Not a valid option! If you don't see your icon, it may not be supported!\nAdd your file extension in setup.py at line 32")
                    return
            else:
                pass
        except NameError as e:
            print(f'Detected no specifed icon...')
            print(e)


        print("\nName: Adds a name for the application, with your compile arguments\n")

        # get rid of bs
        self.icon = str(self.icon)
        self.icon = self.icon.translate({ord(i): None for i in '[],'})

        self.name = str(input("Press enter for default name, otherwise specify: "))

        if self.name == "":
            self.name = "Winpeg"
        else:
            pass

        print(f'\nYou chose:\n >> {self.name} <<\n')

        self.bundleId = str(input("Press enter for no bundle ID, other wise specify: "))

        while "." not in self.bundleId:
            self.bundleWarn = input("\nYour bundle ID didn't include any periods to seperate the developer \nand the apps name for example.\nDo you want to try again? Y/n: ")
            if self.bundleWarn in "Yy":
                self.bundleId = str(input("Press enter for no bundle ID, other wise specify: "))
            elif self.bundleWarn in "Nn":
                if self.bundleId == "":
                    self.bundleId = "com.leifadev.winpeg"
                break
            else:
                continue
        else:
            pass

        # if self.bundleWarn == "":
        #     self.bundleId = "com.leifadev.winpeg"


        print(f'\n-------------------------------\nYou have configured debug to "{self.debug}",\nYou have configured your version to be: "{self.appVersion}",\nYou have configured your icon to the path: {self.icon},\nYou have configured name to be: "{self.name}",\nYou configured bundle ID is: "{self.bundleId}"\n\nSettings saved!\n-------------------------------')
        time.sleep(2)

        print("Are you sure you want to compile?")
        comp = input("Do you want to proceed? Y/n: ")
        if comp in "yY":
            pass
        elif comp in "nN":
            return
        else:
            return


        print(f'{self.version} -m PyInstaller --onefile {self.debug} --icon={self.icon} --osx-bundle-identifier={self.bundleId} --version-file="{self.appVersion}" -n={self.name} {self.targetFile}')


        time.sleep(2)


        import pyperclip
        clipBool = input("Do you want to copy the compile terminal command to your clipboard just in case? Y/n: ")
        if clipBool in "yY":
            pyperclip.copy(f'{self.version} -m PyInstaller --onefile {self.debug} --icon={self.icon} --osx-bundle-identifier={self.bundleId} --version-file="{self.appVersion}" -n={self.name} {self.targetFile}')
        elif clipBool in "nN":
            return
        else:
            return

        time.sleep(1)

        # compile command


        try:
            # print(f'Compiling configurations: {self.debug}, {self.icon}, {self.name}, {self.bundleId}')
            subprocess.run(f'{self.which} install pyinstaller', shell=True)
            subprocess.run(f'{self.version} -m PyInstaller --onefile {self.debug} --icon="{self.icon}" --osx-bundle-identifier="{self.bundleId}" --version-file="{self.appVersion}" -n="{self.name}" {self.targetFile}', shell=True)

        except ModuleNotFoundError as e:
            print(f'Pyinstaller wasn\'t not found! Try to install it again, must haven\'t worked')
        except PermissionError as d:
            print(f"Permission error! This script doesn't have certain permissions.\n{d}")




if __name__ == '__main__':
    setup()

# end of script
