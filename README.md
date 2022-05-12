# Winpeg: FFmpeg installed with one click!

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
6. Deletes original downloaded data in `Temp`
