## Movement Operations

The Pacman environment supports 4 operations that take the form of single character strings:

| OP STRING | NAME |
|----|------|
| <center>`'U'`</center> | UP |
| <center>`'D'`</center> | DOWN |
| <center>`'L'`</center> | LEFT |
| <center>`'R'`</center> | RIGHT |



## Base Strategy

To create a movement strategy, first create a file at `/game/moves/[filename].py` with the following contents:

```python
class MyMovementStrategy:

    name = 'Human Readable Name'

    def __init__(self, board):

        pass

    def generate_move(self, pacman):

        return 'R'
```

Now you can update the `generate_move` function with your own logic, always returning one of the four movement ops.

To run your strategy, use the `run.py` CLI with the strategy option matching your filename.


## Ideas

* Shortest Path to nearest nugget
* Furthest Path from Ghosts
* Reinforcment Learners
* Read from Sensors

