'''
Configure the LED into a spinning swirl
'''
from tree import FastRGBChristmasTree
from time import sleep

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    i = list(range(0,8))


    tree[3] = [255,255,255]
    while True:
        tree[:,i[0]] = [255, 255, 255]
        tree[:,i[1]] = [255, 0, 0]
        tree[:,i[2]] = [0, 255, 0]
        tree[:,i[3]] = [0, 0, 255]
        tree[:,i[4]] = [255, 255, 255]
        tree[:,i[5]] = [255, 255, 0]
        tree[:,i[6]] = [255, 0, 255]
        tree[:,i[7]] = [0, 255, 255]

        tree.commit()

        t = i[0]
        for j in range(0,7):
            i[j] = i[j+1]
        i[7] = t

        sleep(0.5)
