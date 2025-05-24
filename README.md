# sccplay
Run a playlist of midi files through GXSCC.

# Usage

sccplay [-h] [-d DIR] [-s] [-l,]

Arguments (Optional):
-d --dir        Specify midi/playlist directory. If you don't specify it will use the working directory
-s --shuffle    Use this argument to shuffle
-l --loop       Use this argument to loop

# Building

This was built with pyinstaller

```pyinstaller --onefile sccplay.py```