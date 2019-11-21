# Game

**Dependencies**

```
pip3 install --user pyserial matplotlib
```

**Run**

If the LED matrix is unavailable then run with `--matplotlib` to show on screen.

```
$ python3 run.py 
usage: run.py [-h] [--matplotlib] [--arduino] [--nooutput] [--images]

optional arguments:
  -h, --help    show this help message and exit
  --matplotlib  Enables matplotlib output
  --arduino     Enables Arduino output
  --nooutput    Enables nooutput
  --images      Saves each figure to ./images/xxxx.png
```