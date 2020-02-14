# Arduino LED Matrix Serial API

The `arduino.ino` file contains the Arduino C code which provides a serial based API for updating a NeoPixel LED Matrix.

## API

### Operations

An operation takes the form of a binary array. The first byte will be the `OP_CODE`, followed by any arguments such operation requires.

Once the Arduino has performed the requested operation it will inform return with an end message in the form of a single `E` character denoting the end.

The end message should be waited for at the end of each operation that's sent. If writing commands to the Arduino in batch, then the software should wait until it's received the same number of end messages as the operations sent initially.

```
>> OP_CODE [ARG_0 ARG_1 ARG_3...]
<< E
```

#### Clear

```
OP_CODE = 0x00
```

The clear operation resets the pixel values in the Arduino's memory. Essentially this is the same as using the [Update Pixel](#Update-Pixel) operation for every pixel with red, green and blue values set to `0`. It's also required to then call the [Show](#Show) operation to update the LEDs.

#### Update Pixel

```
OP_CODE = 0x01
```

Arguments:

* `id` (byte x 2) Between 0 and the number of pixels - 1
* `r` (byte) Between 0 and 255
* `g` (byte) Between 0 and 255
* `b` (byte) Between 0 and 255

The update pixel operation updates the Arduino's memory. A further show operation is required to update the LEDs.

#### Show

```
OP_CODE = 0x02
```

The show operations updates the LED matrix based on the Arduino's memory and requires no arguments.

### Examples

#### Clearing the LEDs using individual writes

```
# Clear the Arduino's memory

send 0x00ff
wait_for E

# Show

send 0x02ff
wait_for E

# Complete
```

#### Clear, set a pixel and show

```
# Send the clear, set pixel and show ops

#      CL EN ST ID R  G  B  E
send 0x00 ff 01 ff ff ff ff ff
# Wait for 3 op ends

wait_for EEE

# Complete
```