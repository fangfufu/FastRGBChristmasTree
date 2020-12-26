from gpiozero import SPIDevice, SourceMixin
from numpy import array

class FastRGBChristmasTree(SourceMixin, SPIDevice):
    def __init__(self, brightness=1, autocommit=0, *args, **kwargs):
        super(FastRGBChristmasTree, self).__init__(mosi_pin=12, clock_pin=25,
                                                   *args, **kwargs)
        # Number of LEDs
        self.nled = 25
        # LED configuration array
        self.leds = array([[24, 19, 7, 0, 16, 15, 6, 12],
                          [23, 20, 8, 1, 17, 14, 5, 11],
                          [22, 21, 9, 2, 18, 13, 4, 10],
                          [3,  3,  3, 3, 3,  3,  3, 3 ]])
        # Start of array __offset
        self.__offset = 4
        # frame padding
        frame_s = [0] * (self.__offset)
        frame_end = [0] * 5
        # transmit buffer
        self.__buf = frame_s + [0] * self.nled * 4 +frame_end
        self.reset()
        self.off()
        self.brightness = 1
        self.autocommit = autocommit

    def __len__(self):
        return self.nled

    def __setitem__(self, ind, val):
        # Enable the use of the slice operator
        if isinstance(ind, slice):
            r_start = ind.start if ind.start is not None else 0
            r_stop = ind.stop if ind.stop is not None else self.nled
            r_step = ind.step if ind.step is not None else 1
            r = range(r_start, r_stop, r_step)
            if type(val[0]) is not list:
                for i in r:
                    self.__setitem__(i, val)
                return
            elif len(val) == len(r):
                for i in range(0, len(val)):
                    self.__setitem__(r[i], val[i])
                return
            else:
                raise IndexError("Mismatch between the LED indices and the \
dimension of the colour list. ")

        if len(val) < 3 or len(val) > 4:
            raise IndexError("The length of the val array must be between 3 \
and 4.")

        for i in val:
            if i >255:
                raise ValueError("The val must be between 0-255!")

        s = self.__offset + ind * 4

        if len(val) == 3:
            s += 1
        else:
            val[0] = self.__brightness_convert(val[0])

        # Swap RGB to BGR
        self.__buf[s]   = val[-1]
        self.__buf[s+1] = val[-2]
        self.__buf[s+2] = val[-3]

    def __getitem__(self, ind):
        if isinstance(ind, slice):
            val = []
            # Convert slice to range
            r_start = ind.start if ind.start is not None else 0
            r_stop = ind.stop if ind.stop is not None else self.nled
            r_step = ind.step if ind.step is not None else 1
            r = range(r_start, r_stop, r_step)
            for i in r:
                val.append(self.__getitem__(i))
            return val
        else:
            s = self.__offset + ind * 4
            val = [None] * 4
            val[0] = self.__brightness_revert(self.__buf[s])
            val[1] = self.__buf[s+3]
            val[2] = self.__buf[s+2]
            val[3] = self.__buf[s+1]
            return val

    def __del__(self):
        super(FastRGBChristmasTree, self).close()

    def __brightness_convert(self, val):
        if val > 31 or val < 1:
            raise ValueError("The brightness must be between 1 and 31")
        # 0b1110000 == 224
        return 0b11100000 | int(val)

    def __brightness_revert(self, val):
        return 0b00011111 & val

    def commit(self):
        self._spi.transfer(self.__buf)

    def off(self):
        for i in range(0, self.nled):
            self.__setitem__(i, [1, 0, 0, 0])
        self.commit()

    def reset(self):
        for i in range(0, len(self.__buf)):
            self.__buf[i] = 0
        self.commit()

    @property
    def brightness(self):
        val = 0
        for i in range(0, self.nled):
            s = self.__offset + i * 4
            val += self.__buf[s]
        return self.__brightness_revert(int(val / self.nled))

    @brightness.setter
    def brightness(self, val):
        for i in range(0, self.nled):
            s = self.__offset + i * 4
            self.__buf[s] = self.__brightness_convert(val)

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    tree[0:tree.nled:7] = [255, 0, 0]
    tree[1:tree.nled:7] = [0, 255, 0]
    tree[2:tree.nled:7] = [0, 0, 255]
    tree[3:tree.nled:7] = [255, 255, 0]
    tree[4:tree.nled:7] = [255, 0, 255]
    tree[5:tree.nled:7] = [0, 255, 255]
    tree[6:tree.nled:7] = [255, 255, 255]
    tree.commit()
    print(tree[0:7])
    print(" ")
    print(tree[:])

