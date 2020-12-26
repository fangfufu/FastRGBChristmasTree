from gpiozero import SPIDevice, SourceMixin
from numpy import array

class FastRGBChristmasTree(SourceMixin, SPIDevice):
    def __init__(self, *args, **kwargs):
        super(FastRGBChristmasTree, self).__init__(mosi_pin=12, clock_pin=25, *args, **kwargs)
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

    def __len__(self):
        return self.nled

    def __setitem__(self, ind, val):
        # Enable the use of the slice operator
        if isinstance(ind, slice):
            r_start = ind.start if ind.start is not None else 0
            r_stop = ind.stop if ind.stop is not None else self.nled
            r_step = ind.step if ind.step is not None else 1
            for i in range(r_start, r_stop, r_step):
                self.__setitem__(i, val)
            return

        if len(val) < 3 or len(val) > 4:
            raise IndexError("The length of the val array must be between 3 and 4")

        for i in val:
            if i >255:
                raise ValueError("The val must be between 0-255!")

        s = self.__offset + ind * 4
        if len(val) == 3:
            s += 1
        else:
            val[0] = self.__brightness_convert(val[0])

        self.__buf[s:s+len(val)] = val

    def __getitem__(self, ind):
        s = self.__offset + ind * 4
        val = self.__buf[s:s+4]
        val[0] = self.__brightness_revert(val[0])
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
        return val / self.nled

    @brightness.setter
    def brightness(self, val):
        for i in range(0, self.nled):
            s = self.__offset + i * 4
            self.__buf[s] = self.__brightness_convert(val)


if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    tree.brightness = 1
    while True:
        tree[1:tree.nled:2] = [255, 255, 255]
        tree.commit()
        tree[:] = [0, 0, 0]
        tree.commit()
        tree[2:tree.nled:2] = [255, 255, 255]
        tree.commit()
        tree[:] = [0, 0, 0]
        tree.commit()
    #tree.off()

