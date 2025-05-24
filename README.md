# sccplay
Run a playlist of midi files through GXSCC.

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
