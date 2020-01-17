
The Pacman environment can be setup to run with or without the LED matrix. If you do not currently have access to the matrix then ignore the 'Setting up the RGB Matrix' part.


## Install Python 3

The Pacman environment is written in `Python 3`. This must be installed on your machine. If using the Raspberian operating system on the Raspberry Pi or Ubuntu Linux then Python is already installed. For other operating systems, installation media can be found at https://www.python.org/downloads/.

## Clone the repository

If you have Git installed (reccomended) you can clone the repository from your terminal with:

    $ git clone git@github.com:bencevans/pacman.git

Otherwise a packaged ZIP can be downloaded from [here](https://github.com/bencevans/pacman/archive/master.zip).

## Install dependencies

We use various libraries (often called modules in Python) that are available through the Python package manger called Pip. Pip should've been installed with your Python installation.

To install the dependencies, open a console/terminal window and navigate to the game directory within the pacman repository.

    $ cd pacman/game

Within the game repository there's a `requirements.txt` file which contains a list of all the required dependencies.

Install the dependencies with:

    $ pip install --user -r requirements.txt

> Sometimes the `pip` command is installed as `pip3`

## Set up the RGB Matrix

The RGB Matrix runs off an Arduino which plugs into your computer or the Raspberry Pi. In order for the Arduino to control the LEDs the Arduino sketch found at /arduino/arduino.ino must be written using the Arduino IDE.

Chances are this program will already be written to the Arduino. In which case there's no need to complete this again.
