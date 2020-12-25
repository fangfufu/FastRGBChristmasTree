from gpiozero import SPIDevice, SourceMixin
from colorzero import Color, Hue

class FastRGBChristmasTree(SourceMixin, SPIDevice):
    def __init__(self, brightness=0.5, *args, **kwargs):
        super(FastRGBChristmasTree, self).__init__(mosi_pin=12, clock_pin=25, *args, **kwargs)
        # Number of LEDs
        self.nled = 25
        # Start of array offset
        self.offset = 4
        # frame padding
        frame_start = [0] * (self.offset)
        frame_end = [0] * 5
        # transmit buffer
        self.__buf = frame_start + [0] * self.nled * 4 +frame_end

    def __len__(self):
        return self.nled

    #def __getitem__(self, index):

    def __setitem__(self, index, value):
        if index > self.nled or index < 0:
            raise IndexError("LED index must be between 0 and 24!")
        if len(value) < 3 or len(value) > 4:
            raise IndexError("The length of the value array must be between 3 and 4")

        for i in value:
            if i >255:
                raise ValueError("The value must be between 0-255!")

        start = self.offset + index * 4
        if len(value) == 3:
            start += 1
        else:
            value[0] = self.__brightness_converter(value[0])

        self.__buf[start:start+len(value)] = value

    def __del__(self):
        super(FastRGBChristmasTree, self).close()

    def __brightness_converter(self, brightness):
        if brightness > 31 or brightness < 0:
            raise ValueError("The brightness must be between 0 and 31")
        # 0b1110000 == 224
        return 0b11100000 | int(brightness)

    def commit(self):
        #print(self.__buf)
        self._spi.transfer(self.__buf)

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    while True:
        for i in range(0,25):
            tree[i] = [15, 255, 255, 255]
        tree.commit()
        for i in range(0,25):
            tree[i] = [15, 0, 0, 0]
        tree.commit()

