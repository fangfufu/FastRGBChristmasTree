'''
Randomly sparkle LEDs
'''
from tree import FastRGBChristmasTree
from random import random

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    while True:
        for i in range(0,25):
            on = 255 if random() < 0.66 else 0
            tree[i] = [1, on, on, on]
        tree.commit()
