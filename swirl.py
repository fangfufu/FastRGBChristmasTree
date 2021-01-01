'''
Configure the LED into a spinning swirl
'''
from tree import FastRGBChristmasTree
from time import sleep

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    i = 0
    j = 1
    k = 2
    l = 3

    tree[3] = [255,255,255]
    while True:
        tree[:,i*2]   = [[255, 0, 0], [255, 255, 0], [0, 255, 0]]
        tree[:,i*2+1] = [[255, 0, 0], [255, 255, 0], [0, 255, 0]]
        tree[:,j*2]   = [[255, 255, 0], [0, 255, 0], [0, 0, 255]]
        tree[:,j*2+1] = [[255, 255, 0], [0, 255, 0], [0, 0, 255]]
        tree[:,k*2]   = [[0, 255, 0], [0, 0, 255], [255, 0, 0]]
        tree[:,k*2+1] = [[0, 255, 0], [0, 0, 255], [255, 0, 0]]
        tree[:,l*2]   = [[0, 0, 255], [255, 0, 0], [255, 255, 0]]
        tree[:,l*2+1] = [[0, 0, 255], [255, 0, 0], [255, 255, 0]]

        tree.commit()

        t = i
        i = j
        j = k
        k = l
        l = t

        sleep(0.5)

