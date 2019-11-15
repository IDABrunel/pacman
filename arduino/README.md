# Arduino

The `arduino.ino` provides a serial based API for updating the pixels.

## API

* Serial connection running at 9600 baud.
* `\n` delimetered commands

### Update Pixel

```
id,r,g,b\n
```

* `id` (int) Between 0 and the number of pixels - 1
* `r` (int) Between 0 and 255
* `g` (int) Between 0 and 255
* `b` (int) Between 0 and 255

