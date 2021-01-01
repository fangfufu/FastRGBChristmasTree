# FastRGBChristmasTree
This is basically a faster / more sensible version of the driver code for the 3D RGB Xmas Tree from The Pi Hut [[1]]. The Pi Hut provided their own  on Github [[2]], but it is super slow - it only allows you to change one LED at a time. In The Pi Hut's code, changing a single LED requires the whole tree to be refreshed, which requires the generation of SPI command byte string. Refreshing the whole Christmas tree seem to be quite slow. Furthermore, every time the SPI command byte string gets generated, 5 list comprehensions are performed<sup>*</sup>. This could be slowing the program down. 

## Appendix - the LED map
|   |       |    |    |    |        |        |   |   |   |       |
|---|-------|----|----|----|--------|--------|---|---|---|-------|
|   |       | 0  | 1  | 2  | 3      | 3      | 2 | 1 | 0 |       |
|   |       |    |    |    | **0**  | **1**  |   |   |   |       |
| 0 |       |    |    |    | 24     | 19     |   |   |   |       |
| 1 |       |    |    |    | 23     | 20     |   |   |   |       |
| 2 |       |    |    |    | 22     | 21     |   |   |   |       |
| 3 | **7** | 12 | 11 | 10 | 3      | 3      | 9 | 8 | 7 | **2** |
| 3 | **6** | 6  | 5  | 4  | 3      | 3      | 2 | 1 | 0 | **3** |
| 2 |       |    |    |    | 13     | 18     |   |   |   |       |
| 1 |       |    |    |    | 14     | 17     |   |   |   |       |
| 0 |       |    |    |    | 15     | 16     |   |   |   |       |
|   |       |    |    |    | **5**  | **4**  |   |   |   |       |
|   |       |    |    |    |        |        |   |   |   |       |
|   |   R   |  A | S  | P  |   B    |   E    | R | R | Y |       |
|   |       |    |    |    |        |        |   | P | I |       |

[1]: https://thepihut.com/products/3d-rgb-xmas-tree-for-raspberry-pi
[2]: https://github.com/ThePiHut/rgbxmastree#rgbxmastree

<sup>*</sup> I could be wrong on this one - I am not very good with Python. This is based on my understand of line 88-90 of [tree.py](https://github.com/ThePiHut/rgbxmastree/blob/master/tree.py#L88-L90)
