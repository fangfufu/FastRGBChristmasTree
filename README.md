# FastRGBChristmasTree
This is basically a faster / more sensible version of the driver code for the 3D RGB Xmas Tree from The Pi Hut [[1]]. The Pi Hut provided their own  on Github [[2]], but it is super slow - it only allows you to change one LED at a time. In The Pi Hut's code, changing a single LED requires the whole tree to be refreshed, which requires the generation of SPI command byte string. Refreshing the whole Christmas tree seem to be quite slow. Furthermore, every time the SPI command byte string gets generated, 5 list comprehensions are performed<sup>*</sup>. This could be slowing the program down. 

## How to use the driver
Put ``tree.py`` in the same folder as your code. To instantiate the driver, use the following:
```python
from tree import FastRGBChristmasTree
tree = FastRGBChristmasTree()
```
To set a LED, you can do the following:
```python
tree[22] = [255, 0, 0]
```
Of course, the above is the equivalent as 
```python
tree[2,0] = [255, 0, 0]
```
You can also set individual LED's brightness (which you cannot do using The Pi Hut's code). 

```python
tree[22] = [10, 255, 0, 0]
```
You can also set multiple LEDs at once, e.g.
```python
tree[:,0]   = [[255, 0, 0], [255, 255, 0], [0, 255, 0]]
```
The LEDs are set using a list in the format of ``[R, G, B]`` or ``[Brightness, R, G, B]``, where Brightness is an integer between 0-30 inclusive, and R, G, B is an integer between 0-255.

The statements above only configures the command buffer, which still needs to be sent down to the SPI bus. To commit your configuration, do:
```python
tree.commit()
```
The indexing schemed is explained in the section below.

## The indexing of the LEDs
I decided to include a numpy array (``__led_config``) to help with indexing the LEDs [[3]]. Vertically, the LEDs are separated into layers, based on the height from the base of the tree. The bottom layer is layer 0. The layer below the star is layer 2. If you look at the Christmas tree from top down, you can see that the tree has 8 "vanes". The numpy array stores the index for each LED in the format of ``[layer][vane]``. If you orient the tree in such a way that the Raspberry Pi is towards you, you can index the LEDs using the table below: 

|         |       |    |    |    |        |        |   |   |   |       |
|---------|-------|----|----|----|--------|--------|---|---|---|-------|
|**Layer**|       | 0  | 1  | 2  | 3      | 3      | 2 | 1 | 0 |       |
|         |**Vane**|    |    |    | **0**  | **1**  |   |   |   |       |
| 0       |        |    |    |    | 24     | 19     |   |   |   |       |
| 1       |        |    |    |    | 23     | 20     |   |   |   |       |
| 2       |        |    |    |    | 22     | 21     |   |   |   |       |
| 3       | **7**  | 12 | 11 | 10 | 3      | 3      | 9 | 8 | 7 | **2** |
| 3       | **6**  | 6  | 5  | 4  | 3      | 3      | 2 | 1 | 0 | **3** |
| 2       |        |    |    |    | 13     | 18     |   |   |   |       |
| 1       |        |    |    |    | 14     | 17     |   |   |   |       |
| 0       |        |    |    |    | 15     | 16     |   |   |   |       |
|         |        |    |    |    | **5**  | **4**  |   |   |   |       |
|         |        |    |    |    |        |        |   |   |   |       |
|         |   R    |  A | S  | P  |   B    |   E    | R | R | Y |       |
|         |        |    |    |    |        |        |   | P | I |       |

## Other thoughts 
The existing example code is awful. There is no datasheet. I would have expected better documentation and drivers for the £18 I paid. 

[1]: https://thepihut.com/products/3d-rgb-xmas-tree-for-raspberry-pi
[2]: https://github.com/ThePiHut/rgbxmastree#rgbxmastree
[3]: https://numpy.org/doc/stable/user/basics.indexing.html

<sup>*</sup> I could be wrong on this one - I am not very good with Python. This is based on my understand of line 88-90 of [tree.py](https://github.com/ThePiHut/rgbxmastree/blob/master/tree.py#L88-L90)
