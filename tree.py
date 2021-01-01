from gpiozero import SPIDevice, SourceMixin
from numpy import array

class FastRGBChristmasTree(SourceMixin, SPIDevice):
    '''
    The FastRGBChristmasTree -- driver for The Pi Hut 3D RGB Christmas Tree

    This is a faster driver for the 3D RGB Christmas Tree from The Pi Hut. The
    original driver from The Pi Hut refreshes the whole Christmas Tree even if
    you change a single LED. This version allows you to change the state of
    multiple LEDs before sending the command down to the SPI bus. The indexing
    convention for the LEDs is also more natural.

    For more information about this driver, please visit its Github page at:
        https://github.com/fangfufu/FastRGBChristmasTree

    To buy The Pi Hut 3D RGB Christmas Tree, please visit:
        https://thepihut.com/products/3d-rgb-xmas-tree-for-raspberry-pi

    Attributes:
        autocommit (bool): Whether to automatically send SPI commands after
            changing the LED configuration. (Basically automatically call
            self.commit() after calling self.__setitem__())
        brightness (int): The default brightness of the LEDs, if the brightness
            is not specified. Brightness has to be between 0 to 30 (inclusive).
    '''

    def __init__(self, brightness=0, autocommit=False):
        '''
        Constructor

        Args:
            brightness (int): Sets the brightness attribute.
            autocommit (bool): Sets the autocommit attribute.
        '''
        super(FastRGBChristmasTree, self).__init__(mosi_pin=12, clock_pin=25)
        # Number of LEDs
        self.nled = 25
        # LED configuration array
        self.__led_config = array([[24, 19, 7, 0, 16, 15, 6, 12],
                                   [23, 20, 8, 1, 17, 14, 5, 11],
                                   [22, 21, 9, 2, 18, 13, 4, 10]])
        # Start of array __offset
        self.__offset = 4

        # frame padding
        frame_s = [0] * (self.__offset)
        frame_end = [0] * 5

        # transmit buffer
        self.__buf = frame_s + [0] * self.nled * 4 +frame_end

        self.brightness = brightness
        self.reset()

        self.autocommit = autocommit


    def __len__(self):
        ''' Returns the number of LEDs on the Christmas tree. '''
        return self.nled

    def __setitem__(self, ind, val):
        '''
        Set the colour and optionally brightness of LEDs

        Args:
            ind: The index of the LEDs, works in the same way as how you index
                a numpy array, more specifically it can be one of the following:
                    - an integer
                    - a 2-tuple of integer
                    - a slice
                    - a 2-tuple of slices
                For more on how the LEDs are indexed, please refer to the Github
                page.
            val: The settings for the LED(s). Each LED can be set using a list
                of the following format:
                    - [R, G, B], where each pixel value has to between 0-255.
                    - [Brightness, R, G, B], where Brightness is an integer
                    between 0-30 inclusive, and R, G, B is an integer between
                    0-255.
                Multiple LEDs can be set at once, using a list of lists. However
                the number of LEDs set must be either 1, or match the number
                LEDs indexed,

        Raises:
            IndexError: If there is a dimensional mismatch between the LED
            indices and the dimension of the colour list.
        '''
        if isinstance(ind, tuple) or isinstance(ind, slice):
            # Shortcut for the writing the star as a layer
            if isinstance(ind, tuple) and (ind[0] == 3):
                self.__setitem__(3, val)
                return

            # Handle changing multiple LEDs
            autocommit_disengaged = False
            if self.autocommit:
                autocommit_disengaged = True
                self.autocommit = False
            r = self.__led_config[ind].flatten()
            if type(val[0]) is not list:
                for i in r:
                    self.__setitem__(i, val)
            elif len(val) == len(r):
                for i in range(0, len(val)):
                    self.__setitem__(r[i], val[i])
            else:
                raise IndexError("Mismatch between the LED indices and the \
dimension of the colour list. ")
            if autocommit_disengaged:
                self.autocommit = True
                self.commit()
            return

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
            self.__buf[s] = self.__brightness_convert(val[0])
            s += 1

        # Swap RGB to BGR, we use negative indexing, so it is agnostic to the
        # size of val
        self.__buf[s]   = val[-1]
        self.__buf[s+1] = val[-2]
        self.__buf[s+2] = val[-3]

        if self.autocommit:
            self.commit()

    def __getitem__(self, ind):
        '''
        Retrive the brightness and colour settings the LEDs

        Args:
            ind: The index of the LEDs, works in the same way as how you index
                a numpy array, more specifically it can be one of the following:
                    - an integer
                    - a 2-tuple of integer
                    - a slice
                    - a 2-tuple of slices
                For more on how the LEDs are indexed, please refer to the Github
                page.

        Returns:
            If only one LED is specified, the LED setting in the format of
            [Brightness, R, G, B] will be returned, where Brightness is an
            integer between 0-30 inclusive and R, G, B is an integer between
            0-255.

            If multiple indices are supplied, then a list of with lists of LED
            setting will be returned.
        '''
        if isinstance(ind, tuple) or isinstance(ind, slice):
            # Shortcut for the writing the star as a layer
            if isinstance(ind, tuple) and (ind[0] == 3):
                return self.__getitem__(3)

            # Handle request for multiple LEDs
            val = []
            r = self.__led_config[ind].flatten()
            for i in r:
                val.append(self.__getitem__(i))
            return val
        else:
            s = self.__offset + ind * 4
            val = [None] * 4
            # Swap BGR back to RGB
            val[0] = self.__brightness_revert(self.__buf[s])
            val[1] = self.__buf[s+3]
            val[2] = self.__buf[s+2]
            val[3] = self.__buf[s+1]
            return val

    def __del__(self):
        ''' Destructor '''
        super(FastRGBChristmasTree, self).close()

    def __brightness_convert(self, val):
        ''' Convert brightness value to buffer format  '''
        if val > 30 or val < 0:
            raise ValueError("The brightness must be between 0 and 30")
        val = val + 1
        # 0b1110000 == 224
        return 0b11100000 | int(val)

    def __brightness_revert(self, val):
        ''' Convert buffer brightness t to human readable format '''
        return 0b00011111 & val - 1

    def commit(self):
        ''' Send the current LED configuration down the SPI bus '''
        self._spi.transfer(self.__buf)

    def off(self):
        ''' Turn off the LEDs '''
        self[:] =  [0, 0, 0, 0]
        self.star = [0, 0, 0, 0]
        self.commit()

    def reset(self):
        ''' Reset the LEDs by sending down zeros '''
        brightness = self.brightness
        for i in range(0, len(self.__buf)):
            self.__buf[i] = 0
        self.commit()
        self.brightness = brightness

    @property
    def star(self):
        ''' Return the value of the star on the LEDs '''
        return self.__getitem__(3)

    @star.setter
    def star(self,val):
        ''' Set the value of the star on the LEDs '''
        return self.__setitem__(3, val)

    @property
    def brightness(self):
        ''' Return the mean brightness of the LEDs '''
        val = 0
        for i in range(0, self.nled):
            s = self.__offset + i * 4
            val += self.__buf[s]
        return self.__brightness_revert(int(val / self.nled))

    @brightness.setter
    def brightness(self, val):
        ''' Set the brightness of the LEDs '''
        for i in range(0, self.nled):
            s = self.__offset + i * 4
            self.__buf[s] = self.__brightness_convert(val)

if __name__ == '__main__':
    tree = FastRGBChristmasTree()
    tree.off()

