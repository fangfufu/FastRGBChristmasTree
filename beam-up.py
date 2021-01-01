'''
Divide the Christmas tree into 4 layers, with red, green, blue and
white. Then move each layer up
'''
from tree import FastRGBChristmasTree
from time import sleep

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    i = 0
    j = 1
    k = 2
    l = 3

    while True:
        tree[i,:] = [255, 0, 0]
        tree[j,:] = [0, 255, 0]
        tree[k,:] = [0, 0, 255]
        tree[l,:] = [255, 255, 255]

        tree.commit()

        t = i
        i = j
        j = k
        k = l
        l = t

        sleep(0.5)

