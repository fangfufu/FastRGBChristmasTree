'''
Cycles the LEDs with random colours.
'''
from tree import FastRGBChristmasTree
from colorzero import Color
from random import random

def random_colour():
    h = random()
    s = 1
    v = 1
    hsv = Color.from_hsv(h,s,v)
    rgb = list(hsv.rgb)
    rgb = [int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)]
    return (rgb)

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    while True:
        for i in range(0,25):
            rgb = random_colour()
            tree[i] = [1, rgb[0], rgb[1], rgb[2]]
        tree.commit()
