# sccplay
Run a playlist of midi files through GXSCC.

Requires GXSCC to be installed and added to the system path!

Download GXSCC here (Get the installer): https://meme.institute/gxscc/
Go to the directory where you installed it to (usually C:\Program Files (x86)\GXSCC\) and verify that gxscc.exe is present
Add the correct directory to the system path and you're done!

# Usage

sccplay [-h] [-d DIR] [-s] [-l,]

Arguments (Optional):
-d --dir        Specify midi/playlist directory. If you don't specify it will use the working directory
-s --shuffle    Use this argument to shuffle
-l --loop       Use this argument to loop

Place the executable somewhere in your system path so you can run it from anywhere!

# Building

This was built with pyinstaller

```pyinstaller --onefile sccplay.py```
