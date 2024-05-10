class Rectangle:

    def __init__(self, x: int, y: int, widht: int, height: int):
        self._x = x
        self._y = y
        self._width = widht
        self._height = height

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = width
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = height

    
class Squre(Rectangle):
    
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, size, size)
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = width
        self._height = width
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._width = height
        self._height = height
    

def resize(rectangle: Rectangle, width: int, height: int):
    rectangle.width = width
    rectangle.height = height
    assert rectangle.width == width and rectangle.height == height