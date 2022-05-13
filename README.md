# Winpeg: FFmpeg installed with one click!

## What is Winpeg?

Winpeg is a installer for windows that downloads, installs, and configures [FFmpeg ](ffmpeg.org/)to be ready at the command-line. It does all the dirty work; downloading the **_latest_** binary of FFmpeg via https://ffbinaries.com, storing it in a safe and appropriate backend directory, safely configuring a environment variable to it, and leaving logs for debugging/troubleshooting!

### Where is it installed?

As of newer versions of this installer, choices for installed directories will be available. But for now the current user and system directories are:

**User**: `C:\Users\User123\AppData\Roaming\FFmpeg`

**System**: `C:\Programs\FFmpeg`


## Can I trust this app?

Yes! The code is completely public and you can see for yourself exactly what it does. Python is a simple language to read, and a non-programmer can get the gist of anything at least to fishy that could be going on.

For those fluent you can easily see more that this script doesn't do anything harmful at all. In fact, here is a simple verbalized process that    the code does below.


### Can I trust this app: How does it work?

This is the simple process of what happens:

1. Configures variables: directories, paths, urls
2. Handles GUI elements such as windows, buttons, dark mode
3. Downloads latest windows ffmpeg binary to user's `Temp` folder
4. Extracts `ffmpeg.zip` into user's `AppData` or systems `Programs` directories
5. Creates enviorment variable via powershell commands using [`subprocess`](https://docs.python.org/3/library/subprocess.html)
    - Uses powershell command [`[Environment]::SetEnvironmentVariable`](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.2#using-the-systemenvironment-methods) to set a permanent (until removed) ffmpeg enviorment variable https://github.com/leifadev/winpeg/blob/5dfc11d3504141a1edc3786ac0828d90fddfd075/main.py#L322
7. Deletes original downloaded data (the zip file) from `Temp`
