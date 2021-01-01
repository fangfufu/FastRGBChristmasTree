'''
Randomly sparkle LEDs
'''
from tree import FastRGBChristmasTree
from random import random

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    while True:
        for i in range(0,25):
            rgb = random_sparkle()
            on = 1 if random() > 0.5 else 0
            tree[i] = [1, on, on, on]
        tree.commit()
