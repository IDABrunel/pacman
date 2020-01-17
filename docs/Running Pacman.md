The Pacman environment can be run either from a CLI or programatically. Initially we reccomend running through the command line steps to ensure everything is setup properly before working on programmatic initialisation.

## Command Line

Within the `/game` directory in the repository you will find `run.py`. This provides an a command line interface to getting Pacman running.

Running the following command (after initial setup) should provide you with a list of options available.

    $ python3 run.py

Something similar to the following output should show.

```text
usage: run.py [-h] [--matplotlib] [--arduino] [--arduino_path ARDUINO_PATH]
              [--nooutput] [--images]
              [--strategy {full_random,valid_random,valid_random_momentum,user_input}]

optional arguments:
  -h, --help            show this help message and exit
  --matplotlib          Enables matplotlib output
  --arduino             Enables Arduino output
  --arduino_path ARDUINO_PATH
                        Arduino serial path
  --nooutput            Enables nooutput
  --images              Saves each figure to ./images/xxxx.png
  --strategy {full_random,valid_random,valid_random_momentum,user_input}
                        Pacman move strategy
```

In order to run the enviroment you need to enable at least one output and set a strategy.

There are various outputs that the CLI can write to. To begin with use `--matplotlib` which will render the board to a new window on your machine. Other outputs are `--arduino`, `--images` and `--nooutput`.

Multiple outputs can be enabled at the same time, just by adding the appropriate `--[output name]` to the `python3 run.py` command.

A strategy can be seen as an algorithm to control Pacman's movement.

Initially, try running the matplotlib output with the valid_random_momentum strategy...

    $ python3 run.py --matplotlib --strategy valid_random_with_momentum

## Code

TODO. For the time being, take a look at the run.py file.